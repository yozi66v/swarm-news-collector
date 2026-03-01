import os
import sys
import json
from datetime import date
from pathlib import Path
from dotenv import load_dotenv
import anthropic

from news_reader.agent import run_agent as collect_news_agent

load_dotenv()


def _resolve_output_dir() -> Path:
    raw = os.getenv("NEWS_OUTPUT_DIR")
    if not raw:
        raise ValueError("NEWS_OUTPUT_DIR not set in environment. Check your .env file.")
    path = Path(raw).expanduser().resolve()
    path.mkdir(parents=True, exist_ok=True)
    return path


def _safe_path(output_dir: Path, filename: str) -> Path:
    """Resolve filename within output_dir, raising on path traversal attempts."""
    target = (output_dir / filename).resolve()
    if not str(target).startswith(str(output_dir) + os.sep) and target != output_dir:
        raise ValueError(f"Path traversal detected: '{filename}' escapes the output directory.")
    return target


def _today_filename() -> str:
    return f"{date.today().isoformat()}_news.md"


# ── Tool definitions ────────────────────────────────────────────────────────

TOOLS = [
    {
        "name": "collect_news",
        "description": (
            "Call the news_reader agent to search the web for a topic and return "
            "a prose summary of the most recent and relevant results."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "The news topic or search query.",
                }
            },
            "required": ["topic"],
        },
    },
    {
        "name": "read_file",
        "description": "Read the contents of a file inside the output directory.",
        "input_schema": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "Filename relative to the output directory.",
                }
            },
            "required": ["filename"],
        },
    },
    {
        "name": "write_file",
        "description": "Write (or overwrite) a file inside the output directory.",
        "input_schema": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "Filename relative to the output directory.",
                },
                "content": {
                    "type": "string",
                    "description": "Full markdown content to write.",
                },
            },
            "required": ["filename", "content"],
        },
    },
]


# ── Tool dispatcher ──────────────────────────────────────────────────────────

def dispatch_tool(name: str, tool_input: dict, output_dir: Path) -> str:
    if name == "collect_news":
        topic = tool_input["topic"]
        print(f"  [collect_news] Searching: {topic}")
        return collect_news_agent(topic)

    if name == "read_file":
        target = _safe_path(output_dir, tool_input["filename"])
        if not target.exists():
            return ""
        print(f"  [read_file] {target}")
        return target.read_text(encoding="utf-8")

    if name == "write_file":
        target = _safe_path(output_dir, tool_input["filename"])
        content = tool_input["content"]
        print(f"  [write_file] {target} ({len(content)} chars)")
        target.write_text(content, encoding="utf-8")
        return f"Written {len(content)} characters to {target.name}."

    raise ValueError(f"Unknown tool: {name}")


# ── Agent loop ───────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """\
You are a news curation agent. Your job:
1. Call collect_news to gather recent news on the requested topic.
2. Call read_file to load today's existing news file (if it exists).
3. Merge the new findings with any existing entries:
   - Remove duplicate or near-duplicate stories.
   - Keep only the BEST 12 news items for the day, ranked by relevance and significance.
4. Call write_file to save the updated markdown file.

Format rules for the markdown file:
- Start with a level-1 heading: "# News – <ISO date>"
- Each news item is a level-2 heading with the story title, followed by a short paragraph summary and a source URL if available.
- Keep the tone concise and factual.
"""


def run_agent(topic: str) -> None:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in environment. Check your .env file.")

    output_dir = _resolve_output_dir()
    today_file = _today_filename()

    client = anthropic.Anthropic(api_key=api_key)
    messages = [
        {
            "role": "user",
            "content": (
                f"Today is {date.today().isoformat()}. "
                f"Collect news about '{topic}', merge with any existing entries in "
                f"'{today_file}', keep the best 12, and save the result."
            ),
        }
    ]

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages,
        )

        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            tool_results = []
            for block in response.content:
                if block.type != "tool_use":
                    continue
                try:
                    result = dispatch_tool(block.name, block.input, output_dir)
                except Exception as exc:
                    result = f"ERROR: {exc}"
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result,
                })
            messages.append({"role": "user", "content": tool_results})
        else:
            text = next((b.text for b in response.content if b.type == "text"), "")
            if text:
                print(text)
            break


def main():
    topic = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "artificial intelligence"
    print(f"File writer agent — topic: {topic}\n")
    run_agent(topic)


if __name__ == "__main__":
    main()
