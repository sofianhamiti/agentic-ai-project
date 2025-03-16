"""
Configuration management for the AI system.

Provides a thread-safe singleton configuration with YAML support.
"""
import os
import threading
import yaml
from typing import Dict, Any, Optional

from .exceptions import ConfigError
from .logger import logger
from ..models import create_bedrock_llm


class Config:
    """Simple configuration loader using YAML."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration from YAML file."""
        self.config_data = {}
        self.config_path = config_path
        self.load_config()
    
    def load_config(self):
        """Load configuration from YAML file."""
        # If config path provided, use it
        if self.config_path and os.path.exists(self.config_path):
            path = self.config_path
        else:
            # Otherwise check default locations
            possible_paths = [
                './config/config.yaml',
                './config/config.yml',
                './config.yaml',
                './config.yml'
            ]
            
            path = None
            for p in possible_paths:
                if os.path.exists(p):
                    path = p
                    break
            
            if not path:
                # Create minimal default config if no file found
                self.config_data = {
                    "llm": {
                        "model_name": "anthropic.claude-3-sonnet-20240229-v1:0",
                        "temperature": 0.7,
                        "max_tokens": 4096,
                        "region": "us-west-2"
                    },
                    "memory": {
                        "output_dir": "./output"
                    }
                }
                return
        
        # Load config from file
        try:
            with open(path, 'r') as f:
                self.config_data = yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading config: {str(e)}")
            # Fall back to defaults
            self.config_data = {
                "llm": {
                    "model_name": "anthropic.claude-3-sonnet-20240229-v1:0",
                    "temperature": 0.7,
                    "max_tokens": 4096,
                    "region": "us-west-2"
                },
                "memory": {
                    "output_dir": "./output"
                }
            }
    
    def get_llm_config(self) -> Dict[str, Any]:
        """Get LLM configuration settings."""
        return self.config_data.get("llm", {})
    
    def get_output_dir(self) -> str:
        """Get output directory for files and history."""
        memory_config = self.config_data.get("memory", {})
        
        # Use Docker path if in container, otherwise local path
        if os.path.exists("/.dockerenv"):
            return memory_config.get("output_dir", "/tmp/output")
        else:
            return memory_config.get("local_output_dir", "./output")

    def in_docker(self) -> bool:
        """
        Check if we're running inside a Docker container.
        
        Returns:
            True if running in Docker, False otherwise
        """
        return os.path.exists("/.dockerenv")
    
    def get_llm(self):
        """Get a LangChain LLM instance based on configuration."""
        return create_bedrock_llm(self.get_llm_config())
    
    @property
    def llm(self) -> Dict[str, Any]:
        """Get LLM configuration."""
        return self.get_llm_config()
    
    def get_tool_config(self, tool_name: str) -> Dict[str, Any]:
        """Get configuration for a specific tool."""
        return self.config_data.get('tools', {}).get(tool_name, {})

    @classmethod
    def from_yaml(cls, yaml_path: str) -> 'Config':
        """
        Create a Config instance from a specific YAML file.
        
        Args:
            yaml_path: Path to the YAML configuration file
            
        Returns:
            Config instance
        """
        instance = cls(config_path=yaml_path)
        return instance 