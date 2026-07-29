"""Tests for changelog-derived GitHub release notes."""

import importlib.util
import re
from pathlib import Path

import pytest


ROOT = Path(__file__).parents[1]
SCRIPT_PATH = ROOT / "scripts" / "changelog_notes.py"
SPEC = importlib.util.spec_from_file_location("changelog_notes", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
changelog_notes = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(changelog_notes)


SAMPLE = """# Changelog

All notable changes will be documented in this file.

## [Unreleased]

---

## [2.19.0] - 2026-07-28

### Fixed

- Corrected the image model slug.

---

## [2.18.0] - 2026-07-28

### Changed

- Refreshed vendored skills.

---
"""


def test_extracts_only_the_requested_section():
    notes = changelog_notes.build_notes(SAMPLE, "2.19.0", repo_url="https://example.test/repo")

    assert "Corrected the image model slug." in notes
    assert "Refreshed vendored skills." not in notes
    assert "## [2.18.0]" not in notes
    assert not notes.startswith("---")


def test_appends_compare_link_to_previous_release():
    notes = changelog_notes.build_notes(SAMPLE, "2.19.0", repo_url="https://example.test/repo")

    assert notes.endswith("**Full Changelog**: https://example.test/repo/compare/v2.18.0...v2.19.0")


def test_oldest_release_has_no_compare_link():
    notes = changelog_notes.build_notes(SAMPLE, "2.18.0", repo_url="https://example.test/repo")

    assert "Full Changelog" not in notes


def test_existing_compare_link_is_not_duplicated():
    text = SAMPLE.replace(
        "- Corrected the image model slug.",
        "- Corrected the image model slug.\n\n**Full Changelog**: https://example.test/hand-written",
    )

    notes = changelog_notes.build_notes(text, "2.19.0", repo_url="https://example.test/repo")

    assert notes.count("Full Changelog") == 1
    assert "hand-written" in notes


def test_unreleased_section_is_not_a_valid_version():
    with pytest.raises(changelog_notes.ChangelogError):
        changelog_notes.build_notes(SAMPLE, "Unreleased")


def test_missing_section_is_rejected():
    with pytest.raises(changelog_notes.ChangelogError):
        changelog_notes.build_notes(SAMPLE, "9.9.9")


def test_empty_section_is_rejected():
    text = SAMPLE.replace("### Fixed\n\n- Corrected the image model slug.\n", "")

    with pytest.raises(changelog_notes.ChangelogError):
        changelog_notes.build_notes(text, "2.19.0")


def test_real_changelog_documents_the_current_package_version():
    """The release workflow extracts these notes, so the shipped version must have an entry."""
    match = re.search(
        r'^version\s*=\s*"([^"]+)"',
        (ROOT / "pyproject.toml").read_text(encoding="utf-8"),
        re.MULTILINE,
    )
    assert match is not None
    version = match.group(1)

    notes = changelog_notes.build_notes(
        (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"), version
    )

    assert notes.strip()
