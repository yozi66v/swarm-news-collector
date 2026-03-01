import os
import sys
import json
from dotenv import load_dotenv
import anthropic
from ddgs import DDGS

load_dotenv()

SEARCH_TOOL = {
    "name": "web_search",
    "description": "Search the web using DuckDuckGo and return a list of results.",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query",
            },
            "max_results": {
                "type": "integer",
                "description": "Maximum number of results to return (default: 5)",
                "default": 5,
            },
        },
        "required": ["query"],
    },
}


def web_search(query: str, max_results: int = 5) -> list[dict]:
    with DDGS() as ddgs:
        return list(ddgs.text(query, max_results=max_results))


def run_agent(search_term: str) -> str:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in environment. Check your .env file.")

    client = anthropic.Anthropic(api_key=api_key)
    messages = [
        {
            "role": "user",
            "content": f"Search the web for '{search_term}' and summarize the results.",
        }
    ]

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            tools=[SEARCH_TOOL],
            messages=messages,
        )

        if response.stop_reason == "tool_use":
            tool_use_block = next(b for b in response.content if b.type == "tool_use")
            tool_input = tool_use_block.input
            query = tool_input["query"]
            max_results = tool_input.get("max_results", 5)

            print(f"Searching for: {query}")
            results = web_search(query, max_results)

            messages.append({"role": "assistant", "content": response.content})
            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_use_block.id,
                        "content": json.dumps(results),
                    }
                ],
            })
        else:
            text_block = next((b for b in response.content if b.type == "text"), None)
            return text_block.text if text_block else ""


def main():
    search_term = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "latest AI news"
    print(f"Agent searching for: {search_term}\n")
    summary = run_agent(search_term)
    print(summary)


if __name__ == "__main__":
    main()
