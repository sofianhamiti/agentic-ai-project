from typing import List, Any
from .base_agent import BaseAgent
from ..core.config import Config
from ..tools.bash import BashTool
from ..tools.file_saver import FileSaverTool
from ..tools.python_executor import PythonExecutorTool
from ..tools.terminal import TerminalTool

class SWEAgent(BaseAgent):
    """
    Software Engineer agent specialized in programming and development tasks.
    This agent can execute code, interact with the terminal, and develop software.
    """
    
    def __init__(
        self,
        config: Config,
        verbose: bool = False
    ):
        """Initialize the Software Engineer agent."""
        super().__init__(
            config=config,
            role="Software Engineer",
            goal="Develop high-quality, efficient software solutions and assist with coding tasks",
            backstory="""You are an expert software engineer with extensive experience in multiple programming languages 
            and development paradigms. You're adept at understanding requirements, writing clean code, debugging issues, 
            and implementing efficient solutions. You always follow best practices and industry standards.""",
            verbose=verbose
        )
        
    def get_tools(self) -> List[Any]:
        """Get the tools available to this agent."""
        return [
            BashTool(),
            TerminalTool(),
            FileSaverTool(),
            PythonExecutorTool()
        ]
        
    async def develop_solution(self, requirements: str) -> str:
        """
        Develop a solution based on requirements.
        
        Args:
            requirements (str): The requirements for the software solution.
            
        Returns:
            str: The result of the development process.
        """
        task = f"""
        Analyze the following requirements and develop a software solution:
        {requirements}
        
        Follow these steps:
        1. Analyze the requirements
        2. Plan the implementation
        3. Write the code
        4. Test the solution
        5. Document your approach
        
        Use your tools (bash, terminal, file_saver, python_executor) as needed to implement the solution.
        """
        
        return await self.execute_task(task)
        
    async def review_code(self, code: str) -> str:
        """
        Review code for issues, bugs, and improvements.
        
        Args:
            code (str): The code to review.
            
        Returns:
            str: Code review results.
        """
        task = f"""
        Review the following code for issues, bugs, and potential improvements:
        
        ```
        {code}
        ```
        
        Analyze:
        - Code quality and readability
        - Potential bugs or errors
        - Performance considerations
        - Security issues
        - Best practices
        
        Provide specific recommendations for improvement.
        """
        
        return await self.execute_task(task) 