"""
Example demonstrating the use of the MainAgent.

This script shows how to create and use the MainAgent for research tasks.
"""

# Simple path setup for local development
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents.factory import AgentFactory
from src.tools.factory import ToolFactory


def main():
    """Run the MainAgent example."""
    print("Starting MainAgent demonstration...")
    
    # Prompt the user for a research topic
    research_topic = input("Enter a research topic: ")
    
    # Create a MainAgent
    agent = AgentFactory.create_agent("main_agent", verbose=True)
    
    # Define the research task
    task_description = f"""
    Conduct comprehensive research on: {research_topic}
    
    Your task is to:
    1. Gather information from multiple sources
    2. Verify facts from different websites
    3. Organize your findings in a clear, structured format
    4. Include relevant statistics, data, and facts
    5. Provide a well-structured summary with sections and subsections
    
    Ensure your research is thorough and accurate.
    """
    
    # Execute the task directly
    result = agent.execute_task(task_description)
    
    # Print the result
    print("\n=== RESEARCH RESULTS ===\n")
    print(result)
    print("\n=== END OF RESULTS ===\n")
    
    return result


if __name__ == "__main__":
    main() 