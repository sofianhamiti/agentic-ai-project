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
│   ├── agents/          # Agent definitions including specialized agents
│   │   ├── base_agent.py       # Base agent implementation
│   │   ├── browser_agent.py    # Web browsing agent
│   │   ├── email_reviewer_agent.py # Email analysis agent
│   │   ├── planning_agent.py   # Planning and task agent
│   │   ├── researcher_agent.py # Research-focused agent
│   │   └── swe_agent.py        # Software engineering agent
│   ├── core/            # Core functionality and configurations
│   ├── flow/            # Workflow management
│   │   ├── base_flow.py        # Base flow implementation
│   │   └── planning_flow.py    # Planning workflow
│   └── tools/           # Custom tools for agent use
│       ├── base.py             # Base tool class
│       ├── bash.py             # Bash command execution
│       ├── browser.py          # Browser automation
│       ├── email_analysis.py   # Email review tools
│       ├── file_saver.py       # File I/O operations
│       ├── planning.py         # Planning tools
│       ├── python_executor.py  # Python code execution
│       ├── terminal.py         # Terminal commands
│       └── web_search.py       # Web search capabilities
├── examples/            # Usage examples
├── config/              # Configuration files
├── requirements.txt     # Project dependencies
└── pyproject.toml       # Project metadata
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

3. Install dependencies (choose one option):

   Option A: Using requirements.txt:
   ```bash
   pip install -r requirements.txt
   ```

   Option B: Using pyproject.toml (requires pip 21.3+):
   ```bash
   pip install -e .
   ```

4. Install browser automation dependencies (if using browser features):
   - Chrome or Firefox browser
   - Appropriate WebDriver for your browser
   
5. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your AWS credentials for Bedrock
```

## Usage

Basic example of using the project:

```python
from src.agents import AgentFactory
from src.tools import ToolFactory
from src.core.config import Config

# Initialize configuration
config = Config.from_yaml()

# Create agents using factory
researcher = AgentFactory.create_agent("researcher", config=config)
email_reviewer = AgentFactory.create_agent("email_reviewer", config=config)

# Create tools
web_search_tool = ToolFactory.create_tool("web_search")

# Execute tasks with agents
research_results = researcher.research("Latest AI advancements in 2024", 
                                      tools=[web_search_tool])

email_content = """
Subject: Project Update
Hi Team,
Quick update on the AI integration project. We're behind schedule but should catch up soon.
Thanks,
Alex
"""

email_feedback = email_reviewer.review_email(email_content)
print(email_feedback)
```

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- Built with [CrewAI](https://github.com/joaomdmoura/crewAI)
- Powered by AWS Bedrock
