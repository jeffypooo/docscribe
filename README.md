# Docscribe

A documentation scraping agent that generates markdown programming guides focused on a topic.

## Features

- Scrapes documentation websites using smart-ish web scraping
- Generates  programming guides in Markdown format
- Configurable AI model and scraping parameters
- Can be run as a Python module or installed as a command-line tool

## Installation

### From Source

```bash
# Clone the repository
git clone <repository-url>
cd docscribe

# Install dependencies
pip install -r requirements.txt

# Install the package in development mode
pip install -e .
```

## Usage

### As a Python Module

The recommended way to run Docscribe is as a Python module:

```bash
# Basic usage
python -m docscribe <url> <topic>

# With output file
python -m docscribe https://docs.python.org/3/ "async programming" -o python_async_guide

# With additional options
python -m docscribe fastapi.tiangolo.com "API development" --debug --max-turns 50 -o fastapi_guide
```

### Command Line Options

- `url`: The base URL of the documentation website to scrape
- `topic`: The specific topic to focus on when generating the guide
- `-o, --output`: Output filename for the generated guide (without .md extension)
- `--model`: The AI model to use (default: o3)
- `--max-turns`: Maximum number of agent turns (default: 100)
- `--debug`: Enable debug logging

### As an Installed Command

If you've installed the package, you can also use the `docscribe` command:

```bash
docscribe https://docs.python.org/3/ "async programming" -o python_guide
```

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Required. Your OpenAI API key for accessing the AI models.

## Requirements

- Python 3.8+
- OpenAI API key

## License

MIT License 