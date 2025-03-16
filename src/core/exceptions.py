"""
Exception hierarchy for the crewai_learning package.

This module defines a standardized exception hierarchy for error handling
throughout the application. All custom exceptions inherit from the base
CrewAILearningError class, enabling consistent error handling patterns.
"""

from typing import Optional, Any, Dict


class CrewAILearningError(Exception):
    """
    Base exception for all crewai_learning exceptions.
    
    All specific error types in the application should inherit from this class.
    """
    
    def __init__(self, message: str, **kwargs):
        """
        Initialize the base exception.
        
        Args:
            message: Error message
            **kwargs: Additional error context as keyword arguments
        """
        self.message = message
        self.context = kwargs
        super().__init__(message)


class ConfigError(CrewAILearningError):
    """
    Exception raised for configuration-related errors.
    
    These may include missing or invalid configuration files,
    invalid configuration values, or environment variable issues.
    """
    pass


class AgentError(CrewAILearningError):
    """
    Exception raised for agent-related errors.
    
    These may include agent creation failures, execution errors,
    or issues with agent configuration.
    """
    
    def __init__(self, message: str, agent_name: Optional[str] = None, **kwargs):
        """
        Initialize the agent error.
        
        Args:
            message: Error message
            agent_name: Name of the agent that caused the error
            **kwargs: Additional error context
        """
        super().__init__(message, agent_name=agent_name, **kwargs)


class ToolError(CrewAILearningError):
    """
    Exception raised for tool-related errors.
    
    These may include tool creation failures, execution errors,
    or issues with tool configuration.
    """
    
    def __init__(self, message: str, tool_name: Optional[str] = None, **kwargs):
        """
        Initialize the tool error.
        
        Args:
            message: Error message
            tool_name: Name of the tool that caused the error
            **kwargs: Additional error context
        """
        super().__init__(message, tool_name=tool_name, **kwargs)


class FlowError(CrewAILearningError):
    """
    Exception raised for flow-related errors.
    
    These may include flow creation failures, execution errors,
    or issues with flow configuration.
    """
    
    def __init__(self, message: str, flow_name: Optional[str] = None, **kwargs):
        """
        Initialize the flow error.
        
        Args:
            message: Error message
            flow_name: Name of the flow that caused the error
            **kwargs: Additional error context
        """
        super().__init__(message, flow_name=flow_name, **kwargs)


class ModelError(CrewAILearningError):
    """
    Exception raised for model-related errors.
    
    These may include API errors, model loading failures,
    or issues with model configuration.
    """
    
    def __init__(self, message: str, model_name: Optional[str] = None, **kwargs):
        """
        Initialize the model error.
        
        Args:
            message: Error message
            model_name: Name of the model that caused the error
            **kwargs: Additional error context
        """
        super().__init__(message, model_name=model_name, **kwargs)

class TokenLimitExceeded(CrewAILearningError):
    """Raised when the token limit is exceeded in an LLM request."""
    
    def __init__(self, message="Token limit exceeded", max_tokens=None):
        self.max_tokens = max_tokens
        details = f" (max: {max_tokens})" if max_tokens else ""
        self.message = f"{message}{details}"
        super().__init__(self.message)

class APIError(CrewAILearningError):
    """Raised when there's an error communicating with an external API."""
    
    def __init__(self, message, status_code=None, service_name=None):
        self.status_code = status_code
        self.service_name = service_name
        
        details = []
        if service_name:
            details.append(f"service: {service_name}")
        if status_code:
            details.append(f"status: {status_code}")
            
        detail_str = f" ({', '.join(details)})" if details else ""
        self.message = f"{message}{detail_str}"
        
        super().__init__(self.message)

class ValidationError(CrewAILearningError):
    """Raised when validation of data or parameters fails."""
    pass 