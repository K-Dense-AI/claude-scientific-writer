#!/usr/bin/env python3
"""
PyPI publishing script for scientific-writer package.

This script handles building and publishing the package to PyPI, with optional
version bumping and git tagging.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Optional, List


def get_project_root() -> Path:
    """
    Get the project root directory.

    Returns
    -------
    Path
        Path to the project root directory.
    """
    return Path(__file__).parent.parent.resolve()


def read_current_version(pyproject_path: Path) -> str:
    """
    Read the current version from pyproject.toml.

    Parameters
    ----------
    pyproject_path : Path
        Path to pyproject.toml file.

    Returns
    -------
    str
        Current version string.

    Raises
    ------
    ValueError
        If version cannot be found.
    """
    content = pyproject_path.read_text()
    match = re.search(r'^version\s*=\s*"(\d+)\.(\d+)\.(\d+)"', content, re.MULTILINE)

    if not match:
        raise ValueError("Could not find version in pyproject.toml")

    return f"{match.group(1)}.{match.group(2)}.{match.group(3)}"


def run_command(cmd: List[str], cwd: Optional[Path] = None, capture_output: bool = False) -> subprocess.CompletedProcess:
    """
    Run a shell command and handle errors.

    Parameters
    ----------
    cmd : List[str]
        Command and arguments to run.
    cwd : Optional[Path]
        Working directory for the command.
    capture_output : bool
        Whether to capture stdout/stderr.

    Returns
    -------
    subprocess.CompletedProcess
        Result of the command execution.

    Raises
    ------
    subprocess.CalledProcessError
        If command fails.
    """
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=capture_output,
        text=True,
        check=True
    )
    return result


def clean_dist_directory(root: Path) -> None:
    """
    Remove old build artifacts.

    Parameters
    ----------
    root : Path
        Project root directory.
    """
    dist_dir = root / "dist"
    if dist_dir.exists():
        print(f"Cleaning {dist_dir}...")
        shutil.rmtree(dist_dir)
        print("  ✓ Removed old build artifacts")
    else:
        print("  ✓ No old build artifacts to clean")


def build_package(root: Path) -> None:
    """
    Build the package using uv build.

    Parameters
    ----------
    root : Path
        Project root directory.

    Raises
    ------
    subprocess.CalledProcessError
        If build fails.
    """
    print("\nBuilding package...")
    run_command(["uv", "build"], cwd=root)

    # Verify build artifacts
    dist_dir = root / "dist"
    if not dist_dir.exists():
        raise RuntimeError("Build failed: dist/ directory not created")

    artifacts = sorted(
        [*dist_dir.glob("*.whl"), *dist_dir.glob("*.tar.gz")],
        key=lambda path: path.name,
    )
    if not artifacts:
        raise RuntimeError("Build failed: no artifacts in dist/ directory")

    print(f"  ✓ Built {len(artifacts)} artifact(s):")
    for artifact in artifacts:
        print(f"    - {artifact.name}")

    verify_wheel_payload(dist_dir)


def verify_wheel_payload(dist_dir: Path) -> None:
    """
    Assert the wheel ships WRITER.md, the skill lock, the plugin manifest, and skills.

    The entire runtime depends on these non-.py data files; if the build tooling
    ever drops them, the package would silently degrade to a generic prompt with
    no skills. Fail the release instead.

    Parameters
    ----------
    dist_dir : Path
        Directory containing the built wheel.

    Raises
    ------
    RuntimeError
        If the wheel is missing the .claude payload.
    """
    wheels = sorted(dist_dir.glob("*.whl"))
    if not wheels:
        raise RuntimeError("No wheel found in dist/ to verify")

    wheel = wheels[-1]
    with zipfile.ZipFile(wheel) as zf:
        names = zf.namelist()
    claude_files = [n for n in names if "/.claude/" in n or n.startswith("scientific_writer/.claude/")]
    has_writer = any(n.endswith(".claude/WRITER.md") for n in names)
    has_skills_lock = any(n.endswith(".claude/skills.lock.json") for n in names)
    # The bundled payload is also an Agent Plugins package; without the manifest
    # no Agent Plugins client can load the skills out of an installed wheel.
    has_plugin_manifest = any(n.endswith(".claude/plugin.json") for n in names)
    skill_files = [n for n in claude_files if "/skills/" in n]

    if not has_writer or not has_skills_lock or not has_plugin_manifest or len(skill_files) < 100:
        raise RuntimeError(
            f"Wheel {wheel.name} is missing the bundled .claude payload "
            f"(WRITER.md found: {has_writer}, skills.lock.json found: {has_skills_lock}, "
            f"plugin.json found: {has_plugin_manifest}, "
            f"skill files: {len(skill_files)}). "
            "Check the hatchling build configuration before publishing."
        )
    print(
        f"  ✓ Wheel contains .claude payload ({len(claude_files)} files, "
        "WRITER.md, skills.lock.json, and plugin.json present)"
    )


def verify_git_status(root: Path) -> None:
    """
    Verify git status is clean.

    Parameters
    ----------
    root : Path
        Project root directory.

    Raises
    ------
    RuntimeError
        If there are uncommitted changes.
    """
    result = run_command(
        ["git", "status", "--porcelain"],
        cwd=root,
        capture_output=True
    )

    if result.stdout.strip():
        raise RuntimeError(
            "Working directory has uncommitted changes. "
            "Please commit or stash changes before publishing."
        )


def create_git_tag(root: Path, version: str, push: bool = True) -> None:
    """
    Create an annotated git tag for the version.

    Parameters
    ----------
    root : Path
        Project root directory.
    version : str
        Version string for the tag.
    push : bool
        Whether to push the tag to remote.
    """
    tag_name = f"v{version}"

    print(f"\nCreating git tag {tag_name}...")

    # Check if tag already exists
    result = run_command(
        ["git", "tag", "-l", tag_name],
        cwd=root,
        capture_output=True
    )

    if result.stdout.strip():
        raise RuntimeError(
            f"Tag {tag_name} already exists. If you are re-publishing, delete the "
            f"tag first (git tag -d {tag_name}; git push origin :refs/tags/{tag_name}) "
            "or bump the version."
        )

    # Create annotated tag
    run_command(
        ["git", "tag", "-a", tag_name, "-m", f"Release v{version}"],
        cwd=root
    )
    print(f"  ✓ Created tag {tag_name}")

    if push:
        print("  Pushing tag to remote...")
        run_command(["git", "push", "origin", tag_name], cwd=root)
        print("  ✓ Pushed tag to remote")


def publish_to_pypi(root: Path, dry_run: bool = False) -> None:
    """
    Publish package to PyPI using uv publish.

    Parameters
    ----------
    root : Path
        Project root directory.
    dry_run : bool
        If True, build but don't publish.

    Raises
    ------
    RuntimeError
        If PyPI token is not configured.
    subprocess.CalledProcessError
        If publish fails.
    """
    if dry_run:
        print("\n✓ Dry run complete - package built but not published")
        return

    # Check for PyPI token (note: uv publish does NOT read ~/.pypirc)
    token = os.getenv("UV_PUBLISH_TOKEN") or os.getenv("TWINE_PASSWORD")

    if not token:
        raise RuntimeError(
            "PyPI credentials not found. Set the UV_PUBLISH_TOKEN (or TWINE_PASSWORD) "
            "environment variable. Note that `uv publish` does not read ~/.pypirc."
        )

    print("\nPublishing to PyPI...")

    # uv publish reads UV_PUBLISH_TOKEN from the environment; never pass the
    # token on the command line (run_command echoes commands, which would leak
    # it into logs).
    env = os.environ.copy()
    env.setdefault("UV_PUBLISH_TOKEN", token)
    print("Running: uv publish")
    subprocess.run(["uv", "publish"], cwd=root, env=env, check=True)
    print("  ✓ Package published to PyPI")


def bump_version_before_publish(root: Path, bump_type: str) -> str:
    """
    Bump version using bump_version.py script.

    Parameters
    ----------
    root : Path
        Project root directory.
    bump_type : str
        Type of bump: "major", "minor", or "patch".

    Returns
    -------
    str
        New version string.

    Raises
    ------
    subprocess.CalledProcessError
        If bump script fails.
    """
    print(f"\nBumping {bump_type} version...")
    bump_script = root / "scripts" / "bump_version.py"

    if not bump_script.exists():
        raise RuntimeError(f"Bump script not found at {bump_script}")

    run_command(["uv", "run", str(bump_script), bump_type], cwd=root)
    run_command(["uv", "lock"], cwd=root)

    # Read new version
    pyproject_path = root / "pyproject.toml"
    return read_current_version(pyproject_path)


def commit_version_bump(root: Path, version: str) -> None:
    """
    Commit the version-bump changes so the release tag points at a commit
    that actually contains the new version.

    Parameters
    ----------
    root : Path
        Project root directory.
    version : str
        The new version string.
    """
    version_files = [
        "pyproject.toml",
        "scientific_writer/__init__.py",
        ".claude-plugin/marketplace.json",
        "uv.lock",
    ]
    existing = [f for f in version_files if (root / f).exists()]
    run_command(["git", "add", *existing], cwd=root)
    run_command(["git", "commit", "-m", f"Bump version to {version}"], cwd=root)
    print(f"  ✓ Committed version bump to {version}")


def push_release_commit(root: Path) -> None:
    """Push the release commit before uploading artifacts or creating a tag."""
    branch = run_command(
        ["git", "branch", "--show-current"],
        cwd=root,
        capture_output=True,
    ).stdout.strip()
    if not branch:
        raise RuntimeError("Cannot publish from a detached HEAD")
    run_command(["git", "push", "origin", branch], cwd=root)
    print(f"  ✓ Pushed release commit on {branch}")


def verify_skill_mirrors(root: Path) -> None:
    """
    Verify the .claude skill mirrors are in sync with skills/ before shipping.

    Raises
    ------
    subprocess.CalledProcessError
        If the mirrors have drifted (sync_skills.py --check exits non-zero).
    """
    sync_script = root / "scripts" / "sync_skills.py"
    if not sync_script.exists():
        raise RuntimeError(f"Sync script not found at {sync_script}")
    run_command([sys.executable, str(sync_script), "--check"], cwd=root)
    print("  ✓ Skill mirrors are in sync")


def run_release_checks(root: Path) -> None:
    """Run the same quality and package checks enforced by release CI."""
    commands = [
        ["uv", "run", "--frozen", "ruff", "check", "."],
        ["uv", "run", "--frozen", "mypy"],
        ["uv", "run", "--frozen", "pytest", "tests/", "-q"],
        [
            "uv",
            "run",
            "--frozen",
            "codespell",
            "README.md",
            "CHANGELOG.md",
            "CONTRIBUTING.md",
            "example_api_usage.py",
            "CLAUDE.md",
            "pyproject.toml",
            ".env.example",
            "scientific_writer",
            "scripts",
            "tests",
            "docs",
            "commands",
            "templates",
            ".github",
        ],
        ["uv", "run", "--frozen", "python", "scripts/check_consistency.py"],
        ["uv", "run", "--frozen", "python", "scripts/verify_package.py"],
    ]
    for command in commands:
        run_command(command, cwd=root)
    print("  ✓ Release quality checks passed")


def validate_package_metadata(root: Path) -> None:
    """
    Validate package metadata in pyproject.toml.

    Parameters
    ----------
    root : Path
        Project root directory.

    Raises
    ------
    ValueError
        If required metadata is missing.
    """
    pyproject_path = root / "pyproject.toml"
    content = pyproject_path.read_text()

    required_fields = {
        "name": r'^name\s*=\s*"([^"]+)"',
        "version": r'^version\s*=\s*"([^"]+)"',
        "description": r'^description\s*=\s*"([^"]+)"',
    }

    missing = []
    for field, pattern in required_fields.items():
        if not re.search(pattern, content, re.MULTILINE):
            missing.append(field)

    if missing:
        raise ValueError(f"Missing required metadata fields: {', '.join(missing)}")

    print("  ✓ Package metadata validated")


def main() -> int:
    """
    Main entry point for publishing script.

    Returns
    -------
    int
        Exit code (0 for success, 1 for error).
    """
    parser = argparse.ArgumentParser(
        description="Build and publish scientific-writer package to PyPI"
    )
    parser.add_argument(
        "--bump",
        choices=["major", "minor", "patch"],
        help="Bump version before publishing"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Build package but don't publish"
    )
    parser.add_argument(
        "--skip-tag",
        action="store_true",
        help="Skip git tag creation"
    )
    parser.add_argument(
        "--skip-git-check",
        action="store_true",
        help="Skip git status verification"
    )

    args = parser.parse_args()

    try:
        root = get_project_root()
        pyproject_path = root / "pyproject.toml"
        release_commit_created = False

        print("=" * 60)
        print("Scientific Writer - PyPI Publishing")
        print("=" * 60)

        # Verify git status (unless skipped)
        if not args.skip_git_check and not args.dry_run:
            print("\nVerifying git status...")
            verify_git_status(root)
            print("  ✓ Working directory is clean")

        # Bump version if requested, and commit it so the tag matches the release
        if args.bump:
            new_version = bump_version_before_publish(root, args.bump)
            print(f"\n  ✓ Version bumped to {new_version}")
            if not args.dry_run:
                commit_version_bump(root, new_version)
                release_commit_created = True

        # Read current version
        current_version = read_current_version(pyproject_path)
        print(f"\nPublishing version: {current_version}")

        # Validate metadata
        print("\nValidating package metadata...")
        validate_package_metadata(root)

        # Verify skill mirrors are in sync with skills/
        print("\nVerifying skill mirrors...")
        verify_skill_mirrors(root)

        print("\nRunning release checks...")
        run_release_checks(root)
        if release_commit_created:
            push_release_commit(root)

        # Clean old builds
        print("\nCleaning build artifacts...")
        clean_dist_directory(root)

        # Build package
        build_package(root)

        # Publish to PyPI first; only tag once the upload has succeeded,
        # so a failed upload never leaves a pushed tag with no release.
        publish_to_pypi(root, dry_run=args.dry_run)

        # Create git tag (unless skipped or dry run)
        if not args.skip_tag and not args.dry_run:
            create_git_tag(root, current_version, push=True)

        print("\n" + "=" * 60)
        if args.dry_run:
            print("✓ DRY RUN COMPLETE")
            print("=" * 60)
            print("\nPackage built successfully but not published.")
            print("To publish, run: uv run scripts/publish.py")
        else:
            print("✓ PUBLICATION COMPLETE")
            print("=" * 60)
            print(f"\nPackage scientific-writer v{current_version} published to PyPI!")
            print("\nInstallation commands:")
            print(f"  pip install scientific-writer=={current_version}")
            print(f"  uv pip install scientific-writer=={current_version}")
            print(f"  uvx scientific-writer@{current_version}")

        return 0

    except subprocess.CalledProcessError as e:
        print(f"\nCommand failed: {e.cmd}")
        if e.stdout:
            print(f"stdout: {e.stdout}")
        if e.stderr:
            print(f"stderr: {e.stderr}")
        return 1
    except Exception as e:
        print(f"\nError: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

