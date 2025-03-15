import asyncio
from src.core.config import Config
from src.agents import AgentFactory
from src.tools import ToolFactory

async def main():
    # Initialize configuration from YAML
    config = Config.from_yaml()
    
    # Validate configuration
    config.validate()
    
    # Create researcher agent using the factory
    researcher = AgentFactory.create_agent("researcher", config=config)
    
    # Create web search tool
    web_search_tool = ToolFactory.create_tool("web_search")
    
    # Define research topic
    topic = "Latest developments in AI agents and autonomous systems in 2024"
    
    print(f"Starting research on: {topic}")
    print("-" * 50)
    
    # Execute research
    try:
        results = await researcher.research(topic, tools=[web_search_tool])
        print("\nResearch Results:")
        print("-" * 50)
        print(results)
    except Exception as e:
        print(f"Error during research: {str(e)}")

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main()) 