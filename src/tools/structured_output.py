from typing import Any, Dict, List, Optional, Type, Union, get_args, get_origin
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

class StructuredOutputTool(BaseTool):
    """
    A tool that creates structured outputs based on a specified schema.
    
    This tool helps agents generate responses in specific formats,
    ensuring consistency and proper structure in the outputs.
    """
    
    name: str = "Structured Output"
    description: str = "Creates a structured response with specified output formatting"
    
    # Type mapping for JSON schema
    type_mapping: Dict[Type, str] = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        dict: "object",
        list: "array",
    }
    
    # Define output_schema as a field
    output_schema: Optional[Type[BaseModel]] = None
    
    def __init__(self, output_schema: Optional[Type[BaseModel]] = None):
        """
        Initialize the tool with an output schema.
        
        Args:
            output_schema: A Pydantic model class defining the expected output structure
        """
        super().__init__()
        if output_schema:
            self.output_schema = output_schema
        
    def _build_parameters(self) -> Dict[str, Any]:
        """
        Build a JSON schema based on the output schema.
        
        Returns:
            A dictionary representing the JSON schema for the output
        """
        if not self.output_schema:
            return {
                "type": "object",
                "properties": {
                    "response": {
                        "type": "string",
                        "description": "The response text that should be delivered to the user."
                    }
                },
                "required": ["response"]
            }
        
        schema = self.output_schema.model_json_schema()
        return {
            "type": "object",
            "properties": schema.get("properties", {}),
            "required": schema.get("required", [])
        }
        
    def _run(self, **kwargs) -> str:
        """
        Process the input and generate a structured output.
        
        Args:
            **kwargs: The input parameters for generating the structured output
            
        Returns:
            A structured output based on the provided schema
        """
        if not self.output_schema:
            return kwargs.get("response", "No response provided")
        
        try:
            # Validate the input against the schema
            validated_data = self.output_schema(**kwargs)
            return validated_data.model_dump_json()
        except Exception as e:
            return f"Error creating structured output: {str(e)}"
            
    def get_schema_description(self) -> str:
        """
        Get a human-readable description of the output schema.
        
        Returns:
            A string describing the expected output structure
        """
        if not self.output_schema:
            return "Simple text response"
            
        schema = self.output_schema.model_json_schema()
        fields = schema.get("properties", {})
        
        description = "Expected output structure:\n"
        for field_name, field_info in fields.items():
            field_type = field_info.get("type", "unknown")
            field_desc = field_info.get("description", "")
            description += f"- {field_name} ({field_type}): {field_desc}\n"
            
        return description 