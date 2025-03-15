from typing import Optional, Any, Type
from .base import BaseTool

class ToolFactory:
    """Factory for creating various types of tools."""
    
    @staticmethod
    def create_tool(tool_type: str, **kwargs) -> Any:
        """
        Create a tool of the specified type.
        
        Args:
            tool_type: Type of tool to create (e.g., "web_search", "bash", "file_saver", etc.)
            **kwargs: Additional arguments to pass to the tool constructor
            
        Returns:
            An instance of the requested tool type
            
        Raises:
            ValueError: If the tool type is unknown
        """
        if tool_type == "web_search":
            from .web_search import WebSearchTool
            return WebSearchTool(**kwargs)
        elif tool_type == "bash":
            from .bash import BashTool
            return BashTool(**kwargs)
        elif tool_type == "terminal":
            from .terminal import TerminalTool
            return TerminalTool(**kwargs)
        elif tool_type == "file_saver":
            from .file_saver import FileSaverTool
            return FileSaverTool(**kwargs)
        elif tool_type == "python_executor":
            from .python_executor import PythonExecutorTool
            return PythonExecutorTool(**kwargs)
        elif tool_type == "planning":
            from .planning import PlanningTool
            return PlanningTool(**kwargs)
        elif tool_type == "task_breakdown":
            from .planning import TaskBreakdownTool
            return TaskBreakdownTool(**kwargs)
        elif tool_type == "browser":
            from .browser import BrowserUseTool
            return BrowserUseTool(**kwargs)
        elif tool_type == "email_analysis":
            from .email_analysis import EmailAnalysisTool
            return EmailAnalysisTool(**kwargs)
        elif tool_type == "email_improvements":
            from .email_analysis import SuggestEmailImprovementsTool
            return SuggestEmailImprovementsTool(**kwargs)
        else:
            raise ValueError(f"Unknown tool type: {tool_type}")
    
    @staticmethod
    def list_available_tools() -> list[str]:
        """List all available tool types."""
        return [
            "web_search",
            "bash",
            "terminal",
            "file_saver",
            "python_executor",
            "planning",
            "task_breakdown",
            "browser",
            "email_analysis",
            "email_improvements"
        ] 