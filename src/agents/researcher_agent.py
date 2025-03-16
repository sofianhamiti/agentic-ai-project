from typing import List, Any
from .base_agent import BaseAgent
from ..core.config import Config
from ..tools.web_search import WebSearchTool

class ResearcherAgent(BaseAgent):
    """An agent specialized in conducting research on various topics."""
    
    def __init__(
        self,
        config: Config,
        verbose: bool = False
    ):
        """Initialize the Researcher agent."""
        super().__init__(
            config=config,
            role="Research Specialist",
            goal="Conduct thorough research on topics and provide comprehensive, accurate information",
            backstory="""You are an expert researcher with experience in finding, analyzing, and 
            synthesizing information from multiple sources. You can quickly identify relevant information,
            distinguish credible sources, and present findings in a clear, organized manner. Your research
            is always thorough, balanced, and focused on providing the most accurate picture possible.""",
            verbose=verbose
        )
    
    def get_tools(self) -> List[Any]:
        """Get the tools available to this agent."""
        return [
            WebSearchTool()
        ]
    
    def research(self, topic: str, depth: str = "medium") -> str:
        """
        Conduct research on a given topic.
        
        Args:
            topic (str): The topic to research.
            depth (str): The depth of research to conduct (shallow, medium, deep).
            
        Returns:
            str: The research findings.
        """
        task = f"""
        Conduct {depth} research on the following topic:
        
        TOPIC: {topic}
        
        Your research should:
        1. Cover key aspects and subtopics
        2. Include factual information from reliable sources
        3. Present multiple perspectives when relevant
        4. Synthesize information into a coherent narrative
        5. Note areas of consensus and controversy
        
        Use the web search tool to gather information from various sources.
        Organize your findings in a clear, structured format.
        """
        
        return self.execute_task(task) 