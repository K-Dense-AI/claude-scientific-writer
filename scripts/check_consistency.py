#!/usr/bin/env python3
"""Repository consistency checks, run in CI and before publishing.

Verifies the invariants that have historically drifted:
  1. Every skill in skills/ is registered in .claude-plugin/marketplace.json (and vice versa).
  2. Every skill has a SKILL.md with valid frontmatter (name matching the directory,
     a non-empty description of sane length).
  3. Versions agree across pyproject.toml, scientific_writer/__init__.py, and marketplace.json.

Mirror synchronization (skills/ vs the two .claude copies) is checked separately by
`python scripts/sync_skills.py --check`.
"""

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
MARKETPLACE = REPO_ROOT / ".claude-plugin" / "marketplace.json"

# document-skills is a bundle whose sub-directories are the actual skills
SKILL_BUNDLE_DIRS = {"document-skills"}
MAX_DESCRIPTION_LENGTH = 1024


def parse_frontmatter(skill_md: Path) -> dict:
    """Parse the YAML-ish frontmatter of a SKILL.md into a flat dict (top-level keys only)."""
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    fields = {}
    for line in text[3:end].splitlines():
        if line.startswith((" ", "\t")) or ":" not in line:
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip().strip('"')
    return fields


def check_marketplace_coverage() -> list[str]:
    problems = []
    data = json.loads(MARKETPLACE.read_text())
    registered = set()
    for plugin in data.get("plugins", []):
        for entry in plugin.get("skills", []):
            registered.add(Path(entry).name)

    on_disk = {d.name for d in SKILLS_DIR.iterdir() if d.is_dir()}

    for missing in sorted(on_disk - registered):
        problems.append(f"skill not registered in marketplace.json: skills/{missing}")
    for phantom in sorted(registered - on_disk):
        problems.append(f"marketplace.json registers a skill that does not exist: {phantom}")
    return problems


def check_skill_frontmatter() -> list[str]:
    problems = []
    for skill_dir in sorted(d for d in SKILLS_DIR.iterdir() if d.is_dir()):
        if skill_dir.name in SKILL_BUNDLE_DIRS:
            targets = sorted(d for d in skill_dir.iterdir() if d.is_dir())
        else:
            targets = [skill_dir]
        for target in targets:
            skill_md = target / "SKILL.md"
            rel = skill_md.relative_to(REPO_ROOT)
            if not skill_md.exists():
                problems.append(f"missing SKILL.md: {rel}")
                continue
            fields = parse_frontmatter(skill_md)
            if not fields:
                problems.append(f"missing or unparsable frontmatter: {rel}")
                continue
            name = fields.get("name", "")
            if name != target.name:
                problems.append(
                    f"frontmatter name {name!r} does not match directory {target.name!r}: {rel}"
                )
            description = fields.get("description", "")
            if not description:
                problems.append(f"missing description in frontmatter: {rel}")
            elif len(description) > MAX_DESCRIPTION_LENGTH:
                problems.append(
                    f"description too long ({len(description)} > {MAX_DESCRIPTION_LENGTH} chars): {rel}"
                )
    return problems


def check_version_alignment() -> list[str]:
    problems = []
    versions = {}

    pyproject = (REPO_ROOT / "pyproject.toml").read_text()
    match = re.search(r'^version\s*=\s*"([^"]+)"', pyproject, re.MULTILINE)
    if match:
        versions["pyproject.toml"] = match.group(1)

    init_text = (REPO_ROOT / "scientific_writer" / "__init__.py").read_text()
    match = re.search(r'^__version__\s*=\s*"([^"]+)"', init_text, re.MULTILINE)
    if match:
        versions["scientific_writer/__init__.py"] = match.group(1)

    data = json.loads(MARKETPLACE.read_text())
    marketplace_version = data.get("metadata", {}).get("version")
    if marketplace_version:
        versions[".claude-plugin/marketplace.json"] = marketplace_version

    if len(versions) < 3:
        problems.append(f"could not read all three version declarations (found: {versions})")
    elif len(set(versions.values())) != 1:
        problems.append(f"version mismatch: {versions}")
    return problems


def main() -> int:
    problems = []
    problems += check_marketplace_coverage()
    problems += check_skill_frontmatter()
    problems += check_version_alignment()

    if problems:
        print(f"Found {len(problems)} consistency problem(s):")
        for problem in problems:
            print(f"  ✗ {problem}")
        return 1
    print("All consistency checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
