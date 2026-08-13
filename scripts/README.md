# Scripts for Package Management

This directory contains automation scripts for managing the scientific-writer package.

## Version Management

### Bump Version

Increment the package version following semantic versioning:

```bash
# Bump patch version (2.0.0 -> 2.0.1)
uv run scripts/bump_version.py patch

# Bump minor version (2.0.0 -> 2.1.0)
uv run scripts/bump_version.py minor

# Bump major version (2.0.0 -> 3.0.0)
uv run scripts/bump_version.py major
```

The script automatically updates version in:
- `pyproject.toml`
- `scientific_writer/__init__.py`
- `.claude-plugin/marketplace.json`
- `plugin.json` and its mirrors in `.claude/` and `scientific_writer/.claude/`

After bumping:
1. Review changes with `git diff`
2. Update `CHANGELOG.md`
3. Commit the version changes
4. Create a git tag
5. Publish to PyPI

## Publishing to PyPI

### Prerequisites

The recommended release path is the tag-triggered GitHub Actions workflow with PyPI
Trusted Publishing. For the alternative local publisher, set a token in the environment:

```bash
export UV_PUBLISH_TOKEN="pypi-your-token-here"
```

`uv publish` does not read `~/.pypirc`.

### Publish Package

```bash
# Publish current version
uv run scripts/publish.py

# Bump patch version and publish
uv run scripts/publish.py --bump patch

# Bump minor version and publish
uv run scripts/publish.py --bump minor

# Dry run (build only, don't publish)
uv run scripts/publish.py --dry-run

# Skip git tag creation
uv run scripts/publish.py --skip-tag

# Skip git status check (use with caution)
uv run scripts/publish.py --skip-git-check
```

The publish script:
1. Verifies git working directory is clean (unless `--skip-git-check`)
2. Optionally bumps and commits the version and refreshed `uv.lock`
3. Validates metadata, skills, lint, types, tests, spelling, and package structure
4. Pushes an automatically created release commit before publication
5. Cleans old build artifacts and builds the wheel/source distribution
6. Publishes to PyPI with `uv publish` (unless `--dry-run`)
7. Creates and pushes `vX.Y.Z` only after a successful upload

## Complete Workflow Example

```bash
# 1. Bump version
uv run scripts/bump_version.py patch

# 2. Update changelog
nano CHANGELOG.md

# 3. Commit changes
git add -A
git commit -m "Bump version to 2.0.1"

# 4. Publish (this will create and push git tag)
uv run scripts/publish.py

# Or, after updating and committing the changelog, bump and publish in one step:
uv run scripts/publish.py --bump patch
```

## Package Installation

After publishing, users can install the package:

```bash
# Using pip
pip install scientific-writer

# Using uv
uv pip install scientific-writer

# Using uv tool (for CLI)
uv tool install scientific-writer

# Using uvx (one-off CLI usage)
uvx scientific-writer
```

## Validating Agent Plugins Conformance

`validate_agent_plugin.py` checks a plugin directory against the
[Agent Plugins](https://agent-plugins.org/specification) specification using the schemas vendored in
`scripts/schemas/agent-plugins/`. It runs offline and needs no dependencies.

```bash
# Repository root plus the bundled .claude payloads (what CI runs)
uv run python scripts/validate_agent_plugin.py

# Any other plugin directory
uv run python scripts/validate_agent_plugin.py ../some-plugin

# Treat warnings as failures
uv run python scripts/validate_agent_plugin.py --strict
```

See [docs/AGENT_PLUGINS.md](../docs/AGENT_PLUGINS.md) for what it checks and the one known warning.

## Verifying Package Structure

Both API and CLI are properly exposed:

**API Usage:**
```python
from scientific_writer import generate_paper
# or
from scientific_writer.api import generate_paper
```

**CLI Usage:**
```bash
scientific-writer
# or
uvx scientific-writer
```

## Troubleshooting

### "No module named 'uv'"
Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`

### "PyPI credentials not found"
Set the `UV_PUBLISH_TOKEN` environment variable, or use the Trusted Publishing workflow.

### "Working directory has uncommitted changes"
Either commit/stash changes or use `--skip-git-check` flag

### Build fails
Ensure you're in the project root and `pyproject.toml` exists

