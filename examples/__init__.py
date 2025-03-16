"""
Helper module for examples.

This __init__.py file adds the project root to the Python path,
allowing example scripts to import from the src package without
each file needing to modify sys.path.
"""
import os
import sys

# Add project root to path once, here in the __init__
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root) 