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
    
    artifacts = list(dist_dir.glob("*"))
    if not artifacts:
        raise RuntimeError("Build failed: no artifacts in dist/ directory")
    
    print(f"  ✓ Built {len(artifacts)} artifact(s):")
    for artifact in artifacts:
        print(f"    - {artifact.name}")


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
        print(f"  ! Tag {tag_name} already exists, skipping creation")
        return
    
    # Create annotated tag
    run_command(
        ["git", "tag", "-a", tag_name, "-m", f"Release v{version}"],
        cwd=root
    )
    print(f"  ✓ Created tag {tag_name}")
    
    if push:
        print(f"  Pushing tag to remote...")
        run_command(["git", "push", "origin", tag_name], cwd=root)
        print(f"  ✓ Pushed tag to remote")


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
    
    # Check for PyPI token
    token = os.getenv("UV_PUBLISH_TOKEN") or os.getenv("TWINE_PASSWORD")
    pypirc = Path.home() / ".pypirc"
    
    if not token and not pypirc.exists():
        raise RuntimeError(
            "PyPI credentials not found. Please set UV_PUBLISH_TOKEN or TWINE_PASSWORD "
            "environment variable, or configure ~/.pypirc"
        )
    
    print("\nPublishing to PyPI...")
    
    # Run uv publish
    cmd = ["uv", "publish"]
    
    # Add token if available
    if token:
        cmd.extend(["--token", token])
    
    run_command(cmd, cwd=root)
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
    
    # Read new version
    pyproject_path = root / "pyproject.toml"
    return read_current_version(pyproject_path)


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
        
        print("=" * 60)
        print("Scientific Writer - PyPI Publishing")
        print("=" * 60)
        
        # Verify git status (unless skipped)
        if not args.skip_git_check and not args.dry_run:
            print("\nVerifying git status...")
            verify_git_status(root)
            print("  ✓ Working directory is clean")
        
        # Bump version if requested
        if args.bump:
            new_version = bump_version_before_publish(root, args.bump)
            print(f"\n  ✓ Version bumped to {new_version}")
            
            if not args.skip_git_check:
                print("\n  ! Remember to commit version changes before continuing")
                response = input("    Continue? [y/N]: ")
                if response.lower() != 'y':
                    print("  Aborted by user")
                    return 1
        
        # Read current version
        current_version = read_current_version(pyproject_path)
        print(f"\nPublishing version: {current_version}")
        
        # Validate metadata
        print("\nValidating package metadata...")
        validate_package_metadata(root)
        
        # Clean old builds
        print("\nCleaning build artifacts...")
        clean_dist_directory(root)
        
        # Build package
        build_package(root)
        
        # Create git tag (unless skipped or dry run)
        if not args.skip_tag and not args.dry_run:
            create_git_tag(root, current_version, push=True)
        
        # Publish to PyPI
        publish_to_pypi(root, dry_run=args.dry_run)
        
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

