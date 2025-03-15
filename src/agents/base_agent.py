from typing import List, Dict, Any
from crewai import Agent
from ..core.config import Config

class BaseAgent:
    """Base agent class that all specific agents should inherit from."""
    
    def __init__(
        self,
        config: Config,
        role: str,
        goal: str,
        backstory: str,
        verbose: bool = False
    ):
        self.config = config
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.verbose = verbose
        self._agent = self._create_agent()
    
    def _create_agent(self) -> Agent:
        """Create a CrewAI agent with the specified configuration."""
        return Agent(
            role=self.role,
            goal=self.goal,
            backstory=self.backstory,
            verbose=self.verbose,
            allow_delegation=True,
            llm=self.config.get_llm()  # Use the LLM from config
        )
    
    async def execute_task(self, task: str) -> str:
        """Execute a task."""
        return await self._agent.run(task)
    
    def get_tools(self) -> List[Any]:
        """Get the list of tools available to this agent."""
        return []  # Override in specific agent implementations
    
    @property
    def agent(self) -> Agent:
        """Get the underlying CrewAI agent."""
        return self._agent 