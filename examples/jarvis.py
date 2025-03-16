"""
Jarvis: An AI Assistant with Web Search Capabilities.

This example shows a conversational agent that can:
1. Interact with users to understand and clarify their needs
2. Use web search to find relevant information
3. Evaluate search results and follow up with additional searches as needed
4. Provide comprehensive, accurate responses based on the most up-to-date information
"""

import sys
import os
import time
import json
from typing import Dict, List, Any, Optional

# Add project root to Python path if not already there
if os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) not in sys.path:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.config import Config
from src.agents import CoordinatorAgent, WebSearchAgent
from src.memory.chat_history import get_session_id, get_chat_history


def run_jarvis(query: str, config: Config = None) -> Dict[str, Any]:
    """
    Run Jarvis assistant to answer user queries using web search.
    
    Args:
        query: The user's query or question
        config: Optional configuration
        
    Returns:
        A dictionary containing the session information and results
    """
    if config is None:
        config = Config()
    
    # Initialize session
    session_id = get_session_id()
    output_dir = config.get_output_dir()
    session_dir = os.path.join(output_dir, f"session_{session_id}")
    os.makedirs(session_dir, exist_ok=True)
    
    # Get chat history
    history = get_chat_history(session_id, output_dir)
    
    # Initialize agents
    coordinator = CoordinatorAgent(config=config, verbose=True)
    web_searcher = WebSearchAgent(config=config, verbose=True)
    
    # Initialize context
    context = {
        "query": query,
        "session_id": session_id,
        "clarifications": None,
        "search_strategy": None,
        "search_results": None,
        "final_response": None
    }
    
    print(f"\n--- JARVIS ACTIVATED ---\n")
    print(f"Session ID: {session_id}")
    print(f"User Query: {query}\n")
    
    # Save the original query for history
    history.add_user_message(f"Original query: {query}")
    
    # Step 1: Determine if clarification is needed
    print("\n--- ANALYZING QUERY ---\n")
    
    clarification_prompt = f"""
    Analyze this user query: "{query}"
    
    Determine if clarification is needed before proceeding with research.
    If clarification is needed, provide 1-3 specific questions to help understand the user's intent better.
    If clarification is NOT needed, respond with "No clarification needed. The query is clear."
    
    Be concise and specific in your clarification questions.
    """
    
    clarification_questions = coordinator.execute_task(clarification_prompt)
    
    # Extract text content from AIMessage if needed
    clarification_text = clarification_questions
    if hasattr(clarification_questions, 'content'):
        clarification_text = clarification_questions.content
    
    if "no clarification needed" not in clarification_text.lower() and len(clarification_text) > 10:
        print("\n=== CLARIFICATION NEEDED ===\n")
        print(clarification_text)
        
        # Ask the user for clarifications
        user_clarifications = input("\nPlease provide clarifications: ")
        context["clarifications"] = user_clarifications
        history.add_user_message(f"Clarifications: {user_clarifications}")
    else:
        print("\n=== NO CLARIFICATION NEEDED ===\n")
        context["clarifications"] = "No clarifications were needed."
    
    # Step 2: Coordinator formulates high-level search strategy
    print("\n--- FORMULATING SEARCH STRATEGY ---\n")
    
    web_search_prompt = f"""
    For the following user query, create a comprehensive web search strategy:
    
    User query: "{query}"
    User clarifications: "{context.get('clarifications', '')}"
    
    Create a detailed strategy with specific search queries that would help gather all the information needed.
    For each search query, explain what information we expect to find and why it's relevant.
    Structure your response as a numbered list of search queries, with brief explanations.
    """
    
    search_strategy = coordinator.execute_task(web_search_prompt)
    context["search_strategy"] = search_strategy
    
    print(f"\n=== SEARCH STRATEGY ===\n{search_strategy}\n=== END OF STRATEGY ===\n")
    
    # Step 3: WebSearchAgent handles the entire search process
    print("\n--- EXECUTING SEARCH STRATEGY ---\n")
    
    search_results = web_searcher.execute_search_strategy(
        query=query,
        strategy=search_strategy,
        session_id=session_id
    )
    
    context["search_results"] = search_results
    
    print(f"\n=== SEARCH RESULTS SUMMARY ===\n")
    print(f"Searches conducted: {len(search_results['queries'])}")
    print(f"Search complete: {search_results['complete']}")
    print(f"=== END OF SUMMARY ===\n")
    
    # Check if additional searches are needed
    if not search_results['complete']:
        print("\n--- ADDITIONAL SEARCHES NEEDED ---\n")
        print(search_results['evaluation'])
        
        # Here we could implement a loop to conduct additional searches
        # For simplicity, we'll proceed with what we have
        print("\nProceeding with current results...")
    
    # Step 4: Formulate final response
    print("\n--- FORMULATING FINAL RESPONSE ---\n")
    
    response_prompt = f"""
    Formulate a comprehensive response to the user's question:
    
    Original question: "{query}"
    User clarifications: "{context.get('clarifications', '')}"
    
    Based on our research, here's what we found:
    {search_results["combined_results"]["text"]}
    
    Create a well-structured, comprehensive, and accurate response that directly addresses the user's query.
    Include relevant facts, details, and context based on the search results.
    If there are limitations to the information available, acknowledge them.
    """
    
    final_response = coordinator.execute_task(response_prompt)
    context["final_response"] = final_response
    
    # Extract text from AIMessage if needed
    if hasattr(final_response, 'content'):
        final_response_text = final_response.content
    else:
        final_response_text = str(final_response)
    
    print(f"\n=== FINAL RESPONSE ===\n{final_response_text}\n=== END OF RESPONSE ===\n")
    
    return {
        "query": query,
        "session_id": session_id,
        "final_response": final_response_text
    }


def main():
    """Run Jarvis assistant."""
    # Initialize config
    config = Config()
    
    # Get user input
    query = input("How can I help you today? ")
    
    if not query:
        print("Please provide a question or request.")
        return
    
    # Execute Jarvis
    start_time = time.time()
    result = run_jarvis(query, config)
    end_time = time.time()
    
    # Print completion information
    print("\n=== JARVIS TASK COMPLETED ===")
    print(f"Task completed in {end_time - start_time:.2f} seconds")
    print("\nFinal response has been provided above.")


def save_text(content: Any, filepath: str) -> None:
    """Save text content to a file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # Handle different types of content
    if hasattr(content, 'content'):
        # If this is an AIMessage or similar object with content attribute
        text_content = content.content
    else:
        # Convert to string if it's not already
        text_content = str(content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text_content)


if __name__ == "__main__":
    main() 