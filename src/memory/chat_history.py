"""Simple chat history utilities built on LangChain."""

import os
import uuid
import datetime
from typing import Optional, List

from langchain_core.messages import BaseMessage
from langchain_community.chat_message_histories import FileChatMessageHistory


def get_session_id() -> str:
    """Create a unique session ID."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    return f"{timestamp}_{unique_id}"


def get_chat_history(session_id: str, output_dir: str = "./output") -> FileChatMessageHistory:
    """Get a file-based chat history for the given session ID."""
    # Ensure the output directory exists
    session_dir = os.path.join(output_dir, f"session_{session_id}")
    os.makedirs(session_dir, exist_ok=True)
    
    # Create the history file path
    history_path = os.path.join(session_dir, "messages.json")
    return FileChatMessageHistory(history_path)


def format_messages(messages: List[BaseMessage]) -> str:
    """Format messages for display or use in prompts."""
    formatted = []
    for message in messages:
        formatted.append(f"{message.type.capitalize()}: {message.content}")
    return "\n".join(formatted) 