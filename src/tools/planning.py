from typing import Dict, Any, List
from crewai.tools import BaseTool

class PlanningTool(BaseTool):
    """Tool for planning and breaking down complex tasks."""
    
    name: str = "Planning Tool"
    description: str = """Create a structured plan for solving complex problems.
Use this tool to break down a complex problem into manageable steps, create a sequence 
of actions, and formulate a strategic approach to achieve a goal."""
    
    def _run(self, problem: str, context: str = "", max_steps: int = 10) -> Dict[str, Any]:
        """
        Create a structured plan for solving a complex problem.
        
        Args:
            problem (str): The problem or task to plan for.
            context (str): Additional context or background information.
            max_steps (int): Maximum number of steps in the plan.
            
        Returns:
            Dict[str, Any]: A structured plan with steps, dependencies, and rationale.
        """
        # This tool would normally use an LLM to generate the plan
        # Since we can't call an LLM directly from a tool, this is just a template
        # The actual implementation would delegate to the agent's language model
        
        # For now, return a structured template that the agent can fill in
        return {
            "problem": problem,
            "context": context,
            "plan": {
                "steps": [
                    {"id": 1, "description": "Analyze the problem", "status": "pending"}
                    # Additional steps would be added by the agent
                ],
                "dependencies": [],
                "estimated_completion_time": "Unknown without further analysis"
            },
            "guidance": "Use this template to create a detailed plan with specific steps."
        }


class TaskBreakdownTool(BaseTool):
    """Tool for breaking down tasks into smaller, manageable subtasks."""
    
    name: str = "Task Breakdown"
    description: str = """Break down a complex task into smaller, manageable subtasks.
Use this tool when you have a large task that needs to be divided into smaller pieces."""
    
    def _run(self, task: str, depth: int = 2) -> Dict[str, Any]:
        """
        Break down a task into subtasks.
        
        Args:
            task (str): The task to break down.
            depth (int): The depth of breakdown (1-3).
            
        Returns:
            Dict[str, Any]: A hierarchical breakdown of tasks.
        """
        # This is a template that would be filled in by the agent
        # The actual implementation would use the agent's language model
        
        return {
            "task": task,
            "breakdown": {
                "level_1": [
                    {"id": "1.1", "description": "First major component of the task"}
                    # Additional items would be added by the agent
                ],
                "level_2": [] if depth < 2 else [
                    {"id": "1.1.1", "description": "Subcomponent of 1.1"}
                    # Additional items would be added by the agent
                ],
                "level_3": [] if depth < 3 else [
                    {"id": "1.1.1.1", "description": "Further breakdown of 1.1.1"}
                    # Additional items would be added by the agent
                ]
            }
        } 