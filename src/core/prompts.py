"""
Utility for loading prompts from configuration files.

This module provides functions for loading and managing prompt templates
from YAML configuration files, with support for example-specific overrides.
"""

import os
import yaml
from typing import Dict, Any, Optional


def load_prompts(agent_type: str, example: Optional[str] = None) -> Dict[str, str]:
    """
    Load prompts for a specific agent type with optional example-specific overrides.
    
    Args:
        agent_type: The type of agent to load prompts for (e.g., "main", "browser")
        example: Optional example name for loading example-specific prompt overrides
        
    Returns:
        A dictionary mapping prompt names to prompt templates
        
    Raises:
        FileNotFoundError: If the base prompt file for the agent type doesn't exist
    """
    base_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "prompts")
    
    # Load base prompts for the agent
    agent_file = os.path.join(base_path, f"{agent_type}.yaml")
    try:
        with open(agent_file, 'r') as f:
            prompts = yaml.safe_load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"No prompt configuration found for agent type '{agent_type}' at {agent_file}")
    
    # Optionally override with example-specific prompts
    if example:
        example_file = os.path.join(base_path, "examples", f"{example}.yaml")
        if os.path.exists(example_file):
            with open(example_file, 'r') as f:
                example_prompts = yaml.safe_load(f)
                if example_prompts:
                    # Update prompts with example-specific ones (allows partial overrides)
                    prompts.update(example_prompts)
    
    return prompts


def format_prompt(prompt_template: str, **kwargs) -> str:
    """
    Format a prompt template with the provided keyword arguments.
    
    Args:
        prompt_template: The prompt template string with {placeholders}
        **kwargs: Keyword arguments to substitute into the template
        
    Returns:
        The formatted prompt string
    """
    try:
        return prompt_template.format(**kwargs)
    except KeyError as e:
        raise KeyError(f"Missing required placeholder in prompt template: {e}")


def load_and_format_prompt(agent_type: str, prompt_name: str, example: Optional[str] = None, **kwargs) -> str:
    """
    Load a specific prompt by name and format it with the provided arguments.
    
    Args:
        agent_type: The type of agent to load prompts for
        prompt_name: The specific prompt to load
        example: Optional example name for loading example-specific prompt overrides
        **kwargs: Keyword arguments to substitute into the prompt template
        
    Returns:
        The formatted prompt string
        
    Raises:
        KeyError: If the requested prompt is not found or a required placeholder is missing
    """
    prompts = load_prompts(agent_type, example)
    
    if prompt_name not in prompts:
        raise KeyError(f"Prompt '{prompt_name}' not found for agent type '{agent_type}'")
    
    return format_prompt(prompts[prompt_name], **kwargs) 