# Development and Architecture

This document is for contributors and maintainers. It summarizes the package architecture, design decisions, and development workflow for Scientific Writer v2.0.

## Architecture Overview

```
scientific_writer/
├── __init__.py          # Public API exports, version
├── api.py               # Async generate_paper() function
├── cli.py               # CLI entrypoint (cli_main)
├── core.py              # Core utilities (API keys, instructions, data processing)
├── models.py            # Data models (ProgressUpdate, PaperResult, etc.)
└── utils.py             # Helper functions (paper detection, file scanning)
```

### Key Components

- `api.generate_paper`: Async generator streaming progress and yielding a comprehensive result
- `cli.cli_main`: CLI interface; 100% backward-compatible behavior
- `core`: Shared logic for API key retrieval, instruction loading, output management, data handling
- `models`: Typed dataclasses for API responses
- `utils`: File scanning, paper detection, and helpers

## Data Models

- `ProgressUpdate`: real-time progress updates (stage, percentage, message, timestamp)
- `PaperResult`: final result with status, files, metadata, citations, and errors
- `PaperMetadata`: title, created_at, topic, word_count
- `PaperFiles`: all relevant paths (final, drafts, references, figures, data, logs)

All models are fully typed and serializable to dictionaries.

## API Design

- Async generator pattern for real-time updates and a final, comprehensive result
- Stateless operation per invocation
- Robust error handling with `success | partial | failed` status
- Automatic paper directory detection and file scanning

## Local Development

### Setup

```bash
uv sync
```

Environment variables:

- `ANTHROPIC_API_KEY` (required)
- `OPENROUTER_API_KEY` (optional, for research lookup)

### Run

```bash
# CLI
uv run scientific-writer

# Example API usage
uv run python example_api_usage.py
```

## Testing and Quality

- Full type hints across the package
- Lint/format according to project defaults
- Validate imports and API signatures locally via example usage

## Release Notes

v2.0 highlights:

- Programmatic API via `generate_paper`
- Progress streaming and comprehensive JSON results
- Modular package structure with entry points
- 100% CLI backward compatibility

See `CHANGELOG.md` for details.

## Migration (v1.x -> v2.0)

- CLI remains identical (`scientific-writer`)
- New package structure replaces single-file script
- For programmatic use, import from `scientific_writer`

Example:

```python
from scientific_writer import generate_paper
```

## Contributing

1. Fork and create a feature branch
2. `uv sync`
3. Make changes with clear commits
4. Ensure examples run
5. Open a pull request with a concise description

## Project Links

- `README.md` — entry point and quick start
- `Docs/API.md` — full API reference
- `Docs/TROUBLESHOOTING.md` — troubleshooting
- `Docs/SKILLS.md` — skills overview
- `CHANGELOG.md` — release history
- `CLAUDE.md` — system instructions (kept at root)


