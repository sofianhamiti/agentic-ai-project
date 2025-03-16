"""
Simple adapter for LangChain tools in CrewAI.
"""

from crewai.tools import BaseTool
from langchain_core.tools import BaseTool as LangChainBaseTool


def adapt_tool(lc_tool: LangChainBaseTool) -> BaseTool:
    """Convert a LangChain tool to a CrewAI tool.
    
    Args:
        lc_tool: LangChain tool to adapt
        
    Returns:
        CrewAI-compatible tool
    """
    return BaseTool(
        name=getattr(lc_tool, "name", lc_tool.__class__.__name__),
        description=getattr(lc_tool, "description", ""),
        _run=lambda query: lc_tool.invoke(query)
    ) 