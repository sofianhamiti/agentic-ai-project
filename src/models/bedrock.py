import os
from typing import Dict, Any
import boto3
from crewai import LLM

class BedrockModel:
    """Implementation of Bedrock model integration."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the Bedrock model with configuration."""
        self.validate_config(config)
        self.config = config
        self._setup_aws()
        
    def _setup_aws(self) -> None:
        """Set up AWS configuration."""
        region = self.config.get('region', 'us-west-2')
        boto3.setup_default_session(region_name=region)
    
    def get_llm(self) -> LLM:
        """Get a configured Bedrock LLM instance."""
        return LLM(
            model=f"bedrock/{self.config['model_name']}",
            temperature=self.config.get('temperature', 0.7)
        )
    
    def validate_config(self, config: Dict[str, Any]) -> None:
        """Validate the Bedrock configuration."""
        if not config.get('model_name'):
            raise ValueError("model_name is required for Bedrock configuration")
        
        if not config.get('region'):
            raise ValueError("AWS region is required for Bedrock configuration")
        
        # Validate AWS credentials are available using boto3 session
        try:
            session = boto3.Session()
            credentials = session.get_credentials()
            if not credentials:
                raise ValueError("No AWS credentials found")
        except Exception as e:
            raise ValueError(
                f"AWS credentials validation failed: {str(e)}. "
                "Ensure credentials are available via ~/.aws/credentials, "
                "environment variables, or instance profile."
            ) 