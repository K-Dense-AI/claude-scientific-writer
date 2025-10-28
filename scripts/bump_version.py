#!/usr/bin/env python3
"""
Version bumping script for scientific-writer package.

This script handles semantic version bumping (major, minor, patch) and ensures
version consistency across pyproject.toml and __init__.py.
"""

import re
import sys
from pathlib import Path
from typing import Tuple, Optional


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
        Current version string in format "X.Y.Z".
    
    Raises
    ------
    ValueError
        If version cannot be found or is invalid.
    """
    content = pyproject_path.read_text()
    match = re.search(r'^version\s*=\s*"(\d+)\.(\d+)\.(\d+)"', content, re.MULTILINE)
    
    if not match:
        raise ValueError("Could not find version in pyproject.toml")
    
    return f"{match.group(1)}.{match.group(2)}.{match.group(3)}"


def parse_version(version: str) -> Tuple[int, int, int]:
    """
    Parse version string into major, minor, patch components.
    
    Parameters
    ----------
    version : str
        Version string in format "X.Y.Z".
    
    Returns
    -------
    Tuple[int, int, int]
        Tuple of (major, minor, patch) version numbers.
    
    Raises
    ------
    ValueError
        If version format is invalid.
    """
    match = re.match(r'^(\d+)\.(\d+)\.(\d+)$', version)
    if not match:
        raise ValueError(f"Invalid version format: {version}")
    
    return int(match.group(1)), int(match.group(2)), int(match.group(3))


def bump_version(version: str, bump_type: str) -> str:
    """
    Bump version according to semantic versioning rules.
    
    Parameters
    ----------
    version : str
        Current version in format "X.Y.Z".
    bump_type : str
        Type of bump: "major", "minor", or "patch".
    
    Returns
    -------
    str
        New version string.
    
    Raises
    ------
    ValueError
        If bump_type is invalid.
    """
    major, minor, patch = parse_version(version)
    
    if bump_type == "major":
        return f"{major + 1}.0.0"
    elif bump_type == "minor":
        return f"{major}.{minor + 1}.0"
    elif bump_type == "patch":
        return f"{major}.{minor}.{patch + 1}"
    else:
        raise ValueError(f"Invalid bump type: {bump_type}. Must be 'major', 'minor', or 'patch'")


def update_pyproject_version(pyproject_path: Path, new_version: str) -> None:
    """
    Update version in pyproject.toml.
    
    Parameters
    ----------
    pyproject_path : Path
        Path to pyproject.toml file.
    new_version : str
        New version string to set.
    """
    content = pyproject_path.read_text()
    
    # Replace version line
    new_content = re.sub(
        r'^version\s*=\s*"(\d+)\.(\d+)\.(\d+)"',
        f'version = "{new_version}"',
        content,
        count=1,
        flags=re.MULTILINE
    )
    
    if content == new_content:
        raise ValueError("Failed to update version in pyproject.toml")
    
    pyproject_path.write_text(new_content)


def update_init_version(init_path: Path, new_version: str) -> None:
    """
    Update version in __init__.py.
    
    Parameters
    ----------
    init_path : Path
        Path to __init__.py file.
    new_version : str
        New version string to set.
    """
    content = init_path.read_text()
    
    # Replace __version__ line
    new_content = re.sub(
        r'^__version__\s*=\s*"(\d+)\.(\d+)\.(\d+)"',
        f'__version__ = "{new_version}"',
        content,
        count=1,
        flags=re.MULTILINE
    )
    
    if content == new_content:
        raise ValueError("Failed to update version in __init__.py")
    
    init_path.write_text(new_content)


def verify_version_consistency(pyproject_path: Path, init_path: Path) -> bool:
    """
    Verify that versions in both files match.
    
    Parameters
    ----------
    pyproject_path : Path
        Path to pyproject.toml file.
    init_path : Path
        Path to __init__.py file.
    
    Returns
    -------
    bool
        True if versions match, False otherwise.
    """
    pyproject_version = read_current_version(pyproject_path)
    
    init_content = init_path.read_text()
    init_match = re.search(r'^__version__\s*=\s*"(\d+)\.(\d+)\.(\d+)"', init_content, re.MULTILINE)
    
    if not init_match:
        return False
    
    init_version = f"{init_match.group(1)}.{init_match.group(2)}.{init_match.group(3)}"
    
    return pyproject_version == init_version


def main() -> int:
    """
    Main entry point for version bumping script.
    
    Returns
    -------
    int
        Exit code (0 for success, 1 for error).
    """
    if len(sys.argv) != 2:
        print("Usage: uv run scripts/bump_version.py [major|minor|patch]")
        print()
        print("Examples:")
        print("  uv run scripts/bump_version.py patch   # 2.0.0 -> 2.0.1")
        print("  uv run scripts/bump_version.py minor   # 2.0.0 -> 2.1.0")
        print("  uv run scripts/bump_version.py major   # 2.0.0 -> 3.0.0")
        return 1
    
    bump_type = sys.argv[1].lower()
    
    if bump_type not in ["major", "minor", "patch"]:
        print(f"Error: Invalid bump type '{bump_type}'")
        print("Must be one of: major, minor, patch")
        return 1
    
    try:
        # Get file paths
        root = get_project_root()
        pyproject_path = root / "pyproject.toml"
        init_path = root / "scientific_writer" / "__init__.py"
        
        # Verify files exist
        if not pyproject_path.exists():
            print(f"Error: pyproject.toml not found at {pyproject_path}")
            return 1
        
        if not init_path.exists():
            print(f"Error: __init__.py not found at {init_path}")
            return 1
        
        # Read current version
        current_version = read_current_version(pyproject_path)
        print(f"Current version: {current_version}")
        
        # Verify consistency before bumping
        if not verify_version_consistency(pyproject_path, init_path):
            print("Warning: Version mismatch detected between pyproject.toml and __init__.py")
            print("Proceeding with version from pyproject.toml as source of truth...")
        
        # Calculate new version
        new_version = bump_version(current_version, bump_type)
        print(f"New version: {new_version}")
        
        # Update both files
        print("\nUpdating version in:")
        update_pyproject_version(pyproject_path, new_version)
        print(f"  ✓ {pyproject_path.relative_to(root)}")
        
        update_init_version(init_path, new_version)
        print(f"  ✓ {init_path.relative_to(root)}")
        
        # Verify consistency after update
        if not verify_version_consistency(pyproject_path, init_path):
            print("\nError: Version consistency check failed after update!")
            return 1
        
        print(f"\n✓ Successfully bumped version from {current_version} to {new_version}")
        print("\nNext steps:")
        print(f"  1. Review changes: git diff")
        print(f"  2. Update CHANGELOG.md with changes for v{new_version}")
        print(f"  3. Commit changes: git add -A && git commit -m 'Bump version to {new_version}'")
        print(f"  4. Create tag: git tag -a v{new_version} -m 'Release v{new_version}'")
        print(f"  5. Publish: uv run scripts/publish.py")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

