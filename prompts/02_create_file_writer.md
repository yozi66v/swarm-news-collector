# create the file writer agent

We already have the news_reader agent. 

Create a similar file_writer agent that can call the news_reader agent to 
collect news and writes the summaries of the most relevant news into a 
markdown file. Take the name of the directory to write to 
from the environment. The name of the file written should include or start
with the current date. 
Running the agent several times a day should update the file of the day,
taking care for consistence and to avoid repetitions. Keep just the best 
dozen of news for one day.

Add a file writer tool for the agent. 
The file writer tool should be protected against path traversal. 

# results

Done. Here's the new file:

src/news_reader/file_writer.py

The agent has three tools:

1. collect_news: Calls news_reader.agent.run_agent to search & summarize
2. read_file: Reads the existing day file from NEWS_OUTPUT_DIR
3. write_file: Writes the updated file — path traversal protected via
   `Path.resolve()`

Path traversal protection (file_writer.py:27-31): the resolved target path must start with the resolved output directory, otherwise an error is raised before any I/O.

Day-file logic: Claude is instructed via system prompt to read the existing file, merge with new results, deduplicate, keep the best 12, and write back — so running it multiple times a day just updates the same `2026-03-01_news.md`.

Setup:

1. Add to your .env:
```
NEWS_OUTPUT_DIR=~/news
```

2. Reinstall to register the new script:
```
pip install -e .
```

3 Run:
```
news-writer "artificial intelligence"
news-writer "open source software"
```
