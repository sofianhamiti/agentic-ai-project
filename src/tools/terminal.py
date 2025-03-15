import os
import subprocess
import tempfile
from typing import Dict, Any
from crewai.tools import BaseTool

class TerminalTool(BaseTool):
    """Tool for executing more complex terminal operations."""
    
    name: str = "Terminal"
    description: str = """Interactive terminal for executing commands and managing processes.
Use this tool when you need to run complex shell commands, manage processes, or interact with the terminal.
It provides more context and flexibility than the basic bash command tool."""
    
    _sessions = {}  # Store terminal sessions
    
    def _run(self, command: str, session_id: str = "default", timeout: int = 60) -> Dict[str, Any]:
        """
        Execute a command in a terminal session.
        
        Args:
            command (str): The command to execute.
            session_id (str): A unique identifier for the terminal session.
            timeout (int): Maximum time in seconds to wait for the command to complete.
            
        Returns:
            Dict[str, Any]: The result of the command execution.
        """
        if not command:
            return {
                "success": False,
                "message": "No command provided",
                "output": "",
                "error": "Error: No command provided"
            }
            
        # Create session script file if it doesn't exist
        if session_id not in self._sessions:
            script_file = tempfile.NamedTemporaryFile(delete=False, prefix=f"terminal_{session_id}_", suffix=".sh")
            self._sessions[session_id] = {
                "script_file": script_file.name,
                "history": []
            }
            script_file.close()
            
            # Initialize script with shebang and basic setup
            with open(self._sessions[session_id]["script_file"], "w") as f:
                f.write("#!/bin/bash\n")
                f.write("set -e\n")  # Exit on error
                f.write("cd $(pwd)\n")  # Start in current directory
                
        # Add command to session history
        self._sessions[session_id]["history"].append(command)
        
        # Write command to script file
        with open(self._sessions[session_id]["script_file"], "a") as f:
            f.write(f"\n# Command: {command}\n")
            f.write(f"echo '> Executing: {command}'\n")
            f.write(f"{command}\n")
            
        try:
            # Execute the script
            result = subprocess.run(
                f"bash {self._sessions[session_id]['script_file']}",
                shell=True,
                text=True,
                capture_output=True,
                timeout=timeout
            )
            
            return {
                "success": result.returncode == 0,
                "message": "Command executed successfully" if result.returncode == 0 else f"Command failed with return code {result.returncode}",
                "output": result.stdout,
                "error": result.stderr,
                "session_id": session_id,
                "command_history": self._sessions[session_id]["history"]
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "message": f"Command timed out after {timeout} seconds",
                "output": "",
                "error": f"Error: Command '{command}' timed out after {timeout} seconds",
                "session_id": session_id,
                "command_history": self._sessions[session_id]["history"]
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error executing command: {str(e)}",
                "output": "",
                "error": f"Error: {str(e)}",
                "session_id": session_id,
                "command_history": self._sessions[session_id]["history"]
            } 