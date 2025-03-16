import time
import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.config import Config
from src.agents import AgentFactory


def run_flow():
    """Main entry point for running agent flows based on user input."""
    # Initialize configuration
    config = Config.from_yaml()
    
    try:
        # Get user input
        print("\n===== CrewAI Learning Project =====")
        print("Enter your prompt, and our agents will work on it.")
        print("Type 'exit' to quit.\n")
        
        prompt = input("Enter your prompt: ")
        
        if prompt.lower() == 'exit':
            print("Exiting the application. Goodbye!")
            return
            
        if not prompt.strip():
            print("Empty prompt provided.")
            return
            
        # Get agent type
        agent_types = AgentFactory.list_available_agents()
        agent_type = "planning"  # Default to planning agent
        
        if len(sys.argv) > 1 and sys.argv[1] in agent_types:
            agent_type = sys.argv[1]
            
        # Create agent using factory
        agent = AgentFactory.create_agent(agent_type, config, verbose=True)
        
        print(f"Processing your request with the {agent_type} agent...")
        
        # Execute agent task with timeout
        try:
            start_time = time.time()
            result = agent.execute_task(prompt)
            elapsed_time = time.time() - start_time
            print(f"Request processed in {elapsed_time:.2f} seconds")
            print("\nResult:")
            print(result)
        except KeyboardInterrupt:
            print("Request processing timed out or was interrupted")
            print("Operation terminated. Please try a simpler request.")
            
    except KeyboardInterrupt:
        print("Operation cancelled by user.")
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_flow() 