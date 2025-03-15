import asyncio
from src.core.config import Config
from src.agents.specialized_agents.researcher_agent import ResearcherAgent

async def main():
    # Initialize configuration from YAML
    config = Config.from_yaml()
    
    # Validate configuration
    config.validate()
    
    # Create researcher agent
    researcher = ResearcherAgent(config)
    
    # Define research topic
    topic = "Latest developments in AI agents and autonomous systems in 2024"
    
    print(f"Starting research on: {topic}")
    print("-" * 50)
    
    # Execute research
    try:
        results = await researcher.research(topic)
        print("\nResearch Results:")
        print("-" * 50)
        print(results)
    except Exception as e:
        print(f"Error during research: {str(e)}")

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main()) 