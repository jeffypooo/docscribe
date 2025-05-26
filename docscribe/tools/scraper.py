from typing import Any
import sys
import httpx
from bs4 import BeautifulSoup
from pydantic import BaseModel, ConfigDict, Field

from agents import RunContextWrapper, FunctionTool

_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"

class ScrapeWebsiteArgs(BaseModel):
    url: str = Field(description="The URL of the website to scrape.")
    model_config = ConfigDict(extra="forbid")

class ScrapeWebsiteResult(BaseModel):
    error: str | None = Field(description="An error message if the website could not be scraped.")
    text_content: str = Field(description="The text content from the HTML of the website.")
    links: list[str] = Field(description="A list of links from the page.")
    model_config = ConfigDict(extra="forbid")

async def scrape_website(url: str) -> str:
    print(f"> Scraping {url}")
    async with httpx.AsyncClient(follow_redirects=True, http2=True, headers={"User-Agent": _USER_AGENT}) as client:
        response = await client.get(url)
    # handle errors
    if response.status_code != 200:
        print(f"> Failed to scrape {url}: status code {response.status_code}", file=sys.stderr)
        return ScrapeWebsiteResult(
            error=f"Failed to scrape {url}: status code {response.status_code}",
            text_content="",
            links=[],
        )
    soup = BeautifulSoup(response.text, "lxml")
    anchors = soup.find_all("a")
    links = [anchor.get("href") for anchor in anchors if anchor.get("href") is not None]
    text_content = soup.get_text()
    if not text_content:
        text_content = "No text content found"
    if not links:
        links = []
    return ScrapeWebsiteResult(
        error=None,
        text_content=text_content,
        links=links,
    )

async def run_function(ctx: RunContextWrapper[Any], args: str) -> str:
    args = ScrapeWebsiteArgs.model_validate_json(args)
    context = await scrape_website(args.url)
    return context.model_dump_json()

def tool() -> FunctionTool:
    return FunctionTool(
        name="scrape_website",
        description="Scrape the HTML content of a website.",
        params_json_schema=ScrapeWebsiteArgs.model_json_schema(),
        on_invoke_tool=run_function,
    )
