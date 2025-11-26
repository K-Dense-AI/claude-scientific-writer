# Development and Architecture

This document is for contributors and maintainers. It summarizes the package architecture, design decisions, and development workflow for Scientific Writer v2.7.0.

## Architecture Overview

### Package Structure

```
scientific_writer/
├── __init__.py          # Public API exports, version
├── api.py               # Async generate_paper() function
├── cli.py               # CLI entrypoint (cli_main)
├── core.py              # Core utilities (API keys, instructions, data processing)
├── models.py            # Data models (ProgressUpdate, PaperResult, etc.)
└── utils.py             # Helper functions (paper detection, file scanning)
```

### Plugin Structure

```
claude-scientific-writer/
├── .claude-plugin/          # Plugin metadata
│   └── plugin.json
├── commands/                # Plugin commands
│   └── scientific-writer-init.md
├── skills/                  # All 19+ skills
│   ├── citation-management/
│   ├── clinical-reports/
│   ├── research-lookup/
│   └── ... (16+ more)
├── templates/               # CLAUDE.md template
│   └── CLAUDE.scientific-writer.md
└── scientific_writer/       # Python package
```

### Key Components

- `api.generate_paper`: Async generator streaming progress and yielding a comprehensive result
- `cli.cli_main`: CLI interface; 100% backward-compatible behavior
- `core`: Shared logic for API key retrieval, instruction loading, output management, data handling
- `models`: Typed dataclasses for API responses
- `utils`: File scanning, paper detection, and helpers
- **Plugin System**: Commands, skills, and templates for Claude Code integration

## Data Models

- `ProgressUpdate`: real-time progress updates (stage, message, timestamp, details)
- `PaperResult`: final result with status, files, metadata, citations, token_usage, and errors
- `PaperMetadata`: title, created_at, topic, word_count
- `PaperFiles`: all relevant paths (final, drafts, references, figures, data, logs)
- `TokenUsage`: token consumption statistics (input_tokens, output_tokens, total_tokens, cache stats)

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

## Plugin Development

### Testing Plugin Locally

For local plugin development and testing:

1. **Create test marketplace** (see `TESTING_INSTRUCTIONS.md`):
   ```bash
   cd ..
   mkdir -p test-marketplace/.claude-plugin
   ```

2. **Configure marketplace** with relative path to your local plugin:
   ```json
   {
     "name": "test-marketplace",
     "plugins": [{
       "name": "claude-scientific-writer",
       "source": "../claude-scientific-writer"
     }]
   }
   ```

3. **Add marketplace in Claude Code**:
   ```
   /plugin marketplace add ../test-marketplace
   ```

4. **Install plugin**:
   ```
   /plugin install claude-scientific-writer@test-marketplace
   ```

5. **Test in a project**:
   ```
   /scientific-writer:init
   ```

### Plugin Structure Requirements

- **`.claude-plugin/plugin.json`** - Plugin metadata
- **`commands/`** - Command definitions (YAML frontmatter required)
- **`skills/`** - Skill definitions (each with SKILL.md + YAML frontmatter)
- **`templates/`** - Template files (CLAUDE.scientific-writer.md)

### Adding New Skills

1. Create directory in `skills/`
2. Add `SKILL.md` with YAML frontmatter:
   ```yaml
   ---
   name: skill-name
   description: Brief description
   allowed-tools: [read_file, write, etc.]
   ---
   ```
3. Add references, scripts, assets as needed
4. Test skill availability after plugin reinstall

## Release Notes

v2.7.0 highlights:

- **Claude Code Plugin Focus** - Optimized for IDE integration
- Plugin installation with `/scientific-writer:init`
- All 19+ skills accessible via plugin
- Streamlined IDE workflow

v2.0 highlights:

- Programmatic API via `generate_paper`
- Progress streaming and comprehensive JSON results
- Modular package structure with entry points
- 100% CLI backward compatibility

See `CHANGELOG.md` for details.

## Migration Guides

### v1.x -> v2.0

- CLI remains identical (`scientific-writer`)
- New package structure replaces single-file script
- For programmatic use, import from `scientific_writer`

Example:

```python
from scientific_writer import generate_paper
```

### CLI/API -> Plugin (v2.7.0)

For best IDE experience:
- Install as Claude Code plugin (recommended)
- Use `/scientific-writer:init` in your project
- Access all skills directly in IDE
- No CLI required for most workflows

## Contributing

1. Fork and create a feature branch
2. `uv sync` to install dependencies
3. Make changes with clear commits
4. Test locally (CLI, API, and plugin if applicable)
5. Ensure all examples run
6. Update documentation if needed
7. Open a pull request with a concise description

## Project Links

- `README.md` — entry point and quick start
- `Docs/API.md` — full API reference
- `Docs/TROUBLESHOOTING.md` — troubleshooting
- `Docs/SKILLS.md` — skills overview
- `CHANGELOG.md` — release history
- `CLAUDE.md` — system instructions (kept at root)


