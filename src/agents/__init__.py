"""
Agent module for the AI system.

This module provides different agent implementations for specialized tasks.
"""

from .base_agent import BaseAgent
from .coordinator_agent import CoordinatorAgent
from .web_search_agent import WebSearchAgent

__all__ = [
    "BaseAgent",
    "CoordinatorAgent",
    "WebSearchAgent"
]
