import os
from typing import Dict, Any
from crewai.tools import BaseTool

class FileSaverTool(BaseTool):
    """Tool for saving content to a file."""
    
    name: str = "File Saver"
    description: str = """Save content to a local file at a specified path.
Use this tool when you need to save text, code, or generated content to a file on the local filesystem."""
    
    def _run(self, content: str, file_path: str, mode: str = "w") -> Dict[str, Any]:
        """
        Save content to a file at the specified path.
        
        Args:
            content (str): The content to save to the file.
            file_path (str): The path where the file should be saved.
            mode (str, optional): The file opening mode. Default is 'w' for write. Use 'a' for append.
            
        Returns:
            Dict[str, Any]: A message indicating the result of the operation.
        """
        try:
            # Ensure the directory exists
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
                
            # Write to the file
            with open(file_path, mode, encoding="utf-8") as file:
                file.write(content)
                
            return {
                "success": True,
                "message": f"Content successfully saved to {file_path}",
                "file_path": file_path
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error saving file: {str(e)}",
                "error": str(e)
            } 