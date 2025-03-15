from typing import List, Any
from .base_agent import BaseAgent
from ..core.config import Config
from ..tools.planning import PlanningTool, TaskBreakdownTool
from ..tools.web_search import WebSearchTool

class PlanningAgent(BaseAgent):
    """
    Planning agent specialized in breaking down complex problems and creating structured plans.
    """
    
    def __init__(
        self,
        config: Config,
        verbose: bool = False
    ):
        """Initialize the Planning agent."""
        super().__init__(
            config=config,
            role="Strategic Planner",
            goal="Create comprehensive, effective plans for solving complex problems",
            backstory="""You are an expert strategist and planner with experience in breaking down complex problems 
            into manageable parts. You excel at creating structured plans that consider all aspects of a problem, 
            including potential obstacles and alternative approaches. Your methodical approach ensures that plans 
            are both comprehensive and practical.""",
            verbose=verbose
        )
        
    def get_tools(self) -> List[Any]:
        """Get the tools available to this agent."""
        return [
            PlanningTool(),
            TaskBreakdownTool(),
            WebSearchTool()
        ]
        
    async def create_plan(self, objective: str, context: str = "") -> str:
        """
        Create a comprehensive plan for achieving an objective.
        
        Args:
            objective (str): The objective to achieve.
            context (str): Additional context or background information.
            
        Returns:
            str: A detailed plan.
        """
        task = f"""
        Create a comprehensive plan for achieving the following objective:
        
        OBJECTIVE: {objective}
        
        CONTEXT: {context}
        
        Your plan should include:
        1. A clear breakdown of the main steps
        2. Identification of potential challenges and mitigation strategies
        3. Resource requirements
        4. Timeline and milestones
        5. Success criteria
        
        Use the planning and task breakdown tools to create a structured, detailed plan.
        If necessary, use web search to gather relevant information to inform your plan.
        """
        
        return await self.execute_task(task)
        
    async def analyze_problem(self, problem: str) -> str:
        """
        Analyze a complex problem and provide insights.
        
        Args:
            problem (str): The problem to analyze.
            
        Returns:
            str: Analysis of the problem with recommendations.
        """
        task = f"""
        Analyze the following problem in depth:
        
        PROBLEM: {problem}
        
        Provide:
        1. A breakdown of the key components of the problem
        2. Root cause analysis
        3. Identification of stakeholders and their concerns
        4. Potential approaches to address the problem
        5. Recommendations for next steps
        
        Use your task breakdown and planning tools to structure your analysis.
        """
        
        return await self.execute_task(task) 