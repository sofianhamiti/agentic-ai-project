from typing import List, Dict, Any
from crewai import Task, Agent
from .base_flow import BaseFlow

class PlanningFlow(BaseFlow):
    """
    A flow for planning and executing complex tasks.
    This flow coordinates planning agents with execution agents.
    """
    
    def __init__(self, planner: Agent, executors: List[Agent], name: str = "Planning Flow"):
        """
        Initialize a planning flow.
        
        Args:
            planner: The planning agent
            executors: List of execution agents
            name: Name of the flow
        """
        agents = [planner] + executors
        super().__init__(agents, name)
        self.planner = planner
        self.executors = executors
    
    def create_tasks(self) -> List[Task]:
        """
        Create tasks for the planning flow.
        
        Returns:
            A list of Task objects
        """
        tasks = []
        
        # Planning task
        planning_task = Task(
            description="Create a comprehensive plan to solve the problem",
            agent=self.planner,
            expected_output="A detailed plan with steps, dependencies, and resource requirements"
        )
        tasks.append(planning_task)
        
        # Execution tasks - one per executor agent
        for i, executor in enumerate(self.executors):
            execution_task = Task(
                description=f"Execute part {i+1} of the plan",
                agent=executor,
                expected_output="Results of plan execution",
                context=[planning_task]  # Depends on the planning task
            )
            tasks.append(execution_task)
        
        return tasks
    
    def process(self, manager_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the output from the flow.
        
        Args:
            manager_output: The output from the crew manager
            
        Returns:
            The processed output with plan and execution results
        """
        # Extract the plan and execution results
        results = manager_output.get("results", {})
        
        # Structure the response in a more meaningful way
        processed_output = {
            "plan": results.get(0, "No plan generated"),  # First task is the planning task
            "execution_results": [results.get(i+1, "No result") for i in range(len(self.executors))],
            "status": "completed"
        }
        
        return processed_output 