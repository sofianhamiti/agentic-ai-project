from typing import Any, Dict, List
from duckduckgo_search import DDGS

class WebSearchTool:
    """A tool for performing web searches using DuckDuckGo."""
    
    def __init__(self, max_results: int = 5):
        self.max_results = max_results
        self.ddgs = DDGS()
        
    def name(self) -> str:
        return "web_search"
        
    def description(self) -> str:
        return "Search the web for information on a given topic"
        
    def parameters(self) -> Dict[str, Any]:
        return {
            "query": {
                "type": "string",
                "description": "The search query to look up"
            },
            "max_results": {
                "type": "integer",
                "description": "Maximum number of results to return",
                "default": 5
            }
        }
    
    async def _execute(self, query: str, max_results: int = None) -> List[Dict[str, str]]:
        """Execute the web search."""
        if max_results is None:
            max_results = self.max_results
            
        results = []
        try:
            for r in self.ddgs.text(query, max_results=max_results):
                results.append({
                    "title": r.get("title", ""),
                    "link": r.get("link", ""),
                    "snippet": r.get("body", "")
                })
        except Exception as e:
            print(f"Error during web search: {str(e)}")
            return []
            
        return results
    
    async def run(self, query: str, max_results: int = None) -> str:
        """Run the web search and format results."""
        results = await self._execute(query, max_results)
        
        if not results:
            return "No results found."
            
        formatted_results = []
        for i, result in enumerate(results, 1):
            formatted_results.append(
                f"{i}. {result['title']}\n"
                f"   URL: {result['link']}\n"
                f"   {result['snippet']}\n"
            )
            
        return "\n".join(formatted_results) 