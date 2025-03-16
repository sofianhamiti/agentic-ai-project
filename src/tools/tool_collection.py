from typing import Dict, List, Optional, Type, Any
from crewai.tools import BaseTool

class ToolCollection:
    """
    A collection of tools that can be used by agents.
    
    This class provides a way to organize and manage multiple tools,
    making it easier to pass collections of tools to agents and
    perform operations on groups of tools.
    """
    
    def __init__(self, *tools: BaseTool):
        """
        Initialize the tool collection with a set of tools.
        
        Args:
            *tools: Variable number of tool instances to add to the collection
        """
        self.tool_map: Dict[str, BaseTool] = {}
        for tool in tools:
            self.add_tool(tool)
    
    def add_tool(self, tool: BaseTool) -> None:
        """
        Add a tool to the collection.
        
        Args:
            tool: The tool instance to add
        """
        self.tool_map[tool.name] = tool
    
    def get_tool(self, tool_name: str) -> Optional[BaseTool]:
        """
        Get a tool from the collection by name.
        
        Args:
            tool_name: The name of the tool to retrieve
            
        Returns:
            The tool instance if found, None otherwise
        """
        return self.tool_map.get(tool_name)
    
    def remove_tool(self, tool_name: str) -> None:
        """
        Remove a tool from the collection by name.
        
        Args:
            tool_name: The name of the tool to remove
        """
        if tool_name in self.tool_map:
            del self.tool_map[tool_name]
    
    def get_all_tools(self) -> List[BaseTool]:
        """
        Get all tools in the collection.
        
        Returns:
            A list of all tool instances in the collection
        """
        return list(self.tool_map.values())
    
    def get_tool_names(self) -> List[str]:
        """
        Get the names of all tools in the collection.
        
        Returns:
            A list of all tool names in the collection
        """
        return list(self.tool_map.keys())
    
    def __contains__(self, tool_name: str) -> bool:
        """
        Check if a tool is in the collection.
        
        Args:
            tool_name: The name of the tool to check
            
        Returns:
            True if the tool is in the collection, False otherwise
        """
        return tool_name in self.tool_map 