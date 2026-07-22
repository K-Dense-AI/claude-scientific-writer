# Releasing: Versioning and Publishing

This guide covers version bumps and publishing to PyPI for this package. It consolidates all essentials into one concise document.

## Recommended: Trusted Publishing via GitHub Actions

Releases publish to PyPI through `.github/workflows/release.yml` using [Trusted Publishing](https://docs.pypi.org/trusted-publishers/) (OIDC) — no long-lived PyPI token exists anywhere.

**One-time setup** (already done if releases work): on pypi.org, open the `scientific-writer` project → Settings → Publishing → add a GitHub publisher with owner `K-Dense-AI`, repository `claude-scientific-writer`, workflow `release.yml`, environment `pypi`.

**To release:**

```bash
# 1. Bump the version (updates pyproject.toml, __init__.py, marketplace.json)
uv run scripts/bump_version.py minor   # or patch | major
uv lock

# 2. Update CHANGELOG.md, then commit the version files and uv.lock
git add -A && git commit -m "Bump version to X.Y.Z" && git push

# 3. Tag and push the tag — this triggers the release workflow
git tag -a vX.Y.Z -m "Release vX.Y.Z"
git push origin vX.Y.Z
```

The workflow verifies the tag matches the package version, installs the committed lock
with `--frozen`, runs Ruff, mypy, pytest, codespell, consistency and package checks,
builds the exact artifacts to publish, asserts the wheel ships the bundled `.claude`
payload, and publishes.

## Alternative: Local publish with a token

- Requires a PyPI token in the environment: `export UV_PUBLISH_TOKEN="pypi-***"`
  (note: `uv publish` does not read `~/.pypirc`)

```bash
# Build only (dry run)
uv run scripts/publish.py --dry-run

# Publish current version
uv run scripts/publish.py

# Bump and publish in one step (auto-commits the bump)
uv run scripts/publish.py --bump patch   # or minor | major
```

The publisher script validates metadata, verifies skills and quality checks, pushes any
automatically created release commit, builds and checks the artifacts, publishes via
`uv publish`, and only then creates and pushes the git tag (`vX.Y.Z`).

## Bump the Version (semver)

Use the helper script to bump patch, minor, or major and keep `pyproject.toml`, `scientific_writer/__init__.py`, and `.claude-plugin/marketplace.json` in sync:

```bash
uv run scripts/bump_version.py patch   # X.Y.Z -> X.Y.(Z+1)
uv run scripts/bump_version.py minor   # X.Y.Z -> X.(Y+1).0
uv run scripts/bump_version.py major   # X.Y.Z -> (X+1).0.0
```

After bumping, review changes and update `CHANGELOG.md`; then commit.

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


