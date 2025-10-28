#!/usr/bin/env python3
"""
Package verification script for scientific-writer.

This script verifies that the package is correctly configured for both
API and CLI usage.
"""

import re
import sys
from pathlib import Path
from typing import Dict, List


def get_project_root() -> Path:
    """
    Get the project root directory.
    
    Returns
    -------
    Path
        Path to the project root directory.
    """
    return Path(__file__).parent.parent.resolve()


def check_version_consistency() -> Dict[str, str]:
    """
    Check version consistency across files.
    
    Returns
    -------
    Dict[str, str]
        Dictionary with version from each file.
    """
    root = get_project_root()
    versions = {}
    
    # Check pyproject.toml
    pyproject = root / "pyproject.toml"
    content = pyproject.read_text()
    match = re.search(r'^version\s*=\s*"([^"]+)"', content, re.MULTILINE)
    if match:
        versions['pyproject.toml'] = match.group(1)
    
    # Check __init__.py
    init_file = root / "scientific_writer" / "__init__.py"
    content = init_file.read_text()
    match = re.search(r'^__version__\s*=\s*"([^"]+)"', content, re.MULTILINE)
    if match:
        versions['__init__.py'] = match.group(1)
    
    return versions


def check_api_exports() -> List[str]:
    """
    Check what's exported from __init__.py.
    
    Returns
    -------
    List[str]
        List of exported names.
    """
    root = get_project_root()
    init_file = root / "scientific_writer" / "__init__.py"
    content = init_file.read_text()
    
    match = re.search(r'__all__\s*=\s*\[(.*?)\]', content, re.DOTALL)
    if not match:
        return []
    
    # Extract names from __all__
    names = re.findall(r'"([^"]+)"', match.group(1))
    return names


def check_cli_entry_point() -> bool:
    """
    Check if CLI entry point is configured.
    
    Returns
    -------
    bool
        True if entry point is configured.
    """
    root = get_project_root()
    pyproject = root / "pyproject.toml"
    content = pyproject.read_text()
    
    # Check for [project.scripts] section
    return bool(re.search(
        r'\[project\.scripts\].*?scientific-writer\s*=\s*"scientific_writer\.cli:cli_main"',
        content,
        re.DOTALL
    ))


def check_package_structure() -> Dict[str, bool]:
    """
    Check if required package files exist.
    
    Returns
    -------
    Dict[str, bool]
        Dictionary of file existence checks.
    """
    root = get_project_root()
    
    required_files = {
        'pyproject.toml': root / "pyproject.toml",
        'README.md': root / "README.md",
        'LICENSE': root / "LICENSE",
        '__init__.py': root / "scientific_writer" / "__init__.py",
        'api.py': root / "scientific_writer" / "api.py",
        'cli.py': root / "scientific_writer" / "cli.py",
        'core.py': root / "scientific_writer" / "core.py",
        'models.py': root / "scientific_writer" / "models.py",
        'utils.py': root / "scientific_writer" / "utils.py",
    }
    
    return {name: path.exists() for name, path in required_files.items()}


def main() -> int:
    """
    Main verification routine.
    
    Returns
    -------
    int
        Exit code (0 for success, 1 for error).
    """
    print("=" * 60)
    print("Scientific Writer - Package Verification")
    print("=" * 60)
    
    all_checks_passed = True
    
    # Check version consistency
    print("\n1. Version Consistency Check")
    versions = check_version_consistency()
    
    if not versions:
        print("  ✗ No versions found!")
        all_checks_passed = False
    elif len(set(versions.values())) == 1:
        version = list(versions.values())[0]
        print(f"  ✓ Version consistent across all files: {version}")
        for file, ver in versions.items():
            print(f"    - {file}: {ver}")
    else:
        print("  ✗ Version mismatch detected!")
        for file, ver in versions.items():
            print(f"    - {file}: {ver}")
        all_checks_passed = False
    
    # Check API exports
    print("\n2. API Exports Check")
    exports = check_api_exports()
    
    if not exports:
        print("  ✗ No exports found in __all__!")
        all_checks_passed = False
    else:
        print(f"  ✓ Found {len(exports)} exported items:")
        for name in exports:
            print(f"    - {name}")
    
    # Check CLI entry point
    print("\n3. CLI Entry Point Check")
    has_cli = check_cli_entry_point()
    
    if has_cli:
        print("  ✓ CLI entry point configured: scientific-writer")
    else:
        print("  ✗ CLI entry point not found!")
        all_checks_passed = False
    
    # Check package structure
    print("\n4. Package Structure Check")
    structure = check_package_structure()
    
    missing_files = [name for name, exists in structure.items() if not exists]
    
    if not missing_files:
        print(f"  ✓ All {len(structure)} required files present")
    else:
        print(f"  ✗ Missing {len(missing_files)} file(s):")
        for name in missing_files:
            print(f"    - {name}")
        all_checks_passed = False
    
    # Summary
    print("\n" + "=" * 60)
    if all_checks_passed:
        print("✓ ALL CHECKS PASSED")
        print("=" * 60)
        print("\nPackage is ready for publishing!")
        print("\nTo publish:")
        print("  uv run scripts/publish.py --bump [major|minor|patch]")
        print("\nOr test build first:")
        print("  uv run scripts/publish.py --dry-run")
        return 0
    else:
        print("✗ SOME CHECKS FAILED")
        print("=" * 60)
        print("\nPlease fix the issues above before publishing.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

