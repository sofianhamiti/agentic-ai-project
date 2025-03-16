from typing import List, Dict, Any
from crewai import Agent, Task, Crew, Process
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
    
    def execute_task(self, task_description: str, tools: List[Any] = None) -> str:
        """Execute a task using a Task object and Crew."""
        # Create a task with the agent
        task = Task(
            description=task_description,
            expected_output="Detailed response to the task",
            agent=self._agent,
            tools=tools if tools is not None else self.get_tools()
        )
        
        # Create a simple crew with just this agent and task
        crew = Crew(
            agents=[self._agent],
            tasks=[task],
            process=Process.sequential,
            verbose=self.verbose
        )
        
        # Execute the task and return the result
        result = crew.kickoff()
        return result
    
    def get_tools(self) -> List[Any]:
        """Get the list of tools available to this agent."""
        return []  # Override in specific agent implementations
    
    @property
    def agent(self) -> Agent:
        """Get the underlying CrewAI agent."""
        return self._agent 