import asyncio
import sys
import os
import logging
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, trace, Runner, ModelSettings
import tools.scraper as scraper

AGENT_NAME = "Docscribe"
AGENT_INSTRUCTIONS = """
You are a documentation scraping agent. You are given a base URL for a documentation website.
You will scrape the website provided by the user and build a comprehensive programming guide for the given SDK, library, framework, or platform.
Your guide should be written in markdown format, with pleasant formatting.
Your guide should include:
- A clear explanation of the SDK, library, framework, or platform, including which version is the latest.
- Comprehensive examples of how to use the SDK, library, framework, or platform. Don't hold back on the examples.
- At the end of the guide, you will include a list of links to more information about the SDK, library, framework, or platform.
"""
AGENT_MODEL = "o3"

RUN_INPUT = """
Scrape the documentation at {url} and build a comprehensive programming guide for the given SDK, library, framework, or platform.
Focus on the following topic: {topic}.
Follow links you find that are relevant to the documentation and the topic (e.g. relative paths, links to other pages on the same domain, etc.).
"""

# Uncomment to enable debug logging
# logging.getLogger("openai.agents").setLevel(logging.DEBUG)
# logging.getLogger("openai.agents").addHandler(logging.StreamHandler())

async def run_docscribe(url: str, topic: str) -> str:
        with trace("docscribe agent"):
            agent = Agent(
                name=AGENT_NAME,
                instructions=AGENT_INSTRUCTIONS,
                tools=[scraper.tool()],
                model=AGENT_MODEL,
                model_settings=ModelSettings(truncation="auto"),
            )
            result = await Runner.run(
                starting_agent=agent, 
                input=RUN_INPUT.format(url=url, topic=topic),
                max_turns=100,
            )
            return result.final_output

def check_openai_api_key() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY is not set")
        sys.exit(1)

def get_url_and_topic_from_args() -> tuple[str, str]:
    if len(sys.argv) < 3:
        print("Usage: python main.py <url> <topic>")
        sys.exit(1)
    url = sys.argv[1]
    topic = sys.argv[2]
    if not url:
        print("Usage: python main.py <url> <topic>")
        sys.exit(1)
    if not topic:
        print("Usage: python main.py <url> <topic>")
        sys.exit(1)
    if not url.startswith("http"):
        url = f"https://{url}"
    return url, topic

async def main():
    check_openai_api_key()
    url, topic = get_url_and_topic_from_args()
    result = await run_docscribe(url, topic)
    filename = input("Enter a filename for the guide: ")
    # remove any .md if the user includes it
    if filename.endswith(".md"):
        filename = filename[:-3]
    with open(f"{filename}.md", "w") as f:
        f.write(result)


if __name__ == "__main__":
    asyncio.run(main())