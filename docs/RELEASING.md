# Releasing: Versioning and Publishing

This guide covers version bumps and publishing to PyPI for this package. It consolidates all essentials into one concise document.

## Requirements

- uv installed (environment and build manager)
- PyPI token configured via environment or ~/.pypirc
  - Environment: `export UV_PUBLISH_TOKEN="pypi-***"`
  - Or `~/.pypirc`:
    ```ini
    [pypi]
    username = __token__
    password = pypi-***
    ```

## Bump the Version (semver)

Use the helper script to bump patch, minor, or major and keep `pyproject.toml` and `scientific_writer/__init__.py` in sync:

```bash
uv run scripts/bump_version.py patch   # X.Y.Z -> X.Y.(Z+1)
uv run scripts/bump_version.py minor   # X.Y.Z -> X.(Y+1).0
uv run scripts/bump_version.py major   # X.Y.Z -> (X+1).0.0
```

After bumping, review changes and update `CHANGELOG.md`; then commit.

## Publish to PyPI

Build and publish with uv. You can optionally bump and publish in one command.

```bash
# Build only (dry run)
uv run scripts/publish.py --dry-run

# Publish current version
uv run scripts/publish.py

# Bump and publish in one step
uv run scripts/publish.py --bump patch   # or minor | major
```

The publisher script will validate metadata, build sdist and wheel, create and push a git tag (`vX.Y.Z`), and publish via `uv publish`.

## Verify

Local verification before publishing (optional):

```bash
uv run scripts/verify_package.py
```

Basic smoke checks after release:

```bash
pip install scientific-writer==X.Y.Z
python -c "from scientific_writer import generate_paper; print('ok')"
uvx scientific-writer --help
```

## CLI entry points

- Installed command: `scientific-writer`
- One-off: `uvx scientific-writer`
- Tools: `uv tool install scientific-writer` then `uv tool run scientific-writer`

## Notes

- Semantic versioning: breaking changes → major; features → minor; fixes → patch.
- If a tag already exists, delete/recreate it or skip tagging with `--skip-tag`.
- If your working tree is dirty, commit or use `--skip-git-check` (not recommended).


