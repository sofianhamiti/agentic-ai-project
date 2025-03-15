from typing import List, Any
from ..base_agent import BaseAgent
from ...core.config import Config
from ...tools.web_search import WebSearchTool
from ...tools.web_browser import WebBrowserTool

class ResearcherAgent(BaseAgent):
    """An agent specialized in conducting research on various topics."""
    
    def __init__(self, config: Config):
        super().__init__(
            config=config,
            role="Research Specialist",
            goal="Conduct thorough research and provide comprehensive, accurate information",
            backstory="""I am an expert researcher with a keen eye for detail and a 
            methodical approach to gathering and analyzing information. I have extensive 
            experience in various fields and am skilled at finding and verifying information 
            from multiple sources.""",
            verbose=True
        )
        self._tools = self.get_tools()
    
    def get_tools(self) -> List[Any]:
        """Get the tools available to the researcher agent."""
        tools = []
        
        if self.config.tools_config['search']['enabled']:
            tools.append(WebSearchTool(
                max_results=self.config.tools_config['search']['max_results']
            ))
            
        if self.config.tools_config['web_browser']['enabled']:
            tools.append(WebBrowserTool(
                timeout=self.config.tools_config['web_browser']['timeout']
            ))
            
        return tools
    
    async def research(self, topic: str) -> str:
        """Conduct research on a specific topic."""
        task = f"""
        Conduct thorough research on the topic: {topic}
        
        Please follow these steps:
        1. Search for relevant and up-to-date information
        2. Verify information from multiple sources
        3. Analyze and synthesize the findings
        4. Provide a comprehensive summary
        5. Include citations and sources
        
        Focus on accuracy and completeness while maintaining objectivity.
        """
        
        return await self.execute_task(task) 