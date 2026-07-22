# Development and Architecture

This document is for contributors and maintainers. It summarizes the package architecture, design decisions, and development workflow for Scientific Writer v2.16+. For day-to-day contribution workflow (tests, lint, PR guidelines), see [CONTRIBUTING.md](../CONTRIBUTING.md).

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
├── .claude-plugin/          # Plugin marketplace metadata
│   └── marketplace.json     # Defines the claude-scientific-writer plugin and its skills
├── commands/                # Plugin commands
│   └── scientific-writer-init.md
├── skills.lock.json         # Pinned upstream revision, selection, and hashes
├── skills/                  # Generated snapshot of 26 upstream skills
│   ├── citation-management/
│   ├── clinical-reports/
│   ├── research-lookup/
│   └── ... (23 more)
├── templates/               # CLAUDE.md template
│   └── CLAUDE.scientific-writer.md
└── scientific_writer/       # Python package
```

There is no `.claude-plugin/plugin.json`; the repository itself acts as a plugin marketplace via `.claude-plugin/marketplace.json`. Skill content is sourced from [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills), pinned by `skills.lock.json`, and vendored into `skills/` for deterministic plugin and package builds. `CLAUDE.md` is the instruction source for both runtime `WRITER.md` mirrors and `templates/CLAUDE.scientific-writer.md`; `scripts/sync_skills.py --check` enforces all three.

The 26 selected skills are: citation-management, clinical-decision-support, clinical-reports, docx, pdf, pptx, xlsx, generate-image, hypothesis-generation, infographics, latex-posters, literature-review, market-research-reports, markitdown, parallel-web, peer-review, pptx-posters, research-grants, research-lookup, scholar-evaluation, scientific-critical-thinking, scientific-schematics, scientific-slides, scientific-writing, treatment-plans, and venue-templates. The four document skills are grouped under the local `document-skills/` plugin path.

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
uv sync --frozen --group dev
```

Environment variables (see `.env.example` for the full list):

- `ANTHROPIC_API_KEY` (required)
- Parallel CLI login or `PARALLEL_API_KEY` (research lookup, web search, and deep research)
- `OPENROUTER_API_KEY` (optional, for AI image generation: schematics, figures, slides, infographics, and markitdown AI features)
- `NCBI_API_KEY` / `NCBI_EMAIL` (optional, for higher-rate PubMed lookups in literature-review scripts)

### Run

```bash
# CLI
uv run scientific-writer

# Example API usage
uv run python example_api_usage.py
```

## Testing and Quality

- Full type hints across the package
- Ruff, mypy, pytest, and codespell in CI
- Locked dependency resolution through committed `uv.lock`
- Validate imports and API signatures locally via `example_api_usage.py`

## Plugin Development

### Testing Plugin Locally

Use the following steps for local plugin development and manual testing:

1. **Create test marketplace** in the parent directory:
   ```bash
   cd ..
   mkdir -p test-marketplace/.claude-plugin
   ```

2. **Configure marketplace** (`test-marketplace/.claude-plugin/marketplace.json`) with a relative path to your local plugin checkout:
   ```json
   {
     "name": "test-marketplace",
     "owner": { "name": "K-Dense" },
     "plugins": [{
       "name": "claude-scientific-writer",
       "source": "../claude-scientific-writer",
       "description": "Scientific writing skills and CLAUDE.md initializer"
     }]
   }
   ```

   **Note**: Update the `source` path to match your local directory structure (relative to the test-marketplace directory).

3. **Add marketplace in Claude Code**:
   ```
   /plugin marketplace add ../test-marketplace
   ```

4. **Install plugin** and restart Claude Code when prompted:
   ```
   /plugin install claude-scientific-writer@test-marketplace
   ```

5. **Test in a project**:
   ```
   /claude-scientific-writer:scientific-writer-init
   ```
   Then verify CLAUDE.md is created, ask "What skills are available?", and try creating a short document.

### Plugin Structure Requirements

- **`.claude-plugin/marketplace.json`** - Marketplace metadata; registers the plugin and lists all skill directories
- **`commands/`** - Command definitions (YAML frontmatter required)
- **`skills/`** - Skill definitions (each with SKILL.md + YAML frontmatter)
- **`templates/`** - Template files (CLAUDE.scientific-writer.md)

### Troubleshooting Plugin Installation

- **Skills not showing**: Verify each `SKILL.md` has valid YAML frontmatter (name, description, allowed-tools) and that the skill directory is listed in `.claude-plugin/marketplace.json`
- **Command not working**: Check `commands/scientific-writer-init.md` exists and has proper frontmatter
- **Template not found**: Ensure `templates/CLAUDE.scientific-writer.md` is present
- **Marketplace not loading**: Verify `marketplace.json` syntax and relative path to plugin

### Adding New Skills

See the [Skill Authoring Guide](SKILL_AUTHORING.md) for the full workflow, frontmatter reference, and quality bar. In brief:

1. Create the skill in the canonical `K-Dense-AI/scientific-agent-skills` repository.
2. Add `SKILL.md` with Agent Skills YAML frontmatter:
   ```yaml
   ---
   name: skill-name
   description: What the skill does and when to use it (1-3 sentences).
   allowed-tools: Read Write Edit Bash
   license: MIT license
   metadata:
       skill-author: K-Dense Inc.
   ---
   ```
   Note that `allowed-tools` is a space-separated string, not a YAML list.
3. Add references, scripts, and assets upstream as needed, then merge and release the change.
4. Select the upstream skill in `skills.lock.json` and register its generated destination in `.claude-plugin/marketplace.json`.
5. Run `python3 scripts/sync_skills.py --update-ref <tag-or-commit>` to regenerate `skills/`, both runtime mirrors, and the plugin instruction template; never edit generated skill snapshots directly.
6. Run `python3 scripts/sync_skills.py --check` and test skill availability after plugin reinstall.

## Release Notes

v2.13+ highlights:

- **Parallel research backend** - research lookup, web search, and deep research use Parallel Search, Extract, and Research through `parallel-cli`; OpenRouter is only used for image generation and explicitly requested optional fallbacks

v2.7.0 highlights:

- **Claude Code Plugin Focus** - Optimized for IDE integration
- Plugin installation with `/claude-scientific-writer:scientific-writer-init`
- All selected skills accessible via plugin (26 as of v2.16)
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
- Use `/claude-scientific-writer:scientific-writer-init` in your project
- Access all skills directly in IDE
- No CLI required for most workflows

### Research backend (v2.13+)

- Authenticate with `parallel-cli login` or set `PARALLEL_API_KEY`
- `OPENROUTER_API_KEY` is optional for image generation and explicitly requested Perplexity fallback research

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for the full workflow. In brief:

1. Fork and create a feature branch
2. `uv sync` to install dependencies
3. Make changes with clear commits
4. Test locally (CLI, API, and plugin if applicable)
5. Ensure all examples run
6. Update documentation if needed
7. Open a pull request with a concise description

## Project Links

- `README.md` — entry point and quick start
- `CONTRIBUTING.md` — contribution workflow
- `docs/API.md` — full API reference
- `docs/TROUBLESHOOTING.md` — troubleshooting
- `docs/SKILLS.md` — skills overview
- `docs/SKILL_AUTHORING.md` — skill authoring guide
- `CHANGELOG.md` — release history
- `CLAUDE.md` — system instructions (kept at root)


