"""
Schema definitions for the CrewAI Learning project.
Contains Pydantic models for structured data throughout the application.
"""
from enum import Enum
from typing import Any, Dict, List, Literal, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime


class Role(str, Enum):
    """Message role options for conversation interactions."""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


# Type aliases for validation
ROLE_VALUES = tuple(role.value for role in Role)
ROLE_TYPE = Literal[tuple(role.value for role in Role)]  # type: ignore


class AgentState(str, Enum):
    """Agent execution states to track agent lifecycle."""
    IDLE = "IDLE"
    RUNNING = "RUNNING"
    FINISHED = "FINISHED"
    ERROR = "ERROR"


class ToolCall(BaseModel):
    """Represents a tool/function call in a message."""
    
    id: str
    name: str
    arguments: Dict[str, Any]
    

class Message(BaseModel):
    """
    Represents a message in agent communication.
    
    Messages are used for structured communication between agents,
    tools, and the system.
    """
    
    content: str = Field(
        description="The content of the message"
    )
    
    sender: str = Field(
        description="The name or identifier of the sender"
    )
    
    recipient: Optional[str] = Field(
        default=None,
        description="The name or identifier of the recipient, if applicable"
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="When the message was created"
    )
    
    message_type: str = Field(
        default="text",
        description="The type of message (e.g., text, command, result)"
    )
    
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata associated with the message"
    )
    
    def to_dict(self) -> dict:
        """Convert message to dictionary format for API compatibility."""
        message = {"role": self.role}
        if self.content is not None:
            message["content"] = self.content
        if self.tool_calls is not None:
            message["tool_calls"] = [tool_call.model_dump() for tool_call in self.tool_calls]
        if self.name is not None:
            message["name"] = self.name
        if self.tool_call_id is not None:
            message["tool_call_id"] = self.tool_call_id
        return message
    
    @classmethod
    def user_message(cls, content: str) -> "Message":
        """Create a user message."""
        return cls(role=Role.USER, content=content)
    
    @classmethod
    def system_message(cls, content: str) -> "Message":
        """Create a system message."""
        return cls(role=Role.SYSTEM, content=content)
    
    @classmethod
    def assistant_message(cls, content: Optional[str] = None) -> "Message":
        """Create an assistant message."""
        return cls(role=Role.ASSISTANT, content=content)
    
    @classmethod
    def tool_message(cls, content: str, name: str, tool_call_id: str) -> "Message":
        """Create a tool result message."""
        return cls(
            role=Role.TOOL, 
            content=content, 
            name=name, 
            tool_call_id=tool_call_id
        )


class Memory(BaseModel):
    """
    Represents a memory item stored by an agent.
    
    Memories allow agents to retain information across interactions
    and maintain context for future decisions.
    """
    
    content: str = Field(
        description="The content of the memory"
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="When the memory was created"
    )
    
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata associated with the memory"
    )
    
    importance: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Importance score from 0.0 to 1.0, used for prioritization"
    )


class ToolInput(BaseModel):
    """Structured input for tool execution."""
    
    arguments: Dict[str, Any] = Field(default_factory=dict)
    

class ToolOutput(BaseModel):
    """Structured output from tool execution."""
    
    success: bool = Field(default=True)
    data: Any = Field(default=None)
    error: Optional[str] = Field(default=None)
    
    @classmethod
    def success_result(cls, data: Any) -> "ToolOutput":
        """Create a successful tool output."""
        return cls(success=True, data=data)
    
    @classmethod
    def error_result(cls, error: str) -> "ToolOutput":
        """Create an error tool output."""
        return cls(success=False, error=error)


class TaskResult(BaseModel):
    """
    Represents the result of a task execution.
    
    Task results provide a standardized structure for returning
    operation outcomes from agents, tools, and flows.
    """
    
    success: bool = Field(
        description="Whether the task was successful"
    )
    
    result: Optional[Union[str, Dict[str, Any]]] = Field(
        default=None,
        description="The result of the task, if applicable"
    )
    
    error: Optional[str] = Field(
        default=None,
        description="Error message if the task failed"
    )
    
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata about the task execution"
    )
    
    execution_time: Optional[float] = Field(
        default=None,
        description="Execution time in seconds"
    ) 