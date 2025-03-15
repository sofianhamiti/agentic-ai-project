from dataclasses import dataclass
from typing import Dict, Any
import yaml
import os
from crewai import LLM
from ..models.bedrock import BedrockModel

@dataclass
class Config:
    """Configuration class for the project."""
    
    # LLM settings
    model_name: str
    temperature: float
    max_tokens: int
    provider: str
    region: str
    
    # Tool configurations
    tools_config: Dict[str, Any]
    
    # LLM instance
    _llm: LLM = None
    
    @classmethod
    def from_yaml(cls, config_path: str = None) -> 'Config':
        """Create a Config instance from YAML file."""
        if config_path is None:
            # Get the project root directory (two levels up from this file)
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            config_path = os.path.join(project_root, 'config', 'config.yaml')
            
        with open(config_path, 'r') as f:
            config_data = yaml.safe_load(f)
            
        return cls(
            model_name=config_data['llm']['model_name'],
            temperature=float(config_data['llm']['temperature']),
            max_tokens=int(config_data['llm']['max_tokens']),
            provider=config_data['llm']['provider'],
            region=config_data['llm']['region'],
            tools_config=config_data['tools']
        )
    
    def validate(self) -> None:
        """Validate the configuration."""
        if self.temperature < 0 or self.temperature > 1:
            raise ValueError("Temperature must be between 0 and 1")
        
        if self.max_tokens < 1:
            raise ValueError("Max tokens must be positive")
        
        # Create and validate the model
        self.get_llm()
    
    def get_llm(self) -> LLM:
        """Get the LLM instance, creating it if necessary."""
        if self._llm is None:
            llm_config = {
                'model_name': self.model_name,
                'temperature': self.temperature,
                'max_tokens': self.max_tokens,
                'region': self.region
            }
            model = BedrockModel(llm_config)
            self._llm = model.get_llm()
        return self._llm 