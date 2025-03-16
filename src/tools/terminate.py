from typing import Dict, Any
from crewai.tools import BaseTool

class TerminateTool(BaseTool):
    """
    A tool for gracefully ending agent execution when a task is complete.
    
    This tool allows agents to signal that they have completed their task
    and should stop execution, optionally providing a final result.
    """
    
    name: str = "Terminate"
    description: str = """
    Use this tool when you have completed the task and want to end execution.
    Provide a final message or result that should be returned to the user.
    """
    
    def _run(self, reason: str, final_result: str = "") -> str:
        """
        Execute the termination.
        
        Args:
            reason: The reason for terminating execution
            final_result: The final result or message to return (optional)
            
        Returns:
            A message indicating successful termination
        """
        result = final_result if final_result else "Task completed successfully."
        return f"TASK_TERMINATED: {reason}\n\nFinal result: {result}"
    
    def is_termination_signal(self, result: str) -> bool:
        """
        Check if a result string contains a termination signal.
        
        Args:
            result: The result string to check
            
        Returns:
            True if the result contains a termination signal, False otherwise
        """
        return result.startswith("TASK_TERMINATED:")
    
    def extract_final_result(self, result: str) -> str:
        """
        Extract the final result from a termination signal.
        
        Args:
            result: The termination signal string
            
        Returns:
            The final result extracted from the termination signal
        """
        if not self.is_termination_signal(result):
            return result
            
        parts = result.split("\n\n")
        if len(parts) < 2:
            return ""
            
        final_part = parts[1]
        if final_part.startswith("Final result: "):
            return final_part[14:]  # Remove "Final result: " prefix
            
        return final_part 