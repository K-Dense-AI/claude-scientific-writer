# Claude Scientific Writer

A Python package and CLI for generating publication-ready scientific papers with Claude Sonnet. Version 2.0 adds a fully typed, programmatic API while keeping the CLI 100% backward compatible.

## Quick Start

### Prerequisites
- Python 3.10+
- uv (package and environment manager)
- ANTHROPIC_API_KEY (required), OPENROUTER_API_KEY (optional for research lookup)

### Install
```bash
git clone https://github.com/yourusername/claude-scientific-writer.git
cd claude-scientific-writer
uv sync
```

### Configure API keys
```bash
# .env file (recommended)
echo "ANTHROPIC_API_KEY=your_key" > .env
echo "OPENROUTER_API_KEY=your_openrouter_key" >> .env
# or export in your shell
export ANTHROPIC_API_KEY='your_key'
```

### Use the CLI
```bash
uv run scientific-writer
```

### Use the Python API
```python
import asyncio
from scientific_writer import generate_paper

async def main():
    async for update in generate_paper("Create a Nature paper on CRISPR gene editing"):
        if update["type"] == "progress":
            print(f"[{update['percentage']}%] {update['message']}")
        else:
            print(f"PDF: {update['files']['pdf_final']}")

asyncio.run(main())
```

## Features
- Scientific writing (IMRaD) with LaTeX and BibTeX outputs
- Real-time progress streaming and transparent logging
- Automatic bibliography and citation management
- Data and figure integration from a local data/ folder
- Research lookup via OpenRouter (optional)
- CLI and programmatic API with full type hints

## Typical Workflow
1. Place figures and data in data/ at the project root (images -> figures/, files -> data/ automatically).
2. Run the CLI (or use the API) and describe what you want (venue, topic, constraints).
3. Follow progress updates; outputs are saved under paper_outputs/<timestamp>_<topic>/.

## Documentation
- [API Reference](docs/API.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
- [Skills Overview](docs/SKILLS.md)
- [Development and Contributing](docs/DEVELOPMENT.md)
- [Releasing (versioning & publishing)](docs/RELEASING.md)
- [Release Notes](CHANGELOG.md)
- [System Instructions (for the agent)](CLAUDE.md)

## Versioning and Publishing (short)
Use `uv` and the helper scripts:
- Bump version (keeps pyproject + __init__ in sync): `uv run scripts/bump_version.py [patch|minor|major]`
- Build and publish: `uv run scripts/publish.py` (or `--bump patch|minor|major`)
See [docs/RELEASING.md](docs/RELEASING.md) for prerequisites, dry runs, tagging, and verification.

## Migration (v1.x -> v2.0)
- CLI remains unchanged (scientific-writer).
- New programmatic API: from scientific_writer import generate_paper.
- Legacy single-file script is replaced by a proper package; no action needed for CLI users.

## License
MIT - see LICENSE.

## Support
- Open an issue on GitHub
- See [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for common problems

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=K-Dense-AI/claude-scientific-writer&type=date&legend=top-left)](https://www.star-history.com/#K-Dense-AI/claude-scientific-writer&type=date&legend=top-left)