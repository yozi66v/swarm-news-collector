# prompts

This file contains the prompts used for generating this project. The new prompts are on the top of the file.

# Create the project

Set up a python project for agentic AI. 
Start with a simple AI agent that reads the Anthropic key from the .env file 
and searches the web using the free DuckDuckGo API for the search term 
and summarizes and prints the results. 

The project is set up. Here's the structure:
```
news-collector/
├── .env.example          # Template for your API key
├── .gitignore            # Excludes .env, .venv, __pycache__
├── pyproject.toml        # Project config + dependencies
└── news_collector/
    ├── __init__.py
    └── agent.py          # The agent
```

To get started:


1. Create and activate a virtual environment
```
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies
```
pip install -e .
```

3. Set up your API key
```
cp .env.example .env
```
Edit .env and add your ANTHROPIC_API_KEY

4. Run the agent
```0
python -m news_collector.agent "latest AI news"
```
or with the installed script:
```
news-collector "latest AI news"
```
