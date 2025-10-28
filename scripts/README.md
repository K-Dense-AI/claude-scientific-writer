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

After bumping:
1. Review changes with `git diff`
2. Update `CHANGELOG.md`
3. Commit the version changes
4. Create a git tag
5. Publish to PyPI

## Publishing to PyPI

### Prerequisites

Set up PyPI credentials using one of these methods:

**Option 1: Environment Variable (Recommended)**
```bash
export UV_PUBLISH_TOKEN="pypi-your-token-here"
```

**Option 2: `.pypirc` file**
Create `~/.pypirc`:
```ini
[pypi]
username = __token__
password = pypi-your-token-here
```

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
2. Optionally bumps version (if `--bump` specified)
3. Validates package metadata
4. Cleans old build artifacts
5. Builds wheel and source distribution with `uv build`
6. Creates git tag `vX.Y.Z` (unless `--skip-tag` or `--dry-run`)
7. Publishes to PyPI with `uv publish` (unless `--dry-run`)

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

# Or do it all at once:
uv run scripts/publish.py --bump patch
# (then manually update CHANGELOG.md and commit)
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
Set `UV_PUBLISH_TOKEN` environment variable or create `~/.pypirc`

### "Working directory has uncommitted changes"
Either commit/stash changes or use `--skip-git-check` flag

### Build fails
Ensure you're in the project root and `pyproject.toml` exists

