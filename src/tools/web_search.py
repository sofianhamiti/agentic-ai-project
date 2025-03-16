from typing import Dict, Any, List
import abc
from duckduckgo_search import DDGS
from crewai.tools import BaseTool

# Base search engine class
class WebSearchEngine(abc.ABC):
    """Base class for web search engines."""
    
    @abc.abstractmethod
    def perform_search(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        """
        Execute a web search and return the results.
        
        Args:
            query (str): The search query to look up.
            max_results (int): Maximum number of results to return.
            
        Returns:
            List[Dict[str, str]]: A list of search results, each as a dictionary.
        """
        pass

# DuckDuckGo search implementation
class DuckDuckGoSearchEngine(WebSearchEngine):
    """DuckDuckGo search engine implementation."""
    
    def perform_search(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        """
        Execute a DuckDuckGo web search and return the results.
        
        Args:
            query (str): The search query to look up.
            max_results (int): Maximum number of results to return.
            
        Returns:
            List[Dict[str, str]]: A list of search results, each as a dictionary.
        """
        results = []
        try:
            ddgs = DDGS()
            for r in ddgs.text(query, max_results=max_results):
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("link", ""),
                    "snippet": r.get("body", "")
                })
        except Exception as e:
            print(f"DuckDuckGo search error: {str(e)}")
        return results

# Google search implementation (requires googlesearch-python package)
class GoogleSearchEngine(WebSearchEngine):
    """Google search engine implementation."""
    
    def perform_search(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        """
        Execute a Google web search and return the results.
        
        Args:
            query (str): The search query to look up.
            max_results (int): Maximum number of results to return.
            
        Returns:
            List[Dict[str, str]]: A list of search results, each as a dictionary.
        """
        results = []
        try:
            # This requires the googlesearch-python package
            # If not installed, it will fail gracefully
            from googlesearch import search
            
            for url in search(query, num_results=max_results):
                # Google search only provides URLs, not titles or snippets
                results.append({
                    "title": "Google Search Result",
                    "url": url,
                    "snippet": "No snippet available from Google search API"
                })
        except Exception as e:
            print(f"Google search error: {str(e)}")
        return results

class WebSearchTool(BaseTool):
    """Tool for performing web searches using multiple search engines with fallback."""
    
    name: str = "Web Search"
    description: str = """Search the web for information on a given topic.
Use this tool to find up-to-date information about news, facts, data, or any topic of interest.
The tool will try multiple search engines if available and return the most relevant results."""
    
    def __init__(self, preferred_engine: str = "duckduckgo"):
        """
        Initialize the web search tool.
        
        Args:
            preferred_engine (str): The preferred search engine to use first.
                Options: "duckduckgo", "google". Defaults to "duckduckgo".
        """
        super().__init__()
        self._search_engines = {
            "duckduckgo": DuckDuckGoSearchEngine(),
            "google": GoogleSearchEngine()
        }
        self._preferred_engine = preferred_engine.lower() if preferred_engine.lower() in self._search_engines else "duckduckgo"
        
    @property
    def preferred_engine(self) -> str:
        """Get the preferred search engine."""
        return self._preferred_engine
        
    def _run(self, query: str, max_results: int = 5) -> str:
        """
        Execute a web search and return the results.
        
        Args:
            query (str): The search query to look up.
            max_results (int): Maximum number of results to return (default: 5).
            
        Returns:
            str: The formatted search results.
        """
        # Try the preferred engine first
        engine_order = [self.preferred_engine] + [e for e in self._search_engines if e != self.preferred_engine]
        
        results = []
        for engine_name in engine_order:
            engine = self._search_engines[engine_name]
            engine_results = engine.perform_search(query, max_results)
            
            if engine_results:
                results = engine_results
                print(f"Using results from {engine_name} search engine")
                break
        
        # Format results for easier reading
        formatted_results = []
        for i, result in enumerate(results, 1):
            formatted_results.append(
                f"{i}. {result['title']}\n"
                f"   URL: {result['url']}\n"
                f"   {result['snippet']}\n"
            )
        
        formatted_text = "\n".join(formatted_results) if formatted_results else "No results found."
        
        return formatted_text 