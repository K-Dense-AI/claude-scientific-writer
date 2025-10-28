# Migration Guide: v1.x to v2.0

This guide helps you migrate from Scientific Writer v1.x to v2.0, which introduces a programmatic API while maintaining full backward compatibility with the CLI.

## What's New in v2.0

### ✨ New Features

1. **Programmatic Python API**: Use Scientific Writer as a library in your own code
2. **Async Generator Interface**: Get real-time progress updates during paper generation
3. **Comprehensive JSON Results**: Access all paper metadata, files, citations, and more
4. **Improved Package Structure**: Clean modular architecture
5. **Type Hints**: Full type annotations for better IDE support

### ✅ Backward Compatibility

- ✅ **CLI remains identical**: All existing CLI commands work exactly the same
- ✅ **Same output structure**: Paper directories and files organized the same way
- ✅ **Same features**: All skills, tools, and capabilities preserved
- ✅ **Same configuration**: `.env` files, system instructions, and skills unchanged

## For CLI Users

**No changes required!** The CLI works exactly as before.

### Old Way (still works)
```bash
scientific-writer
> Create a Nature paper on CRISPR gene editing
```

### New Installation
```bash
# If you previously ran:
# python scientific_writer.py

# Now use:
scientific-writer

# Or with uv:
uv run scientific-writer
```

The only difference is that `scientific_writer.py` has been replaced with a proper Python package, but the CLI command `scientific-writer` works identically.

## For Programmatic Use

### New: Python API

You can now import and use Scientific Writer as a library:

```python
import asyncio
from scientific_writer import generate_paper

async def main():
    async for update in generate_paper("Create a NeurIPS paper on transformers"):
        if update["type"] == "progress":
            print(f"[{update['percentage']}%] {update['message']}")
        else:
            print(f"Paper: {update['paper_directory']}")
            print(f"PDF: {update['files']['pdf_final']}")

asyncio.run(main())
```

### Available Imports

```python
from scientific_writer import (
    generate_paper,      # Main API function
    ProgressUpdate,      # Progress update model
    PaperResult,         # Final result model
    PaperMetadata,       # Paper metadata model
    PaperFiles,          # Paper files model
)
```

## Breaking Changes

### None! 🎉

v2.0 is 100% backward compatible. The only "breaking change" is that the package name in `pyproject.toml` changed from `claude-scientific-writer` to `scientific-writer`, but this doesn't affect functionality.

If you previously had scripts that imported from the old `scientific_writer.py` file directly, you'll need to update them to use the package imports shown above.

## Package Structure Changes

### Old Structure (v1.x)
```
claude-scientific-writer/
├── scientific_writer.py    # Single file with all code
├── .claude/
├── paper_outputs/
└── pyproject.toml
```

### New Structure (v2.0)
```
scientific-writer/
├── scientific_writer/       # Package directory
│   ├── __init__.py         # Public API exports
│   ├── api.py              # Async API
│   ├── cli.py              # CLI interface
│   ├── core.py             # Core utilities
│   ├── models.py           # Data models
│   └── utils.py            # Helper functions
├── .claude/
├── paper_outputs/
├── example_api_usage.py    # API examples
└── pyproject.toml
```

## Installation

### Fresh Install
```bash
# Clone the repository
git clone https://github.com/yourusername/scientific-writer.git
cd scientific-writer

# Install with uv
uv sync

# Or install in your environment
uv pip install -e .
```

### Upgrading from v1.x
```bash
# Pull latest changes
git pull origin main

# Reinstall
uv sync
```

## API Examples

### Basic Usage
```python
import asyncio
from scientific_writer import generate_paper

async def create_paper():
    async for update in generate_paper("Create a short paper on quantum computing"):
        if update["type"] == "progress":
            print(f"Progress: {update['message']}")
        else:
            print(f"Complete! PDF: {update['files']['pdf_final']}")

asyncio.run(create_paper())
```

### With Custom Options
```python
async def create_with_options():
    async for update in generate_paper(
        query="Create a NeurIPS paper on attention mechanisms",
        output_dir="./my_papers",
        data_files=["results.csv", "attention_map.png"],
        api_key="sk-ant-...",  # Optional: override env var
    ):
        # Handle updates...
        pass
```

### Save Result to JSON
```python
import json

async def create_and_save():
    async for update in generate_paper("Create a paper on ML"):
        if update["type"] == "result":
            with open("result.json", "w") as f:
                json.dump(update, f, indent=2)
```

## Response Format

### Progress Update
```json
{
  "type": "progress",
  "timestamp": "2024-10-28T14:30:22Z",
  "message": "Writing paper sections",
  "stage": "writing",
  "percentage": 50
}
```

### Final Result
```json
{
  "type": "result",
  "status": "success",
  "paper_directory": "/path/to/paper_outputs/20241028_143022_topic/",
  "paper_name": "20241028_143022_topic",
  "metadata": {
    "title": "Paper Title",
    "created_at": "2024-10-28T14:30:22Z",
    "topic": "topic description",
    "word_count": 5200
  },
  "files": {
    "pdf_final": "/path/to/final/manuscript.pdf",
    "tex_final": "/path/to/final/manuscript.tex",
    "pdf_drafts": [...],
    "tex_drafts": [...],
    "bibliography": "/path/to/references/references.bib",
    "figures": [...],
    "data": [...],
    "progress_log": "/path/to/progress.md",
    "summary": "/path/to/SUMMARY.md"
  },
  "citations": {
    "count": 42,
    "style": "BibTeX",
    "file": "/path/to/references/references.bib"
  },
  "figures_count": 5,
  "compilation_success": true,
  "errors": []
}
```

## Troubleshooting

### Import Error: `ModuleNotFoundError: No module named 'scientific_writer'`

Make sure you've installed the package:
```bash
uv sync
# or
uv pip install -e .
```

### CLI Not Working

Reinstall with uv:
```bash
uv sync
```

Then run:
```bash
uv run scientific-writer
# or just
scientific-writer
```

### API Key Issues

The API now supports passing the key as a parameter:
```python
async for update in generate_paper(
    "Create a paper",
    api_key="your-key-here"  # Override env var
):
    pass
```

## Support

For issues or questions:
- Check the [README.md](README.md) for full documentation
- Review [example_api_usage.py](example_api_usage.py) for code examples
- Open an issue on GitHub

## Summary

**v2.0 is a superset of v1.x** - everything from v1.x works, plus you now have a powerful programmatic API for integrating Scientific Writer into your own applications and workflows.

No migration required for CLI users - just update and continue using as before! 🚀

