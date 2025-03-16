"""
Configuration management for the CrewAI Learning project.
Provides a thread-safe singleton configuration with YAML support.
"""
import os
import threading
import yaml
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

from .exceptions import ConfigError
from .logger import logger
from ..models.bedrock import BedrockModel


class LLMSettings(BaseModel):
    """LLM configuration settings."""
    
    model_name: str = Field(..., description="Model name to use")
    temperature: float = Field(0.7, description="Sampling temperature")
    max_tokens: int = Field(4096, description="Maximum tokens per response")
    provider: str = Field(..., description="LLM provider (bedrock, openai)")
    region: Optional[str] = Field(None, description="AWS region for Bedrock")


class ToolSettings(BaseModel):
    """Tool configuration settings."""
    
    enabled: bool = Field(True, description="Whether the tool is enabled")
    
    class Config:
        extra = "allow"  # Allow extra fields for tool-specific settings


class Config:
    """
    Thread-safe singleton configuration manager for the project.
    
    Loads configuration from YAML files and provides access to settings.
    """
    
    _instance = None
    _lock = threading.Lock()
    _initialized = False
    
    def __new__(cls):
        """Ensure only one instance is created (singleton pattern)."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the configuration only once."""
        if not self._initialized:
            with self._lock:
                if not self._initialized:
                    self._llm_config = None
                    self._tools_config = {}
                    self._llm_instance = None
                    self._load_config()
                    self._initialized = True
    
    def _get_config_path(self) -> str:
        """Get the configuration file path."""
        # Get the project root directory (three levels up from this file)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        config_path = os.path.join(project_root, 'config', 'config.yaml')
        
        if not os.path.exists(config_path):
            raise ConfigError(f"Configuration file not found: {config_path}")
            
        return config_path
    
    def _load_config(self) -> None:
        """Load configuration from YAML file."""
        try:
            config_path = self._get_config_path()
            logger.info(f"Loading configuration from {config_path}")
            
            with open(config_path, 'r') as f:
                config_data = yaml.safe_load(f)
            
            # Parse LLM configuration
            llm_data = config_data.get('llm', {})
            self._llm_config = LLMSettings(
                model_name=llm_data.get('model_name'),
                temperature=float(llm_data.get('temperature', 0.7)),
                max_tokens=int(llm_data.get('max_tokens', 4096)),
                provider=llm_data.get('provider'),
                region=llm_data.get('region')
            )
            
            # Parse tools configuration
            self._tools_config = {}
            for tool_name, tool_config in config_data.get('tools', {}).items():
                self._tools_config[tool_name] = tool_config
                
            logger.debug(f"Configuration loaded successfully")
        except Exception as e:
            logger.error(f"Error loading configuration: {str(e)}")
            raise ConfigError(f"Failed to load configuration: {str(e)}")
    
    def reload(self) -> None:
        """Reload configuration from file."""
        with self._lock:
            self._load_config()
            self._llm_instance = None  # Force recreation of LLM instance
    
    def validate(self) -> None:
        """Validate the configuration."""
        if self._llm_config.temperature < 0 or self._llm_config.temperature > 1:
            raise ConfigError("Temperature must be between 0 and 1")
        
        if self._llm_config.max_tokens < 1:
            raise ConfigError("Max tokens must be positive")
        
        # Create and validate the model to catch any issues early
        self.get_llm()
    
    def get_llm(self):
        """Get the LLM instance, creating it if necessary."""
        if self._llm_instance is None:
            with self._lock:
                if self._llm_instance is None:
                    llm_config = {
                        'model_name': self._llm_config.model_name,
                        'temperature': self._llm_config.temperature,
                        'max_tokens': self._llm_config.max_tokens,
                        'region': self._llm_config.region
                    }
                    model = BedrockModel(llm_config)
                    self._llm_instance = model.get_llm()
        return self._llm_instance
    
    @property
    def llm(self) -> LLMSettings:
        """Get LLM configuration."""
        return self._llm_config
    
    @property
    def tools_config(self) -> Dict[str, Any]:
        """Get tools configuration."""
        return self._tools_config
    
    def get_tool_config(self, tool_name: str) -> Dict[str, Any]:
        """Get configuration for a specific tool."""
        return self._tools_config.get(tool_name, {})


# Create a global instance of the configuration
config = Config() 