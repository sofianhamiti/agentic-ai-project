from typing import List, Dict, Any, Optional
from pydantic import Field
from .base_agent import BaseAgent
from ..core.config import Config
from ..tools.tool_collection import ToolCollection
from ..tools.web_search import WebSearchTool
from ..tools.browser import BrowserUseTool
from ..tools.python_executor import PythonExecutorTool
from ..tools.file_saver import FileSaverTool
from ..tools.terminal import TerminalTool
import os

class MainAgent(BaseAgent):
    """
    A versatile general-purpose agent that uses multiple tools to solve tasks.
    
    This agent is designed to handle a wide range of tasks by leveraging a 
    comprehensive set of tools and capabilities, including web search, browsing, 
    code execution, file operations, and terminal commands.
    """
    
    def __init__(
        self,
        config: Config = None,
        verbose: bool = False
    ):
        """Initialize the Main agent."""
        super().__init__(
            config=config,
            role="Versatile Task Solver",
            goal="Solve diverse tasks using a combination of tools and capabilities",
            backstory="""You are a versatile AI assistant designed to handle a wide range of tasks.
            You have access to multiple tools including web search, browser automation, Python code execution,
            file operations, and terminal commands. You can analyze complex problems, break them down into
            manageable steps, and use the appropriate tools to solve each part efficiently.
            You approach problems methodically, considering different strategies and using the best
            combination of tools for each task.""",
            verbose=verbose
        )
        
    def get_tools(self) -> List[Any]:
        """Get the comprehensive set of tools available to this agent."""
        # Create the default tools collection
        tools = ToolCollection(
            WebSearchTool(),
            PythonExecutorTool(),
            FileSaverTool(),
            TerminalTool()
        )
        
        # Try to add the browser tool, but only if we're not in a Docker container
        if not os.environ.get('PYTHONPATH') == '/app':  # Check if we're in Docker
            browser_tool = BrowserUseTool()
            if hasattr(browser_tool, '_ensure_driver_initialized') and browser_tool._ensure_driver_initialized():
                tools.add_tool(browser_tool)
        
        return tools.get_all_tools()
    
    def research(self, topic: str, depth: str = "comprehensive", tools: List[Any] = None) -> str:
        """
        Conduct research on a given topic.
        
        Args:
            topic: The topic to research
            depth: Depth of research ("brief", "moderate", "comprehensive")
            tools: Optional list of tools to use for research
            
        Returns:
            Research findings as formatted text
        """
        if tools is None:
            tools = self.get_tools()
            
        task_description = f"""
        Conduct {depth} research on: {topic}
        
        Your task is to:
        1. Gather information from multiple sources
        2. Verify facts from different websites
        3. Organize your findings in a clear, structured format
        4. Include relevant statistics, data, and facts
        5. Provide a well-structured summary with sections and subsections
        
        Ensure your research is thorough and accurate.
        """
        
        task = self.create_task(task_description)
        return self.execute_task(task, tools=tools)
        
    def create_content(self, content_type: str, topic: str, target_audience: str, tools: List[Any] = None) -> str:
        """
        Create content on a specific topic.
        
        Args:
            content_type: Type of content to create (article, blog post, report, etc.)
            topic: The topic for the content
            target_audience: The intended audience for the content
            tools: Optional list of tools to use for content creation
            
        Returns:
            Generated content as formatted text
        """
        if tools is None:
            tools = self.get_tools()
            
        task_description = f"""
        Create a {content_type} about {topic} for {target_audience}.
        
        Your content should:
        1. Be engaging and appropriate for the target audience
        2. Include accurate information backed by research
        3. Be well-structured with clear sections
        4. Have a compelling introduction and conclusion
        5. Include relevant examples, data, or case studies where appropriate
        
        Make sure your {content_type} is original, informative, and valuable to readers.
        """
        
        task = self.create_task(task_description)
        return self.execute_task(task, tools=tools)
        
    def analyze_data(self, data_source: str, analysis_goals: str, tools: List[Any] = None) -> str:
        """
        Analyze data from a specified source.
        
        Args:
            data_source: Source of the data to analyze
            analysis_goals: Goals or questions for the analysis
            tools: Optional list of tools to use for data analysis
            
        Returns:
            Analysis results as formatted text
        """
        if tools is None:
            tools = self.get_tools()
            
        task_description = f"""
        Analyze data from {data_source} with the following goals:
        
        {analysis_goals}
        
        Your analysis should:
        1. Use appropriate methods to extract and process the data
        2. Present clear findings with supporting evidence
        3. Address all the specified analysis goals
        4. Include visualizations or tables where helpful
        5. Provide actionable insights based on the data
        
        Ensure your analysis is accurate, thorough, and addresses the key questions.
        """
        
        task = self.create_task(task_description)
        return self.execute_task(task, tools=tools) 