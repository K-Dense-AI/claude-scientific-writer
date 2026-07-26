# Contributing to Claude Scientific Writer

Thank you for your interest in contributing! This guide covers the development setup, testing, and pull request workflow. For architecture details and plugin development, see the [Development Guide](docs/DEVELOPMENT.md); for writing new skills, see the [Skill Authoring Guide](docs/SKILL_AUTHORING.md).

## Development Setup

```bash
git clone https://github.com/K-Dense-AI/claude-scientific-writer.git
cd claude-scientific-writer
uv sync --frozen --group dev
```

Copy `.env.example` to `.env` and fill in your API keys:

- `ANTHROPIC_API_KEY` (required)
- Parallel CLI login or `PARALLEL_API_KEY` (research lookup, web search, and deep research)
- `OPENROUTER_API_KEY` (optional, for AI image generation skills)
- `NCBI_API_KEY` / `NCBI_EMAIL` (optional, for higher-rate PubMed lookups)

## Running Tests

```bash
uv run --frozen pytest
```

Tests live in `tests/` and cover the Python package (`scientific_writer/`). Please add or update tests for any behavior you change.

## Linting

```bash
uv run --frozen ruff check .
uv run --frozen mypy
uv run --frozen pre-commit run codespell --all-files
```

Ruff configuration lives in `pyproject.toml`. Fix all lint errors before opening a pull request.

## Skills: Source of Truth

The canonical source of truth for skill content is [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills). `skills.lock.json` pins the exact upstream release and content hashes selected for Scientific Writer.

- `skills/` is the generated plugin snapshot
- `.claude/skills/`
- `scientific_writer/.claude/skills/`

Similarly, `CLAUDE.md` at the root is the source of truth for the agent instructions mirrored to `.claude/WRITER.md` and `scientific_writer/.claude/WRITER.md`.

**Never edit any of the three local skill snapshots directly.** Make skill-content changes upstream, then pin and vendor an upstream tag or commit:

```bash
python3 scripts/sync_skills.py --update-ref <tag-or-commit>
```

To verify the pinned snapshot and mirrors without using the network (this is what CI checks):

```bash
python3 scripts/sync_skills.py --check
```

New skills must be merged upstream, selected in `skills.lock.json`, and registered in `.claude-plugin/marketplace.json` so they are available through the Claude Code plugin. See the [Skill Authoring Guide](docs/SKILL_AUTHORING.md) for the full workflow.

## Pull Request Guidelines

1. **Fork and branch**: Create a feature branch from `main` with a descriptive name (e.g., `fix/latex-compilation-retry`).
2. **Keep changes focused**: One logical change per pull request. Small, reviewable diffs merge faster.
3. **Test locally**: Run Ruff, mypy, pytest, and codespell with `uv run --frozen`. If you changed the upstream skill pin, run `python3 scripts/sync_skills.py --check` and commit the skill lock plus all regenerated snapshots. Commit `uv.lock` whenever project dependencies change.
4. **Exercise what you changed**: For CLI changes run `uv run scientific-writer`; for API changes run `uv run python example_api_usage.py`; for plugin changes follow [Testing Plugin Locally](docs/DEVELOPMENT.md#testing-plugin-locally).
5. **Update documentation**: If your change affects user-facing behavior, update the README and the relevant files under `docs/`.
6. **Write clear commits**: Use concise, descriptive commit messages that explain the why, not just the what.
7. **Open the pull request**: Include a short description of the problem, the approach, and how you verified it.

## Reporting Issues

Found a bug or have a feature request? Open an issue at
[github.com/K-Dense-AI/claude-scientific-writer/issues](https://github.com/K-Dense-AI/claude-scientific-writer/issues) with steps to reproduce, your OS and Python version, and the full error output. Check the [Troubleshooting Guide](docs/TROUBLESHOOTING.md) first for known issues.

## Releasing

Version bumps and PyPI publishing are handled by maintainers. See [docs/RELEASING.md](docs/RELEASING.md) for the release process, including `scripts/bump_version.py` and `scripts/publish.py`.

## Code of Conduct

Be respectful and constructive. We want this to be a welcoming project for researchers and developers alike. If you have questions, join the [K-Dense Community on Slack](https://join.slack.com/t/k-densecommunity/shared_invite/zt-3iajtyls1-EwmkwIZk0g_o74311Tkf5g).
