from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from crewai import Crew, Task, Agent

class BaseFlow(ABC):
    """Base class for all flows."""
    
    def __init__(self, agents: List[Agent], name: str = ""):
        """
        Initialize a flow with agents.
        
        Args:
            agents: List of agents to use in the flow
            name: Optional name for the flow
        """
        self.agents = agents
        self.name = name or self.__class__.__name__
        self.tasks = []
        self.crew = None
    
    @abstractmethod
    def create_tasks(self) -> List[Task]:
        """
        Create tasks for the flow.
        Must be implemented by subclasses.
        
        Returns:
            A list of Task objects
        """
        pass
    
    def build_crew(self) -> Crew:
        """
        Build a crew with the flow's agents and tasks.
        
        Returns:
            A configured Crew object
        """
        # Create tasks if they don't exist
        if not self.tasks:
            self.tasks = self.create_tasks()
            
        # Create the crew
        self.crew = Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=True,
            process=self.process
        )
        
        return self.crew
    
    def process(self, manager_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the output from the crew manager.
        
        Args:
            manager_output: The output from the crew manager
            
        Returns:
            The processed output
        """
        # By default, just return the output
        # Subclasses can override this to provide custom processing
        return manager_output
    
    async def run(self) -> Dict[str, Any]:
        """
        Run the flow.
        
        Returns:
            The result of the flow execution
        """
        if not self.crew:
            self.build_crew()
            
        # Run the crew
        result = await self.crew.run()
        
        return result 