"""
Logging utilities for the crewai_learning package.

This module provides a centralized logging configuration using Loguru,
with support for different logging levels, file output, and structured
formatting.
"""

import os
import sys
from loguru import logger


# Default logging format
DEFAULT_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Remove default handler
logger.remove()

# Add console handler with custom format
logger.add(
    sys.stderr,
    format=DEFAULT_FORMAT,
    level="INFO",
    backtrace=True,
    diagnose=True,
)

# Add file handler for more detailed logging
logger.add(
    "logs/crewai_learning.log",
    rotation="10 MB",
    retention="1 week",
    compression="zip",
    format=DEFAULT_FORMAT,
    level="DEBUG",
    backtrace=True,
    diagnose=True,
)


def get_logger(name: str):
    """
    Get a logger with the specified name.
    
    Args:
        name: The logger name, typically the module name (__name__)
        
    Returns:
        A configured logger instance
    """
    return logger.bind(name=name)


__all__ = ["logger", "get_logger"] 