from typing import List, Any
from .base_agent import BaseAgent
from ..core.config import Config
from ..tools.browser_use_tool import BrowserUseTool
from ..tools.web_search import WebSearchTool

class BrowserAgent(BaseAgent):
    """
    Browser agent specialized in web interactions, browsing, and content extraction.
    This agent can navigate websites, extract information, and interact with web elements.
    """
    
    def __init__(
        self,
        config: Config,
        verbose: bool = False
    ):
        """Initialize the Browser agent."""
        super().__init__(
            config=config,
            role="Web Browser Expert",
            goal="Navigate and interact with websites to gather information and perform web tasks",
            backstory="""You are an expert at navigating the web and extracting information from websites. 
            You know how to efficiently browse websites, interact with web elements, and extract 
            the most relevant information. You're skilled at automating web tasks and can work 
            with various web interfaces effectively.""",
            verbose=verbose
        )
        
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