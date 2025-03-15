import asyncio
import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.config import Config
from src.agents import AgentFactory
from src.flow import PlanningFlow

async def main():
    """Example of using the planning flow for complex tasks."""
    # Initialize configuration
    config = Config.from_yaml()
    
    # Create agents using factory
    planner = AgentFactory.create_agent("planning", config, verbose=True).agent
    developer = AgentFactory.create_agent("swe", config, verbose=True).agent
    
    # Create a planning flow
    planning_flow = PlanningFlow(
        planner=planner,
        executors=[developer],
        name="Software Planning Flow"
    )
    
    # Set the task context
    planner.task = """
    Create a detailed plan for developing a web scraper application that:
    1. Extracts product information from e-commerce websites
    2. Stores the data in a structured format
    3. Provides a simple API to query the data
    
    The plan should consider:
    - Different e-commerce website structures
    - Rate limiting and ethical scraping practices
    - Data storage options
    - Error handling and robustness
    """
    
    # Set the executor's task
    developer.task = """
    Based on the plan provided, implement the core components of the web scraper.
    Focus on creating a modular and extensible design that can be easily adapted to 
    different websites.
    """
    
    # Run the flow
    print("Starting the planning flow...")
    result = await planning_flow.run()
    
    print("\n\nFlow Results:")
    
    # Print the plan
    print("\n--- Plan ---")
    print(result.get("plan", "No plan generated"))
    
    # Print the execution results
    print("\n--- Execution Results ---")
    for i, exec_result in enumerate(result.get("execution_results", [])):
        print(f"\nExecutor {i+1} Result:")
        print(exec_result)

if __name__ == "__main__":
    asyncio.run(main()) 