"""
CrewAI Learning Project

A modern agent-based AI project built with CrewAI, designed to demonstrate and 
implement autonomous AI agents working together to solve complex tasks.
"""

# Import submodules to make them available through src
from . import agents
from . import tools
from . import flow
from . import core
from . import models

# Export key modules
__all__ = [
    'agents',
    'tools',
    'flow',
    'core',
    'models',
]

# Version information
__version__ = '0.1.0'
