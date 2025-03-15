import sys
import io
import traceback
from typing import Dict, Any
from crewai.tools import BaseTool

class PythonExecutorTool(BaseTool):
    """Tool for executing Python code."""
    
    name: str = "Python Executor"
    description: str = """Execute Python code and return the result.
Use this tool when you need to run Python code to process data, perform calculations, or automate tasks."""
    
    def _run(self, code: str) -> Dict[str, Any]:
        """
        Execute Python code and return the result.
        
        Args:
            code (str): The Python code to execute.
            
        Returns:
            Dict[str, Any]: The result of the code execution.
        """
        # Capture stdout and stderr
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        
        redirected_output = io.StringIO()
        redirected_error = io.StringIO()
        
        sys.stdout = redirected_output
        sys.stderr = redirected_error
        
        # Initialize return values
        result = None
        success = True
        error_msg = ""
        
        try:
            # Create a local environment for execution
            local_vars = {}
            
            # Execute the code
            exec(code, None, local_vars)
            
            # Check if there's a result variable
            if 'result' in local_vars:
                result = local_vars['result']
                
        except Exception as e:
            success = False
            error_msg = str(e)
            traceback.print_exc()
            
        finally:
            # Restore stdout and stderr
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            
        # Get the output and error messages
        output = redirected_output.getvalue()
        error = redirected_error.getvalue()
        
        return {
            "success": success,
            "result": result,
            "stdout": output,
            "stderr": error,
            "error_message": error_msg
        } 