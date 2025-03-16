"""
Web Search Agent for gathering information from the internet.

This agent is specialized in search query formulation, search execution,
and synthesis of search results from the web.
"""

import os
import json
import re
from typing import Dict, Any, Optional, List

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.tools import DuckDuckGoSearchRun

from ..core.config import Config
from ..core.structured_output import SearchResult
from ..memory.chat_history import get_session_id, get_chat_history


class WebSearchAgent:
    """Agent that performs web searches and answers questions using LangChain."""
    
    def __init__(self, config: Optional[Config] = None, verbose: bool = False):
        """Initialize the web search agent."""
        self.config = config or Config()
        self.verbose = verbose
        self._session_id = None
        self.output_dir = self.config.get_output_dir()
        
        # Set up LangChain components
        self.llm = self.config.get_llm()
        self.search_tool = DuckDuckGoSearchRun()
        self.parser = PydanticOutputParser(pydantic_object=SearchResult)
        
        # Create search chain with LCEL
        self.search_chain = (
            # First step: web search
            {"query": RunnablePassthrough()} | 
            {"search_results": lambda x: self.search_tool.invoke(x["query"]), 
             "query": lambda x: x["query"],
             "format_instructions": lambda _: self.parser.get_format_instructions()} |
            # Second step: structure the results
            PromptTemplate.from_template(
                """Perform a web search for: {query}
                
                Search results:
                {search_results}
                
                Summarize these results in a structured format.
                {format_instructions}
                """
            ) | 
            self.llm | 
            self.parser
        )
    
    def _get_session_id(self) -> str:
        """Get or create a session ID."""
        if not self._session_id:
            self._session_id = get_session_id()
            # Create session directory
            os.makedirs(os.path.join(self.output_dir, f"session_{self._session_id}"), exist_ok=True)
        return self._session_id
    
    def search(self, query: str) -> Dict[str, Any]:
        """Perform a structured web search using LangChain."""
        session_id = self._get_session_id()
        history = get_chat_history(session_id, self.output_dir)
        history.add_user_message(f"Search query: {query}")
        
        try:
            # Run the LangChain search chain
            search_data = self.search_chain.invoke({
                "query": query,
                "format_instructions": self.parser.get_format_instructions()
            })
            
            # Convert to dictionary for storage
            result_dict = search_data.model_dump()
            
            # Save to history and file
            history.add_ai_message(f"Search completed. Found: {search_data.main_findings}")
            self._save_json(result_dict, f"session_{session_id}/search_results.json")
            
            return result_dict
            
        except Exception as e:
            if self.verbose:
                print(f"Error in structured search: {str(e)}")
            
            # Fallback to basic search
            search_results = self.search_tool.invoke(query)
            history.add_ai_message(search_results)
            
            # Return in SearchResult-like format
            return {
                "main_findings": search_results,
                "key_points": [],
                "sources": [],
                "confidence": 5
            }
    
    def answer_question(self, question: str) -> str:
        """Answer a specific question using web search."""
        session_id = self._get_session_id()
        history = get_chat_history(session_id, self.output_dir)
        history.add_user_message(f"Question: {question}")
        
        # Search for information
        search_result = self.search(question)
        
        # Format the answer
        answer = search_result["main_findings"]
        
        # Add sources if available
        if search_result.get("sources"):
            sources_text = "\n".join(f"- {source}" for source in search_result["sources"])
            answer += f"\n\nSources:\n{sources_text}"
        
        # Save the answer
        self._save_text(
            f"Question: {question}\n\nAnswer: {answer}",
            f"session_{session_id}/question_answer.txt"
        )
        history.add_ai_message(answer)
        
        return answer
    
    def execute_search_strategy(self, query: str, strategy: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute a complete search strategy based on the provided plan.
        
        Args:
            query: The original user query
            strategy: The search strategy text
            session_id: Optional session ID to use
            
        Returns:
            Dictionary containing search results, evaluation, and completion status
        """
        # Set or create session ID
        if session_id:
            self._session_id = session_id
        else:
            session_id = self._get_session_id()
            
        # Extract search queries from the strategy
        search_queries = self._extract_search_queries(strategy)
        
        if self.verbose:
            print(f"Executing {len(search_queries)} searches from strategy...")
            
        # Execute each search query
        all_search_results = []
        for i, search_query in enumerate(search_queries, 1):
            if self.verbose:
                print(f"Search {i}/{len(search_queries)}: {search_query}")
            
            # Execute the search
            result = self.search(search_query)
            all_search_results.append({
                "query": search_query,
                "result": result,
                "number": i
            })
        
        # Combine and evaluate results
        combined_results = self._create_combined_results(query, all_search_results)
        
        # Create an evaluation
        evaluation = self._evaluate_search_results(query, combined_results)
        
        # Determine if search is complete
        search_complete = self._is_search_complete(evaluation)
        
        # Save the search results
        self._save_json({
            "original_query": query,
            "strategy": strategy,
            "searches": all_search_results,
            "combined_results": combined_results,
            "evaluation": evaluation,
            "complete": search_complete
        }, f"session_{session_id}/search_strategy_results.json")
        
        # Return the complete package
        return {
            "original_query": query,
            "strategy": strategy,
            "queries": search_queries,
            "results": all_search_results,
            "combined_results": combined_results,
            "evaluation": evaluation,
            "complete": search_complete
        }
    
    def _extract_search_queries(self, strategy) -> List[str]:
        """Extract search queries from the strategy text."""
        # Handle AIMessage objects by extracting content
        if hasattr(strategy, 'content'):
            strategy_text = strategy.content
        else:
            strategy_text = str(strategy)
            
        lines = strategy_text.split('\n')
        queries = []
        
        # Look for lines that might contain search queries
        for line in lines:
            line = line.strip()
            
            # Check if this line looks like a query plan
            if any(word in line.lower() for word in ["search for", "query:", "research:", "look up"]):
                # Clean it up
                query = re.sub(r'^.*?[:-]\s*', '', line).strip('" ')
                if query and len(query) > 5:  # Minimum reasonable query length
                    queries.append(query)
            
            # Check for numbered or bulleted items
            elif re.match(r'^\d+[\.\)]|^[-*•]', line):
                # Extract content after bullet/number
                query = re.sub(r'^[\d\.\)\-*•\s]+', '', line).strip('" ')
                if query and len(query) > 5:
                    queries.append(query)
        
        # If we couldn't extract any queries, just use the strategy itself
        if not queries:
            # Try to find quoted phrases
            quoted = re.findall(r'"([^"]+)"', strategy_text)
            if quoted:
                return quoted[:3]  # Return up to 3 quoted phrases
            
            # Fall back to using the whole strategy
            return [strategy_text.strip()]
        
        return queries[:5]  # Limit to 5 queries
    
    def _create_combined_results(self, query: str, search_results: List[Dict]) -> Dict[str, Any]:
        """Combine multiple search results into a coherent response."""
        # Create a combined search prompt
        combined_prompt = f"""
        I've searched for information about: "{query}"
        
        Based on {len(search_results)} different searches, here's what I found:
        
        """
        
        # Add each search result
        for result in search_results:
            combined_prompt += f"Search {result['number']}: {result['query']}\n"
            combined_prompt += f"Findings: {result['result']['main_findings']}\n\n"
        
        # Ask the LLM to combine the results
        template = """
        Combine these search results into a comprehensive answer:
        
        Original question: {query}
        
        Search information:
        {combined_results}
        
        Provide a well-structured, comprehensive answer that synthesizes all the information.
        Include only factual information from the search results.
        """
        
        prompt = PromptTemplate.from_template(template)
        
        # Generate the combined result
        combined_text = self.llm.invoke(prompt.format(
            query=query,
            combined_results=combined_prompt
        ))
        
        return {
            "text": combined_text,
            "num_searches": len(search_results),
            "search_queries": [r["query"] for r in search_results]
        }
    
    def _evaluate_search_results(self, query: str, combined_results: Dict) -> str:
        """Evaluate if the search results adequately answer the original query."""
        template = """
        Evaluate if the search results adequately answer the original query.
        
        Original query: {query}
        
        Combined search results:
        {results}
        
        Provide an evaluation of:
        1. How well the search results answer the query
        2. If any important information is missing
        3. If additional searches would be helpful, and if so, what specific searches
        4. A clear judgment: "SEARCH COMPLETE" or "ADDITIONAL SEARCHES NEEDED"
        """
        
        prompt = PromptTemplate.from_template(template)
        
        # Generate the evaluation
        evaluation = self.llm.invoke(prompt.format(
            query=query,
            results=combined_results["text"]
        ))
        
        return evaluation
    
    def _is_search_complete(self, evaluation) -> bool:
        """Evaluate if the search results adequately answer the original query."""
        # Check the type of evaluation response
        evaluation_text = evaluation
        if hasattr(evaluation, 'content'):
            evaluation_text = evaluation.content
        
        # Convert to string if not already
        evaluation_text = str(evaluation_text).lower()
        
        # Indicators that search results are complete
        complete_indicators = [
            "adequately answer",
            "sufficient information",
            "comprehensive enough",
            "query is answered",
            "satisfactory"
        ]
        
        # Indicators that more searches are needed
        incomplete_indicators = [
            "more information needed",
            "additional search",
            "missing information",
            "need to explore"
        ]
        
        # Check if any complete indicators are present
        if any(indicator in evaluation_text for indicator in complete_indicators):
            return True
            
        # Check if any incomplete indicators are present
        if any(indicator in evaluation_text for indicator in incomplete_indicators):
            return False
            
        # Default to complete
        return True
    
    def _save_text(self, content: str, filename: str) -> None:
        """Save text content to a file."""
        filepath = os.path.join(self.output_dir, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _save_json(self, data: Any, filename: str) -> None:
        """Save JSON content to a file."""
        filepath = os.path.join(self.output_dir, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Convert data to JSON-serializable format
        serializable_data = self._make_json_serializable(data)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(serializable_data, f, indent=2)
    
    def _make_json_serializable(self, obj: Any) -> Any:
        """Recursively convert an object to JSON-serializable types."""
        if hasattr(obj, 'content'):
            # Handle AIMessage or similar objects with content attribute
            return obj.content
        elif hasattr(obj, 'model_dump'):
            # Handle Pydantic models
            return obj.model_dump()
        elif isinstance(obj, dict):
            # Recursively convert dictionary values
            return {k: self._make_json_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            # Recursively convert list items
            return [self._make_json_serializable(item) for item in obj]
        elif isinstance(obj, (str, int, float, bool, type(None))):
            # Basic JSON types are already serializable
            return obj
        else:
            # Fallback to string representation
            return str(obj) 