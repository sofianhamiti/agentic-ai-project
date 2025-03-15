import asyncio
import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.config import Config
from src.agents import AgentFactory

async def main():
    """Example of using the SWE agent for software development tasks."""
    # Initialize configuration
    config = Config.from_yaml()
    
    # Create SWE agent using factory
    swe_agent = AgentFactory.create_agent("swe", config, verbose=True)
    
    # Define requirements for a simple task
    requirements = """
    Create a simple Python program that:
    1. Reads data from a CSV file containing sales records with columns: date, product_id, quantity, price
    2. Calculates total sales by product
    3. Identifies the top 3 selling products
    4. Generates a summary report and saves it to a file
    
    The program should handle basic error cases and include docstrings.
    """
    
    # Let the agent develop the solution
    print("Starting development task...")
    result = await swe_agent.develop_solution(requirements)
    
    print("\n\nDevelopment Result:")
    print(result)
    
    # Example of code review
    code_to_review = """
    def calculate_average(numbers):
        total = 0
        for num in numbers:
            total += num
        return total / len(numbers)
    
    def main():
        data = [1, 2, 3, 4, 5]
        avg = calculate_average(data)
        print(f"The average is: {avg}")
        
        # This will cause an error
        empty_data = []
        avg2 = calculate_average(empty_data)
        print(f"The average of empty data is: {avg2}")
    
    if __name__ == "__main__":
        main()
    """
    
    print("\n\nStarting code review task...")
    review_result = await swe_agent.review_code(code_to_review)
    
    print("\n\nCode Review Result:")
    print(review_result)

if __name__ == "__main__":
    asyncio.run(main()) 