"""
AWS Bedrock LLM integration.

This module handles the creation and configuration of AWS Bedrock LLM instances.
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from langchain_aws import BedrockLLM, ChatBedrock


class BedrockSettings(BaseModel):
    """Bedrock configuration settings."""
    
    model_name: str = Field(..., description="Bedrock model name to use")
    temperature: float = Field(0.7, description="Sampling temperature")
    max_tokens: int = Field(4096, description="Maximum tokens per response")
    region: str = Field("us-west-2", description="AWS region for Bedrock")


def create_bedrock_llm(config: Dict[str, Any]):
    """
    Create a LangChain LLM instance for AWS Bedrock.
    
    Args:
        config: LLM configuration dictionary
        
    Returns:
        A configured AWS Bedrock LLM instance
    """
    # Get parameters
    model_name = config.get("model_name")
    region = config.get("region", "us-west-2")
    temperature = config.get("temperature", 0.7)
    max_tokens = config.get("max_tokens", 4096)
    
    # Model kwargs with parameters
    model_kwargs = {
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    # Choose the right model class based on model name
    is_claude_v3 = "claude-3" in model_name.lower()
    
    if is_claude_v3:
        return ChatBedrock(
            model_id=model_name,
            region_name=region,
            model_kwargs=model_kwargs
        )
    else:
        return BedrockLLM(
            model_id=model_name,
            region_name=region,
            model_kwargs=model_kwargs
        ) 