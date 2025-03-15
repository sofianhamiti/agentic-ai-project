import os
import subprocess
from typing import Dict, Any
from crewai.tools import BaseTool

class BashTool(BaseTool):
    """Tool for executing bash commands."""
    
    name: str = "Bash Command"
    description: str = """Execute a bash command in the terminal.
Use this tool when you need to run shell commands, like file operations, installs, or other system commands.
For long-running processes, consider using command & to run in background."""
    
    def _run(self, command: str, timeout: int = 60) -> Dict[str, Any]:
        """
        Execute a bash command.
        
        Args:
            command (str): The bash command to execute.
            timeout (int, optional): Maximum time in seconds to wait for the command to complete.
                                    Default is 60 seconds.
        
        Returns:
            Dict[str, Any]: The result of the command execution.
        """
        if not command:
            return {
                "success": False,
                "message": "No command provided",
                "stdout": "",
                "stderr": "Error: No command provided"
            }
            
        # Handle special case for Ctrl+C
        if command.lower() == "ctrl+c":
            return {
                "success": True,
                "message": "Ctrl+C signal sent",
                "stdout": "Process terminated",
                "stderr": ""
            }
            
        try:
            # Execute the command
            process = subprocess.run(
                command,
                shell=True,
                text=True,
                capture_output=True,
                timeout=timeout
            )
            
            return {
                "success": process.returncode == 0,
                "returncode": process.returncode,
                "stdout": process.stdout,
                "stderr": process.stderr,
                "message": "Command executed successfully" if process.returncode == 0 else f"Command failed with return code {process.returncode}"
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "message": f"Command timed out after {timeout} seconds",
                "stdout": "",
                "stderr": f"Error: Command '{command}' timed out after {timeout} seconds"
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error executing command: {str(e)}",
                "stdout": "",
                "stderr": f"Error: {str(e)}"
            } 