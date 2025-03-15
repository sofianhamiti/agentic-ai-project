from typing import Dict, Any, List
from duckduckgo_search import DDGS
from crewai.tools import BaseTool

class WebSearchTool(BaseTool):
    """Tool for performing web searches using DuckDuckGo."""
    
    name: str = "Web Search"
    description: str = """Search the web for information on a given topic.
Use this tool to find up-to-date information about news, facts, data, or any topic of interest."""
    
    def __init__(self):
        super().__init__()
        self.ddgs = DDGS()
        
    def _run(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """
        Execute a web search and return the results.
        
        Args:
            query (str): The search query to look up.
            max_results (int): Maximum number of results to return (default: 5).
            
        Returns:
            Dict[str, Any]: The search results and metadata.
        """
        results = []
        try:
            for r in self.ddgs.text(query, max_results=max_results):
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("link", ""),
                    "snippet": r.get("body", "")
                })
        except Exception as e:
            return {
                "success": False,
                "error": f"Error during web search: {str(e)}",
                "results": []
            }
            
        # Format results for easier reading
        formatted_results = []
        for i, result in enumerate(results, 1):
            formatted_results.append(
                f"{i}. {result['title']}\n"
                f"   URL: {result['url']}\n"
                f"   {result['snippet']}\n"
            )
        
        formatted_text = "\n".join(formatted_results) if formatted_results else "No results found."
        
        return {
            "success": len(results) > 0,
            "query": query,
            "count": len(results),
            "results": results,
            "formatted_text": formatted_text
        } 