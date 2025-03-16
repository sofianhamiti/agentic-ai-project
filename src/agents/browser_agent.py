import asyncio
from typing import List, Any, Dict, Optional
from pydantic import Field
from crewai import Agent
from .base_agent import BaseAgent
from ..core.config import Config
from ..tools.browser import BrowserUseTool
from ..tools.web_search import WebSearchTool
from ..tools.factory import ToolFactory
from ..core.schema import Message, Memory
from ..core.logger import get_logger

logger = get_logger(__name__)

class BrowserAgent(BaseAgent):
    """
    Browser agent specialized in web interactions, browsing, and content extraction.
    This agent can navigate websites, extract information, and interact with web elements.
    """
    
    def __init__(
        self,
        name: str = "Browser Agent",
        role: str = "Web Automation Expert",
        goal: str = "Navigate websites and automate browser interactions",
        backstory: str = "I am a browser automation expert who can navigate websites, interact with web elements, and extract information effectively.",
        verbose: bool = False,
        allow_delegation: bool = True,
        memory: Optional[List[Memory]] = None,
        **kwargs
    ):
        """
        Initialize the browser agent.
        
        Args:
            name: The name of the agent
            role: The role of the agent
            goal: The goal of the agent
            backstory: The backstory of the agent
            verbose: Whether to enable verbose logging
            allow_delegation: Whether to allow delegation to other agents
            memory: Optional list of memory items to initialize agent memory
            **kwargs: Additional arguments to pass to the agent constructor
        """
        super().__init__(
            name=name,
            role=role,
            goal=goal,
            backstory=backstory,
            verbose=verbose,
            allow_delegation=allow_delegation,
            **kwargs
        )
        
        # Initialize agent memory
        self._memory = memory or []
        logger.info(f"Initialized {name} with {len(self._memory)} memory items")
    
    def create_agent(self) -> Agent:
        """Create the browser agent with appropriate tools."""
        tools = self._get_tools()
        
        return Agent(
            name=self.name,
            role=self.role,
            goal=self.goal,
            backstory=self.backstory,
            verbose=self.verbose,
            allow_delegation=self.allow_delegation,
            tools=tools,
            **self.kwargs
        )
    
    def _get_tools(self) -> List[Any]:
        """Get the tools for the browser agent."""
        return [
            ToolFactory.create_tool("browser"),
            ToolFactory.create_tool("web_search"),
            ToolFactory.create_tool("terminal")
        ]
    
    def remember(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Add a memory item to the agent's memory.
        
        Args:
            content: The content of the memory
            metadata: Optional metadata for the memory
        """
        memory_item = Memory(
            content=content,
            metadata=metadata or {}
        )
        self._memory.append(memory_item)
        logger.debug(f"Added memory: {content[:50]}...")
    
    def get_memories(self) -> List[Memory]:
        """
        Get all memory items.
        
        Returns:
            List of memory items
        """
        return self._memory
        
    def get_tools(self) -> List[Any]:
        """Get the tools available to this agent."""
        return [
            BrowserUseTool(),
            WebSearchTool()
        ]
        
    async def browse_website(self, url: str, task: str) -> str:
        """
        Browse a website and perform a specific task.
        
        Args:
            url (str): The URL of the website to browse.
            task (str): Description of the task to perform on the website.
            
        Returns:
            str: The result of the browsing task.
        """
        browser_task = f"""
        Navigate to the website at {url} and perform the following task:
        
        TASK: {task}
        
        Use the browser tool to:
        1. Navigate to the URL
        2. Interact with the necessary elements on the page
        3. Extract the relevant information
        4. Document your findings
        
        If you encounter any obstacles, try different approaches to achieve the task.
        """
        
        return await self.execute_task(browser_task)
        
    async def extract_data(self, url: str, data_description: str) -> str:
        """
        Extract specific data from a website.
        
        Args:
            url (str): The URL of the website to extract data from.
            data_description (str): Description of the data to extract.
            
        Returns:
            str: The extracted data.
        """
        extraction_task = f"""
        Navigate to the website at {url} and extract the following data:
        
        DATA TO EXTRACT: {data_description}
        
        Follow these steps:
        1. Navigate to the URL
        2. Locate the relevant sections containing the target data
        3. Extract the information
        4. Format and present the extracted data clearly
        5. Document your extraction process
        
        Use browser actions like get_text, get_html, and screenshot as needed.
        """
        
        return await self.execute_task(extraction_task)
        
    async def research_topic(self, topic: str, depth: str = "medium") -> str:
        """
        Research a topic on the web and provide comprehensive information.
        
        Args:
            topic (str): The topic to research.
            depth (str): How deep the research should go (shallow, medium, deep).
            
        Returns:
            str: The research findings.
        """
        research_task = f"""
        Conduct {depth} research on the following topic:
        
        TOPIC: {topic}
        
        Follow these steps:
        1. Search for information about the topic
        2. Visit multiple relevant websites from the search results
        3. Extract key information, facts, and insights
        4. Compare and cross-reference information from different sources
        5. Synthesize the findings into a comprehensive report
        
        Your research should be thorough and cover different aspects of the topic.
        Use both the web search tool and browser tool for effective research.
        """
        
        return await self.execute_task(research_task) 