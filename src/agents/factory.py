from typing import Optional
from .base_agent import BaseAgent
from ..core.config import Config

class AgentFactory:
    """Factory for creating various types of agents."""
    
    @staticmethod
    def create_agent(agent_type: str, config: Config = None, verbose: bool = False) -> BaseAgent:
        """
        Create an agent of the specified type.
        
        Args:
            agent_type: Type of agent to create ("swe", "planning", "browser", etc.)
            config: Configuration object (optional)
            verbose: Whether the agent should output verbose logs
            
        Returns:
            An instance of the requested agent type
            
        Raises:
            ValueError: If the agent type is unknown
        """
        # If config is None, create a new Config instance
        if config is None:
            config = Config()
            
        if agent_type == "swe":
            from .swe_agent import SWEAgent
            return SWEAgent(config, verbose=verbose)
        elif agent_type == "planning":
            from .planning_agent import PlanningAgent
            return PlanningAgent(config, verbose=verbose)
        elif agent_type == "browser":
            from .browser_agent import BrowserAgent
            return BrowserAgent(config, verbose=verbose)
        elif agent_type == "researcher":
            from .researcher_agent import ResearcherAgent
            return ResearcherAgent(config, verbose=verbose)
        elif agent_type == "main_agent":
            from .main_agent import MainAgent
            return MainAgent(config, verbose=verbose)
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")
    
    @staticmethod
    def list_available_agents() -> list[str]:
        """List all available agent types."""
        return ["swe", "planning", "browser", "researcher", "main_agent"] 