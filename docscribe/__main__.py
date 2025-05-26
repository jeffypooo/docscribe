"""
Entry point for running Docscribe as a module.

Usage:
    python -m docscribe <url> <topic> [options]
"""

import asyncio
import sys
import argparse
from typing import Optional

from .core import DocscribeConfig, run_docscribe_and_save


def parse_args() -> DocscribeConfig:
    """Parse command line arguments and return a DocscribeConfig."""
    parser = argparse.ArgumentParser(
        description="Docscribe - A documentation scraping agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python -m docscribe https://docs.python.org/3/ "async programming"
    python -m docscribe fastapi.tiangolo.com "API development" -o fastapi_guide
    python -m docscribe docs.openai.com "GPT models" --debug --max-turns 50
        """
    )
    
    parser.add_argument(
        "url",
        help="The base URL of the documentation website to scrape"
    )
    
    parser.add_argument(
        "topic",
        help="The specific topic to focus on when generating the guide"
    )
    
    parser.add_argument(
        "-o", "--output",
        dest="output_file",
        help="Output filename for the generated guide (without .md extension)"
    )
    
    parser.add_argument(
        "--model",
        default="o3",
        help="The model to use for the agent (default: o3)"
    )
    
    parser.add_argument(
        "--max-turns",
        type=int,
        default=100,
        help="Maximum number of turns for the agent (default: 100)"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )
    
    args = parser.parse_args()
    
    # If no output file specified, prompt for one
    output_file = args.output_file
    if not output_file:
        output_file = input("Enter a filename for the guide (without .md extension): ").strip()
        if not output_file:
            print("No filename provided. Guide will not be saved to file.")
            output_file = None
    
    return DocscribeConfig(
        url=args.url,
        topic=args.topic,
        model=args.model,
        max_turns=args.max_turns,
        debug=args.debug,
        output_file=output_file
    )


async def main() -> None:
    """Main entry point for the module."""
    try:
        config = parse_args()
        result = await run_docscribe_and_save(config)
        
        if not config.output_file:
            print("\n" + "="*50)
            print("GENERATED GUIDE:")
            print("="*50)
            print(result)
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


def sync_main() -> None:
    """Synchronous wrapper for the main function for console script entry point."""
    asyncio.run(main())


if __name__ == "__main__":
    sync_main() 