# Migration to uv

This project has been migrated from using `requirements.txt` and `pip` to using `uv` for dependency management.

## What Changed

### Files Added
- **`pyproject.toml`**: Now contains all project metadata and dependencies
- **`UV_MIGRATION.md`**: This migration guide

### Files Modified
- **`setup.sh`**: Updated to install and use `uv` instead of `pip`
- **`README.md`**: Updated installation instructions to use `uv`
- **`.gitignore`**: Added uv-specific files (`.uv/`, `uv.lock`)

### Files Removed
- **`requirements.txt`**: Replaced by `pyproject.toml`

## Why uv?

[uv](https://docs.astral.sh/uv/) is a modern Python package installer that offers:

- **Speed**: 10-100x faster than pip
- **Reliability**: Better dependency resolution
- **Modern**: Written in Rust, follows modern Python packaging standards
- **Compatibility**: Drop-in replacement for pip with similar commands

## How to Use

### Fresh Installation

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv pip install -e .
```

Or simply run the setup script:
```bash
bash setup.sh
```

### Common Commands

```bash
# Install dependencies
uv pip install -e .

# Add a new dependency
uv pip install package-name

# Update dependencies
uv pip install -e . --upgrade

# Create/sync a virtual environment
uv venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate     # On Windows

# Install in virtual environment
uv pip install -e .
```

### Using with Virtual Environments

```bash
# Create a virtual environment
uv venv

# Activate it
source .venv/bin/activate  # Unix/macOS
# or
.venv\Scripts\activate     # Windows

# Install dependencies
uv pip install -e .

# Run the application
python scientific_writer.py
```

## Rollback (if needed)

If you need to rollback to the old `pip`-based setup:

```bash
# Checkout the old requirements.txt from git
git show HEAD~1:requirements.txt > requirements.txt

# Install with pip
pip install -r requirements.txt
```

## Benefits for This Project

1. **Faster installation**: Scientific workflow dependencies install much quicker
2. **Better reproducibility**: More reliable dependency resolution
3. **Modern standard**: Uses `pyproject.toml` which is the Python packaging standard
4. **Easy updates**: Simple commands to keep dependencies up to date

## Learn More

- [uv Documentation](https://docs.astral.sh/uv/)
- [Python Packaging Guide](https://packaging.python.org/)
- [pyproject.toml specification](https://peps.python.org/pep-0621/)

