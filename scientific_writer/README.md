# Scientific Writer Python Package

This folder contains a standalone Python package for programmatic scientific paper generation using the Claude Agent SDK.

## Purpose

Provides two entry points for using the scientific writer **outside of Claude Code**:

1. **CLI Tool** - Interactive terminal interface
2. **Python API** - Programmatic paper generation

## When to Use This

- **Working in Claude Code?** You don't need this package - use the skills and WRITER.md directly
- **Want a standalone CLI?** Run `scientific-writer` from terminal
- **Building automation?** Import `generate_paper()` in your Python code

## Usage

### CLI

```bash
# Install the package
uv sync

# Run the CLI
uv run scientific-writer
> Create a NeurIPS paper on transformer attention mechanisms
```

### Python API

```python
from scientific_writer import generate_paper

async for update in generate_paper("Create a Nature paper on CRISPR"):
    if update["type"] == "text":
        print(update["content"], end="")
    elif update["type"] == "result":
        print(f"Paper created: {update['paper_directory']}")
```

## Module Reference

| File | Purpose |
|------|---------|
| `__init__.py` | Package exports: `generate_paper`, data models |
| `api.py` | Async `generate_paper()` with streaming updates |
| `cli.py` | Interactive command-line interface |
| `core.py` | Helpers: API keys, skill setup, output folders |
| `models.py` | Data classes: `ProgressUpdate`, `PaperResult`, `TokenUsage` |
| `utils.py` | Utilities: scan papers, count citations, extract titles |

## Requirements

- Python 3.10+
- `claude-agent-sdk` (for Claude API access)
- `ANTHROPIC_API_KEY` environment variable

## Relationship to Claude Code

This package reads `.claude/WRITER.md` for agent instructions and can set up skills in a working directory. It's an alternative interface to the same scientific writing capabilities available directly in Claude Code.
