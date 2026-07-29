#!/usr/bin/env python3
"""Extract GitHub release notes for one version out of CHANGELOG.md.

Used by .github/workflows/release.yml so the GitHub release body is the changelog
entry itself, rather than prose written by hand after the tag is already pushed.
Historically that manual step was skipped and the releases page went stale while
PyPI was current.

The extracted notes are the body of the `## [X.Y.Z]` section, with a compare link
to the preceding released version appended when one exists.

Usage:
    python scripts/changelog_notes.py 2.19.0
        Print the notes for 2.19.0 to stdout.
    python scripts/changelog_notes.py 2.19.0 --output release-notes.md
        Write the notes to a file.
"""

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CHANGELOG = REPO_ROOT / "CHANGELOG.md"
DEFAULT_REPO_URL = "https://github.com/K-Dense-AI/claude-scientific-writer"

SECTION_HEADING = re.compile(r"^##\s+\[([^\]]+)\]", re.MULTILINE)
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")


class ChangelogError(RuntimeError):
    """Raised when a version has no usable changelog entry."""


def iter_sections(text: str) -> list[tuple[str, str]]:
    """Return (label, body) for every `## [label]` section, in document order."""
    matches = list(SECTION_HEADING.finditer(text))
    sections = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[match.end() : end]
        # Drop the remainder of the heading line (the ` - YYYY-MM-DD` date suffix).
        _, _, body = body.partition("\n")
        sections.append((match.group(1), _strip_separators(body)))
    return sections


def _strip_separators(body: str) -> str:
    """Strip surrounding whitespace and the `---` rules that divide changelog entries."""
    lines = body.strip().splitlines()
    while lines and lines[-1].strip() in {"", "---"}:
        lines.pop()
    while lines and lines[0].strip() in {"", "---"}:
        lines.pop(0)
    return "\n".join(lines).strip()


def previous_version(text: str, version: str) -> str | None:
    """Return the released version documented directly below `version`, if any."""
    labels = [label for label, _ in iter_sections(text)]
    if version not in labels:
        return None
    for label in labels[labels.index(version) + 1 :]:
        if SEMVER.match(label):
            return label
    return None


def build_notes(text: str, version: str, repo_url: str = DEFAULT_REPO_URL) -> str:
    """Build the release body for `version`, appending a compare link when possible.

    Raises
    ------
    ChangelogError
        If the version has no section, or its section has no content. Failing here
        keeps the workflow from publishing a release with an empty body.
    """
    if not SEMVER.match(version):
        raise ChangelogError(f"not a semantic version: {version!r}")

    sections = dict(iter_sections(text))
    if version not in sections:
        raise ChangelogError(f"{CHANGELOG.name} has no '## [{version}]' section")

    body = sections[version]
    if not body:
        raise ChangelogError(f"the '## [{version}]' section in {CHANGELOG.name} is empty")

    if "Full Changelog" in body:
        return body

    previous = previous_version(text, version)
    if previous is None:
        return body
    compare = f"{repo_url}/compare/v{previous}...v{version}"
    return f"{body}\n\n**Full Changelog**: {compare}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("version", help="version to extract, without a leading 'v'")
    parser.add_argument("--output", type=Path, help="write to this file instead of stdout")
    parser.add_argument(
        "--changelog",
        type=Path,
        default=CHANGELOG,
        help=f"changelog to read (default: {CHANGELOG.name})",
    )
    parser.add_argument(
        "--repo-url",
        default=DEFAULT_REPO_URL,
        help="repository URL used to build the compare link",
    )
    args = parser.parse_args()

    version = args.version.removeprefix("v")
    try:
        notes = build_notes(
            args.changelog.read_text(encoding="utf-8"), version, repo_url=args.repo_url
        )
    except (ChangelogError, OSError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    if args.output:
        args.output.write_text(notes + "\n", encoding="utf-8")
        print(f"Wrote {len(notes.splitlines())} line(s) of release notes to {args.output}")
    else:
        print(notes)
    return 0


if __name__ == "__main__":
    sys.exit(main())
