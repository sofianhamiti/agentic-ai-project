"""
Coordinator Agent for managing workflows and overseeing task execution.

This agent is responsible for:
1. Understanding user requirements and planning task execution
2. Coordinating specialized agents (researchers, engineers, etc.)
3. Ensuring quality and verifying results against requirements
4. Communicating with users throughout the process
"""

import os
from typing import Dict, Any, Optional, List
from langchain_community.tools import DuckDuckGoSearchRun

from ..core.config import Config
from ..memory.chat_history import get_session_id, get_chat_history

class CoordinatorAgent:
    """
    Agent responsible for coordinating workflows, understanding user requirements,
    and managing the overall execution process.
    """
    
    def __init__(self, config: Optional[Config] = None, verbose: bool = False):
        """
        Initialize a CoordinatorAgent.
        
        Args:
            config: Configuration for the agent
            verbose: Whether to enable verbose output
        """
        self.config = config or Config()
        self.verbose = verbose
        self.llm = self.config.get_llm()
        self.search_tool = DuckDuckGoSearchRun()
        self._session_id = None
        self.output_dir = self.config.get_output_dir()
    
    def _get_session_id(self) -> str:
        """Get or create a session ID."""
        if not self._session_id:
            self._session_id = get_session_id()
            # Create session directory
            os.makedirs(os.path.join(self.output_dir, f"session_{self._session_id}"), exist_ok=True)
        return self._session_id
    
    def execute_task(self, prompt: str) -> str:
        """
        Execute a task based on the provided prompt.
        
        Args:
            prompt: The prompt describing the task
            
        Returns:
            The result of executing the task
        """
        session_id = self._get_session_id()
        history = get_chat_history(session_id, self.output_dir)
        
        # Log the prompt
        history.add_user_message(f"Task: {prompt}")
        
        # Execute task using LLM
        result = self.llm.invoke(prompt)
        
        # Log the result
        history.add_ai_message(result)
        
        # Save the result
        self._save_text(
            f"Prompt: {prompt}\n\nResult: {result}",
            f"session_{session_id}/task_result.txt"
        )
        
        return result
    
    def _save_text(self, content: str, filename: str) -> None:
        """Save text content to a file."""
        filepath = os.path.join(self.output_dir, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content) 