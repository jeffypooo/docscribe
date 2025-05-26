"""
Command-line interface for Docscribe.

This module provides the main CLI entry point for the Docscribe package.
"""

import asyncio
import sys
from .core import DocscribeConfig, run_docscribe_and_save


def get_url_and_topic_from_args() -> tuple[str, str]:
    """
    Parse URL and topic from command line arguments (legacy format).
    
    Returns:
        Tuple of (url, topic)
    """
    if len(sys.argv) < 3:
        print("Usage: python -m docscribe <url> <topic>")
        print("   or: python main.py <url> <topic>")
        sys.exit(1)
    
    url = sys.argv[1]
    topic = sys.argv[2]
    
    if not url or not topic:
        print("Usage: python -m docscribe <url> <topic>")
        print("   or: python main.py <url> <topic>")
        sys.exit(1)
    
    return url, topic


async def legacy_main() -> None:
    """
    Legacy main function that maintains compatibility with the original main.py interface.
    """
    try:
        url, topic = get_url_and_topic_from_args()
        
        # Prompt for filename
        filename = input("Enter a filename for the guide: ").strip()
        if not filename:
            filename = None
        
        config = DocscribeConfig(
            url=url,
            topic=topic,
            output_file=filename
        )
        
        await run_docscribe_and_save(config)
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1) 