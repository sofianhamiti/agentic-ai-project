"""
Factory for creating agent instances.

This module provides a factory class for instantiating different types of agents.
"""

from typing import Dict, Type, Optional
from .base_agent import BaseAgent
from .coordinator_agent import CoordinatorAgent
from ..core.config import Config


class AgentFactory:
    """
    Factory for creating different types of agents.
    
    This factory makes it easy to instantiate agents by name without directly
    importing their classes.
    """
    
    # Registry of available agent types
    _registry: Dict[str, Type[BaseAgent]] = {
        "coordinator": CoordinatorAgent,
    }
    
    @classmethod
    def create(cls, agent_type: str, config: Optional[Config] = None, verbose: bool = False) -> BaseAgent:
        """
        Create an agent instance by type name.
        
        Args:
            agent_type: The type of agent to create (coordinator)
            config: Optional configuration for the agent
            verbose: Whether to enable verbose output
            
        Returns:
            An instantiated agent of the requested type
            
        Raises:
            ValueError: If the requested agent type is not found in the registry
        """
        if agent_type not in cls._registry:
            raise ValueError(f"Unknown agent type: {agent_type}. Available types are: {list(cls._registry.keys())}")
        
        agent_class = cls._registry[agent_type]
        return agent_class(config=config, verbose=verbose)

    @classmethod
    def get_available_agent_types(cls) -> Dict[str, str]:
        """
        Get the available agent types.
        
        Returns:
            A dictionary mapping agent types to their descriptions.
        """
        return {
            "coordinator": "Versatile agent with multiple tools for diverse tasks",
        } 