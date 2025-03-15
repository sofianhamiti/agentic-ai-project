import asyncio
import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.config import Config
from src.agents import AgentFactory

async def main():
    """Example of using the Browser agent for web interactions."""
    # Initialize configuration
    config = Config.from_yaml()
    
    # Create Browser agent using factory
    browser_agent = AgentFactory.create_agent("browser", config, verbose=True)
    
    # Example 1: Browse a specific website
    browse_url = "https://news.ycombinator.com/"
    browse_task = "Find the top 3 most-discussed news articles on the front page and summarize them"
    
    print("Starting browsing task...")
    browse_result = await browser_agent.browse_website(browse_url, browse_task)
    
    print("\n\nBrowsing Result:")
    print(browse_result)
    
    # Example 2: Extract data from a website
    extract_url = "https://en.wikipedia.org/wiki/Artificial_intelligence"
    extract_description = "Extract the main definitions of AI, key areas of AI research, and important milestones in AI history"
    
    print("\n\nStarting data extraction task...")
    extraction_result = await browser_agent.extract_data(extract_url, extract_description)
    
    print("\n\nExtraction Result:")
    print(extraction_result)
    
    # Example 3: Research a topic
    research_topic = "Recent advancements in quantum computing"
    
    print("\n\nStarting research task...")
    research_result = await browser_agent.research_topic(research_topic, depth="medium")
    
    print("\n\nResearch Result:")
    print(research_result)

if __name__ == "__main__":
    asyncio.run(main()) 