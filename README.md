# CrewAI Learning Project

A modern agent-based AI project built with CrewAI, designed to demonstrate and implement autonomous AI agents working together to solve complex tasks.

## Features

- 🤖 Multiple specialized AI agents with distinct roles and capabilities
- 🛠 Extensible tool system for agent interactions
- 📝 Structured agent behaviors
- 🔄 Flexible workflow management

## Project Structure

```
crewai_learning/
├── src/
│   ├── agents/          # Agent definitions and behaviors
│   ├── core/            # Core functionality and configurations
│   ├── tools/           # Custom tools for agent use
│   └── models/          # Model implementations
├── examples/            # Usage examples
├── config/             # Configuration files
├── requirements.txt    # Project dependencies
└── pyproject.toml     # Project metadata
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/crewai_learning.git
cd crewai_learning
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your AWS credentials for Bedrock
```

## Usage

Basic example of using the project:

```python
from src.agents import ResearchAgent, AnalysisAgent
from src.core.config import Config

# Initialize configuration
config = Config.from_yaml()

# Create agents
researcher = ResearchAgent(config)
analyst = AnalysisAgent(config)

# Execute tasks
results = await researcher.research("AI trends 2024")
analysis = await analyst.analyze(results)
```

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- Built with [CrewAI](https://github.com/joaomdmoura/crewAI)
- Powered by AWS Bedrock
