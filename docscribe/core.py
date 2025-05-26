"""
Core functionality for the Docscribe documentation scraping agent.
"""

import asyncio
import os
import logging
from typing import Optional
from dataclasses import dataclass
from agents import Agent, trace, Runner, ModelSettings
from .tools import scraper

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


@dataclass
class DocscribeConfig:
    """Configuration for the Docscribe agent."""
    url: str
    topic: str
    model: str = AGENT_MODEL
    max_turns: int = 100
    debug: bool = False
    output_file: Optional[str] = None


def setup_logging(debug: bool = False) -> None:
    """Setup logging configuration."""
    if debug:
        logging.getLogger("openai.agents").setLevel(logging.DEBUG)
        logging.getLogger("openai.agents").addHandler(logging.StreamHandler())


def check_openai_api_key() -> None:
    """Check if OPENAI_API_KEY environment variable is set."""
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable is not set")


def normalize_url(url: str) -> str:
    """Normalize URL by adding https:// if no protocol is specified."""
    if not url.startswith(("http://", "https://")):
        return f"https://{url}"
    return url


async def run_docscribe(config: DocscribeConfig) -> str:
    """
    Run the Docscribe agent to scrape documentation and generate a guide.
    
    Args:
        config: Configuration object containing URL, topic, and other settings
        
    Returns:
        The generated documentation guide as a string
        
    Raises:
        ValueError: If OPENAI_API_KEY is not set
    """
    check_openai_api_key()
    setup_logging(config.debug)
    
    # Normalize the URL
    normalized_url = normalize_url(config.url)
    
    with trace("docscribe agent"):
        agent = Agent(
            name=AGENT_NAME,
            instructions=AGENT_INSTRUCTIONS,
            tools=[scraper.tool()],
            model=config.model,
            model_settings=ModelSettings(truncation="auto"),
        )
        result = await Runner.run(
            starting_agent=agent, 
            input=RUN_INPUT.format(url=normalized_url, topic=config.topic),
            max_turns=config.max_turns,
        )
        return result.final_output


def save_guide(content: str, filename: str) -> None:
    """
    Save the generated guide to a file.
    
    Args:
        content: The guide content to save
        filename: The filename (without extension) to save to
    """
    # Remove .md extension if provided
    if filename.endswith(".md"):
        filename = filename[:-3]
    
    filepath = f"{filename}.md"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Guide saved to: {filepath}")


async def run_docscribe_and_save(config: DocscribeConfig) -> str:
    """
    Run Docscribe and optionally save the result to a file.
    
    Args:
        config: Configuration object
        
    Returns:
        The generated guide content
    """
    result = await run_docscribe(config)
    
    if config.output_file:
        save_guide(result, config.output_file)
    
    return result 