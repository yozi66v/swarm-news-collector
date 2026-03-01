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

## adjust the project

Create an src folder and move the agent into the news_reader package. 
Later we will have other agents for publishing the summary of the collected news.

Done. The new structure is:
```
news-collector/
├── src/
│   └── news_reader/
│       ├── __init__.py
│       └── agent.py
├── .env.example
├── .gitignore
├── pyproject.toml
└── README.md
```

## debug

(.venv) yozi@deb13:~/swarm/news-collector$ news-reader
Agent searching for: latest AI news

Searching for: latest AI news
/home/yozi/swarm/news-collector/src/news_reader/agent.py:32: RuntimeWarning: This package (`duckduckgo_search`) has been renamed to `ddgs`! Use `pip install ddgs` instead.

Now reinstall to swap the package:
```
pip install ddgs && pip uninstall duckduckgo-search -y && pip install -e .
```

Agent searching for: latest AI news

Searching for: latest AI news
Impersonate 'safari_17.4.1' does not exist, using 'random'
Here's a summary of the latest AI news based on the search results:

---

### 🤖 Latest AI News Summary

1. **AI-Driven Business Growth** *(Artificial Intelligence News)*
The AI industry continues to push forward with the latest updates in **machine learning, deep learning, enterprise AI**, and other emerging technologies. Businesses worldwide are increasingly adopting AI to drive growth and innovation.

2. **AI in Tech & Ethics** *(TechCrunch)*
TechCrunch is actively covering news around **AI and machine learning technologies**, the companies developing them, and the **ethical issues** that AI raises in today's world — a hot topic as AI becomes more embedded in everyday life.

3. **AI Breakthroughs in Robotics & More** *(AI News YouTube)*
The AI News channel is reporting on the latest **breakthroughs in AI, machine learning, deep learning, brain-computer interfaces, and robotics**, highlighting how rapidly these futuristic technologies are advancing.

4. **Google's AI Initiatives** *(Google Blog)*
Google recently made headlines with **new global partnerships and funding announcements** at the **AI Impact Summit in India**, signaling its continued commitment to expanding AI's positive impact around the world.

5. **AI in the Federal Government** *(Federal News Network)*
The U.S. federal government is actively working on **incorporating AI** across various agencies and departments, with ongoing efforts to explore the full spectrum of AI applications in public service.

---

### 🔑 Key Takeaways:
- AI is rapidly evolving across **enterprise, robotics, and government** sectors.
- **Ethical concerns** around AI remain a major discussion point.
- Major players like **Google** are making significant global investments in AI.
- **Brain-computer interfaces and deep learning** are among the cutting-edge frontiers being explored.

Would you like me to dive deeper into any specific topic? 😊
