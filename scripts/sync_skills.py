#!/usr/bin/env python3
"""Vendor pinned writing skills from their upstream repositories and sync mirrors.

Skill content sources of truth:
    https://github.com/K-Dense-AI/scientific-agent-skills (default upstream)
    https://github.com/anthropics/skills (docx, pdf, pptx, xlsx; Apache-2.0)

The top-level repository/ref/commit in skills.lock.json is the default
upstream. A skill entry may carry its own repository/ref/commit to pin it to a
different upstream. An entry may also list "overrides": repository-local files
under skill-overrides/<destination>/ that replace upstream files after
extraction. Each override records the SHA-256 of the upstream file it replaces,
so a sync fails loudly instead of silently masking a changed upstream file.

Local generated snapshots:
    skills/
    .claude/skills/
    scientific_writer/.claude/skills/

Agent instructions remain sourced from CLAUDE.md and are mirrored to the two
WRITER.md files and the plugin initialization template.

The root Agent Plugins manifest (plugin.json) is mirrored alongside the skills
so each payload directory is itself a loadable Agent Plugin package
(https://agent-plugins.org/specification).

Usage:
    python scripts/sync_skills.py
        Download the commit pinned in skills.lock.json and regenerate snapshots.
    python scripts/sync_skills.py --check
        Verify the vendored snapshot and mirrors without network access.
    python scripts/sync_skills.py --update-ref <tag-or-commit>
        Resolve a new upstream tag/ref, refresh content, and rewrite the lock.
    python scripts/sync_skills.py --update-ref <ref> --repository <url>
        Re-pin only the skills whose effective upstream is <url>
        (for example https://github.com/anthropics/skills).
"""

import argparse
import filecmp
import hashlib
import json
import os
import shutil
import sys
import tarfile
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path, PurePosixPath
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent

SKILLS_LOCK = REPO_ROOT / "skills.lock.json"
SKILLS_SOURCE = REPO_ROOT / "skills"
SKILLS_OVERRIDES = REPO_ROOT / "skill-overrides"
SKILLS_MIRRORS = [
    REPO_ROOT / ".claude" / "skills",
    REPO_ROOT / "scientific_writer" / ".claude" / "skills",
]
SKILLS_LOCK_MIRRORS = [
    REPO_ROOT / ".claude" / "skills.lock.json",
    REPO_ROOT / "scientific_writer" / ".claude" / "skills.lock.json",
]

PLUGIN_MANIFEST = REPO_ROOT / "plugin.json"
PLUGIN_MANIFEST_MIRRORS = [
    REPO_ROOT / ".claude" / "plugin.json",
    REPO_ROOT / "scientific_writer" / ".claude" / "plugin.json",
]

INSTRUCTIONS_SOURCE = REPO_ROOT / "CLAUDE.md"
INSTRUCTIONS_MIRRORS = [
    # AGENTS.md is the vendor-neutral equivalent of CLAUDE.md; keeping it a
    # byte-identical generated mirror means the two can never drift.
    REPO_ROOT / "AGENTS.md",
    REPO_ROOT / ".claude" / "WRITER.md",
    REPO_ROOT / "scientific_writer" / ".claude" / "WRITER.md",
]
# One template per project instruction filename, written into user projects by
# the scientific-writer-init command.
INSTRUCTIONS_TEMPLATES = [
    REPO_ROOT / "templates" / "CLAUDE.scientific-writer.md",
    REPO_ROOT / "templates" / "AGENTS.scientific-writer.md",
]

IGNORE_PATTERNS = shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store")
IGNORE_NAMES = {"__pycache__", ".DS_Store"}
USER_AGENT = "claude-scientific-writer-skill-sync"
COPY_BUFFER_SIZE = 1024 * 1024


class SyncError(RuntimeError):
    """Raised when upstream skill synchronization cannot complete safely."""


def _iter_files(root: Path):
    """Yield paths relative to root for every file under it, minus ignored names."""
    for path in sorted(root.rglob("*")):
        if path.is_dir():
            continue
        rel = path.relative_to(root)
        if any(part in IGNORE_NAMES for part in rel.parts) or rel.suffix == ".pyc":
            continue
        yield rel


def _validate_relative_path(value: str, field: str) -> Path:
    """Return a safe repository-relative path from lock data."""
    path = Path(value)
    if not value or path.is_absolute() or ".." in path.parts:
        raise SyncError(f"Invalid {field} path in {SKILLS_LOCK.name}: {value!r}")
    return path


def load_lock() -> dict[str, Any]:
    """Load and validate upstream provenance and selected skill mappings."""
    try:
        data = json.loads(SKILLS_LOCK.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SyncError(f"Skill lock file not found: {SKILLS_LOCK}") from exc
    except json.JSONDecodeError as exc:
        raise SyncError(f"Invalid JSON in {SKILLS_LOCK}: {exc}") from exc

    if data.get("schema_version") != 1:
        raise SyncError(f"Unsupported schema_version in {SKILLS_LOCK.name}")
    if not isinstance(data.get("repository"), str) or not data["repository"]:
        raise SyncError(f"Missing repository in {SKILLS_LOCK.name}")
    if not isinstance(data.get("ref"), str) or not data["ref"]:
        raise SyncError(f"Missing ref in {SKILLS_LOCK.name}")
    if not isinstance(data.get("commit"), str) or len(data["commit"]) != 40:
        raise SyncError(f"Expected a 40-character commit in {SKILLS_LOCK.name}")

    entries = data.get("skills")
    if not isinstance(entries, list) or not entries:
        raise SyncError(f"No selected skills in {SKILLS_LOCK.name}")

    sources: set[str] = set()
    destinations: set[Path] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise SyncError(f"Invalid skill entry in {SKILLS_LOCK.name}: {entry!r}")
        source = entry.get("source")
        if (
            not isinstance(source, str)
            or not source
            or "/" in source
            or source in {".", ".."}
        ):
            raise SyncError(f"Invalid upstream skill name: {source!r}")
        destination = _validate_relative_path(entry.get("destination", ""), "destination")
        if source in sources:
            raise SyncError(f"Duplicate upstream skill in lock: {source}")
        if destination in destinations:
            raise SyncError(f"Duplicate local skill destination in lock: {destination}")
        _validate_entry_upstream(entry)
        _validate_entry_overrides(entry, destination)
        sources.add(source)
        destinations.add(destination)
    return data


def _validate_entry_upstream(entry: dict[str, Any]) -> None:
    """Check an entry's optional per-skill upstream pin (all three fields or none)."""
    fields = [key for key in ("repository", "ref", "commit") if key in entry]
    if not fields:
        return
    if len(fields) != 3:
        raise SyncError(
            f"Skill {entry['source']!r} must set repository, ref, and commit together "
            f"in {SKILLS_LOCK.name}"
        )
    if not isinstance(entry["repository"], str) or not entry["repository"]:
        raise SyncError(f"Missing repository for skill {entry['source']!r}")
    if not isinstance(entry["ref"], str) or not entry["ref"]:
        raise SyncError(f"Missing ref for skill {entry['source']!r}")
    if not isinstance(entry["commit"], str) or len(entry["commit"]) != 40:
        raise SyncError(f"Expected a 40-character commit for skill {entry['source']!r}")


def _validate_entry_overrides(entry: dict[str, Any], destination: Path) -> None:
    """Check an entry's optional {relative path: upstream sha256} override map."""
    overrides = entry.get("overrides")
    if overrides is None:
        return
    if not isinstance(overrides, dict) or not overrides:
        raise SyncError(f"overrides for skill {entry['source']!r} must be a non-empty mapping")
    for relative, base_sha256 in overrides.items():
        _validate_relative_path(relative, "override")
        if not isinstance(base_sha256, str) or len(base_sha256) != 64:
            raise SyncError(
                f"Override {destination}/{relative} must record the 64-character SHA-256 "
                "of the upstream file it replaces"
            )


def entry_upstream(data: dict[str, Any], entry: dict[str, Any]) -> tuple[str, str, str]:
    """Return the effective (repository, ref, commit) for one skill entry."""
    if "repository" in entry:
        return entry["repository"], entry["ref"], entry["commit"]
    return data["repository"], data["ref"], data["commit"]


def group_by_upstream(
    data: dict[str, Any],
) -> dict[tuple[str, str], list[dict[str, Any]]]:
    """Group skill entries by the (repository, commit) archive they come from."""
    groups: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for entry in data["skills"]:
        repository, _ref, commit = entry_upstream(data, entry)
        groups.setdefault((repository, commit), []).append(entry)
    return groups


def file_sha256(path: Path) -> str:
    """Return the SHA-256 of one file's contents."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(COPY_BUFFER_SIZE):
            digest.update(chunk)
    return digest.hexdigest()


def apply_overrides(
    entries: list[dict[str, Any]],
    root: Path,
    overrides_root: Path = SKILLS_OVERRIDES,
) -> None:
    """Replace upstream files in an extracted tree with repository-local overrides.

    Each override is applied only when the upstream file still has the SHA-256
    recorded in the lock, so an upstream change to an overridden file is
    surfaced instead of being silently discarded.
    """
    for entry in entries:
        destination = _validate_relative_path(entry["destination"], "destination")
        for relative, base_sha256 in (entry.get("overrides") or {}).items():
            relative_path = _validate_relative_path(relative, "override")
            source = overrides_root / destination / relative_path
            target = root / destination / relative_path
            if not source.is_file():
                raise SyncError(f"Missing override file: {source.relative_to(overrides_root.parent)}")
            if not target.is_file():
                raise SyncError(
                    f"Override target is not an upstream file: skills/{destination}/{relative}"
                )
            if file_sha256(target) != base_sha256:
                raise SyncError(
                    f"Upstream changed skills/{destination}/{relative}, which has a local "
                    "override. Re-apply the override to the new upstream file, then update "
                    "its base SHA-256 in the lock."
                )
            mode = target.stat().st_mode & 0o777
            shutil.copyfile(source, target)
            os.chmod(target, mode)


def override_problems(data: dict[str, Any], root: Path) -> list[str]:
    """Return override files that are missing or not reflected in the snapshot."""
    problems: list[str] = []
    for entry in data["skills"]:
        destination = _validate_relative_path(entry["destination"], "destination")
        for relative in entry.get("overrides") or {}:
            source = SKILLS_OVERRIDES / destination / relative
            target = root / destination / relative
            if not source.is_file():
                problems.append(f"missing override file: skill-overrides/{destination}/{relative}")
            elif not target.is_file() or not filecmp.cmp(source, target, shallow=False):
                problems.append(f"override not applied: skills/{destination}/{relative}")
    if SKILLS_OVERRIDES.is_dir():
        declared = {
            Path(entry["destination"]) / relative
            for entry in data["skills"]
            for relative in entry.get("overrides") or {}
        }
        for relative in _iter_files(SKILLS_OVERRIDES):
            if relative not in declared:
                problems.append(f"undeclared override file: skill-overrides/{relative.as_posix()}")
    return problems


def _repository_parts(repository: str) -> tuple[str, str]:
    """Extract a GitHub owner and repository name from an HTTPS URL."""
    parsed = urllib.parse.urlparse(repository)
    parts = [part for part in parsed.path.strip("/").split("/") if part]
    if parsed.scheme != "https" or parsed.netloc != "github.com" or len(parts) != 2:
        raise SyncError(f"Only GitHub HTTPS repositories are supported: {repository}")
    return parts[0], parts[1].removesuffix(".git")


def resolve_ref(repository: str, ref: str) -> str:
    """Resolve an upstream branch, tag, or SHA to an immutable commit."""
    owner, name = _repository_parts(repository)
    encoded_ref = urllib.parse.quote(ref, safe="")
    url = f"https://api.github.com/repos/{owner}/{name}/commits/{encoded_ref}"
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": USER_AGENT,
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            payload = json.load(response)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise SyncError(f"Unable to resolve upstream ref {ref!r}: {exc}") from exc

    commit = payload.get("sha")
    if not isinstance(commit, str) or len(commit) != 40:
        raise SyncError(f"GitHub returned no commit for upstream ref {ref!r}")
    return commit


def _download_archive(repository: str, commit: str, destination: Path) -> None:
    """Download the immutable upstream GitHub tarball."""
    owner, name = _repository_parts(repository)
    url = f"https://codeload.github.com/{owner}/{name}/tar.gz/{commit}"
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with (
            urllib.request.urlopen(request, timeout=180) as response,
            destination.open("wb") as output,
        ):
            shutil.copyfileobj(response, output, COPY_BUFFER_SIZE)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise SyncError(f"Unable to download upstream skills at {commit}: {exc}") from exc


def _is_ignored(parts: tuple[str, ...]) -> bool:
    """Return whether an archive member should be omitted from snapshots."""
    return any(part in IGNORE_NAMES for part in parts) or any(
        part.endswith(".pyc") for part in parts
    )


def _extract_selected_skills(
    archive: Path,
    destination: Path,
    entries: list[dict[str, Any]],
) -> None:
    """Safely extract only configured skill directories from an upstream tarball."""
    source_to_destination = {
        entry["source"]: _validate_relative_path(entry["destination"], "destination")
        for entry in entries
    }
    seen: set[str] = set()
    destination.mkdir(parents=True, exist_ok=True)

    try:
        tar = tarfile.open(archive, mode="r:gz")
    except (tarfile.TarError, OSError) as exc:
        raise SyncError(f"Unable to read upstream archive: {exc}") from exc

    with tar:
        for member in tar:
            parts = PurePosixPath(member.name).parts
            if len(parts) < 3 or parts[1] != "skills":
                continue
            source_name = parts[2]
            local_base = source_to_destination.get(source_name)
            if local_base is None:
                continue

            relative_parts = parts[3:]
            if _is_ignored(relative_parts):
                continue
            if any(part in {"", ".", ".."} for part in relative_parts):
                raise SyncError(f"Unsafe path in upstream archive: {member.name}")

            seen.add(source_name)
            target = destination / local_base
            if relative_parts:
                target = target.joinpath(*relative_parts)

            if member.isdir():
                target.mkdir(parents=True, exist_ok=True)
                continue
            if not member.isfile():
                raise SyncError(
                    f"Unsupported link or special file in upstream skill: {member.name}"
                )

            extracted = tar.extractfile(member)
            if extracted is None:
                raise SyncError(f"Unable to extract upstream file: {member.name}")
            target.parent.mkdir(parents=True, exist_ok=True)
            with extracted, target.open("wb") as output:
                shutil.copyfileobj(extracted, output, COPY_BUFFER_SIZE)
            os.chmod(target, member.mode & 0o777)

    missing = sorted(set(source_to_destination) - seen)
    if missing:
        raise SyncError(f"Upstream archive is missing selected skills: {', '.join(missing)}")
    for local_path in source_to_destination.values():
        if not (destination / local_path / "SKILL.md").is_file():
            raise SyncError(f"Selected upstream skill has no SKILL.md: {local_path}")


def hash_tree(root: Path) -> str:
    """Compute a cross-platform SHA-256 over relative paths and file contents."""
    digest = hashlib.sha256()
    for relative in _iter_files(root):
        path = root / relative
        digest.update(relative.as_posix().encode("utf-8"))
        digest.update(b"\0")
        with path.open("rb") as handle:
            while chunk := handle.read(COPY_BUFFER_SIZE):
                digest.update(chunk)
        digest.update(b"\0")
    return digest.hexdigest()


def update_hashes(data: dict[str, Any], root: Path) -> None:
    """Write deterministic content hashes into in-memory lock data."""
    for entry in data["skills"]:
        destination = _validate_relative_path(entry["destination"], "destination")
        entry["sha256"] = hash_tree(root / destination)
    data["snapshot_sha256"] = hash_tree(root)


def snapshot_problems(data: dict[str, Any], root: Path) -> list[str]:
    """Return drift between the vendored skills tree and its upstream lock."""
    problems: list[str] = []
    if not root.is_dir():
        return [f"missing generated snapshot: {root.relative_to(REPO_ROOT)}"]

    for entry in data["skills"]:
        destination = _validate_relative_path(entry["destination"], "destination")
        skill_dir = root / destination
        expected = entry.get("sha256")
        if not skill_dir.is_dir():
            problems.append(f"missing upstream skill snapshot: skills/{destination}")
        elif not isinstance(expected, str) or len(expected) != 64:
            problems.append(f"missing content hash for upstream skill: {entry['source']}")
        elif hash_tree(skill_dir) != expected:
            problems.append(f"upstream snapshot differs: skills/{destination}")

    expected_snapshot = data.get("snapshot_sha256")
    if not isinstance(expected_snapshot, str) or len(expected_snapshot) != 64:
        problems.append("missing snapshot_sha256 in skills.lock.json")
    elif hash_tree(root) != expected_snapshot:
        problems.append("skills/ contains added, removed, or modified upstream content")
    return problems


def diff_trees(source: Path, mirror: Path) -> list[str]:
    """Return human-readable drift entries between source and mirror."""
    if not mirror.exists():
        return [f"missing mirror: {mirror}"]
    source_files = set(_iter_files(source))
    mirror_files = set(_iter_files(mirror))
    drift = [f"only in source: {rel}" for rel in sorted(source_files - mirror_files)]
    drift += [f"only in mirror: {rel}" for rel in sorted(mirror_files - source_files)]
    for rel in sorted(source_files & mirror_files):
        if not filecmp.cmp(source / rel, mirror / rel, shallow=False):
            drift.append(f"differs: {rel}")
    return drift


def expected_instructions_template(template: Path | None = None) -> str:
    """Return the generated plugin template content for one instruction filename.

    The template file `templates/<NAME>.scientific-writer.md` becomes `<NAME>.md`
    in the user's project, so its header names the document it produces.
    """
    template = INSTRUCTIONS_TEMPLATES[0] if template is None else template
    document = f"{template.name.split('.', 1)[0]}.md"
    header = (
        "<!--\n"
        f"This is the Scientific Writer {document} template.\n"
        "Generated from the repository-root CLAUDE.md by scripts/sync_skills.py.\n"
        "For more information, see: https://github.com/K-Dense-AI/claude-scientific-writer\n"
        "-->\n\n"
    )
    return header + INSTRUCTIONS_SOURCE.read_text(encoding="utf-8")


def check() -> int:
    """Verify the pinned snapshot, generated mirrors, and instruction mirrors."""
    try:
        data = load_lock()
    except SyncError as exc:
        print(exc, file=sys.stderr)
        return 1

    problems = snapshot_problems(data, SKILLS_SOURCE)
    problems += override_problems(data, SKILLS_SOURCE)
    for mirror in SKILLS_MIRRORS:
        for entry in diff_trees(SKILLS_SOURCE, mirror):
            problems.append(f"{mirror.relative_to(REPO_ROOT)}: {entry}")
    for mirror in SKILLS_LOCK_MIRRORS:
        if not mirror.exists():
            problems.append(f"{mirror.relative_to(REPO_ROOT)}: missing")
        elif not filecmp.cmp(SKILLS_LOCK, mirror, shallow=False):
            problems.append(f"{mirror.relative_to(REPO_ROOT)}: differs from skills.lock.json")
    for mirror in PLUGIN_MANIFEST_MIRRORS:
        if not mirror.exists():
            problems.append(f"{mirror.relative_to(REPO_ROOT)}: missing")
        elif not filecmp.cmp(PLUGIN_MANIFEST, mirror, shallow=False):
            problems.append(f"{mirror.relative_to(REPO_ROOT)}: differs from plugin.json")
    for mirror in INSTRUCTIONS_MIRRORS:
        if not mirror.exists():
            problems.append(f"{mirror.relative_to(REPO_ROOT)}: missing")
        elif not filecmp.cmp(INSTRUCTIONS_SOURCE, mirror, shallow=False):
            problems.append(f"{mirror.relative_to(REPO_ROOT)}: differs from CLAUDE.md")
    for template in INSTRUCTIONS_TEMPLATES:
        if not template.exists():
            problems.append(f"{template.relative_to(REPO_ROOT)}: missing")
        elif template.read_text(encoding="utf-8") != expected_instructions_template(template):
            problems.append(
                f"{template.relative_to(REPO_ROOT)}: differs from generated CLAUDE.md template"
            )
    if problems:
        print("Pinned skill snapshots or mirrors are out of sync:")
        for problem in problems:
            print(f"  {problem}")
        print("\nRun `python scripts/sync_skills.py` to regenerate them.")
        return 1
    pins = ", ".join(
        f"{_repository_label(repository)} at {commit[:12]}"
        for repository, commit in group_by_upstream(data)
    )
    print(f"Pinned upstream skill snapshot and mirrors are in sync ({data['ref']}; {pins}).")
    return 0


def _repository_label(repository: str) -> str:
    """Return owner/name for a GitHub repository URL, for log messages."""
    try:
        owner, name = _repository_parts(repository)
    except SyncError:
        return repository
    return f"{owner}/{name}"


def _replace_skills_tree(staged: Path, temporary_root: Path) -> None:
    """Replace skills/ while restoring the old tree if the move fails."""
    backup = temporary_root / "previous-skills"
    if SKILLS_SOURCE.exists():
        SKILLS_SOURCE.rename(backup)
    try:
        staged.rename(SKILLS_SOURCE)
    except Exception:
        if backup.exists():
            backup.rename(SKILLS_SOURCE)
        raise
    if backup.exists():
        shutil.rmtree(backup)


def _sync_mirrors() -> None:
    """Regenerate runtime skill and instruction mirrors."""
    for mirror in SKILLS_MIRRORS:
        if mirror.exists():
            shutil.rmtree(mirror)
        shutil.copytree(SKILLS_SOURCE, mirror, ignore=IGNORE_PATTERNS)
        print(f"Synced skills/ -> {mirror.relative_to(REPO_ROOT)}")
    for mirror in SKILLS_LOCK_MIRRORS:
        mirror.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(SKILLS_LOCK, mirror)
        print(f"Synced skills.lock.json -> {mirror.relative_to(REPO_ROOT)}")
    for mirror in PLUGIN_MANIFEST_MIRRORS:
        mirror.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(PLUGIN_MANIFEST, mirror)
        print(f"Synced plugin.json -> {mirror.relative_to(REPO_ROOT)}")
    for mirror in INSTRUCTIONS_MIRRORS:
        mirror.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(INSTRUCTIONS_SOURCE, mirror)
        print(f"Synced CLAUDE.md -> {mirror.relative_to(REPO_ROOT)}")
    for template in INSTRUCTIONS_TEMPLATES:
        template.parent.mkdir(parents=True, exist_ok=True)
        template.write_text(expected_instructions_template(template), encoding="utf-8")
        print(f"Synced CLAUDE.md -> {template.relative_to(REPO_ROOT)}")


def _write_lock(data: dict[str, Any]) -> None:
    """Atomically write updated upstream provenance and hashes."""
    temporary = SKILLS_LOCK.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, SKILLS_LOCK)


def _retarget(data: dict[str, Any], update_ref: str, repository: str | None) -> int:
    """Re-pin the default upstream, or every entry on `repository`, to update_ref.

    Returns the number of re-pinned skill entries.
    """
    if repository is None or repository == data["repository"]:
        commit = resolve_ref(data["repository"], update_ref)
        data["ref"] = update_ref
        data["commit"] = commit
        return sum(1 for entry in data["skills"] if "repository" not in entry)

    matching = [entry for entry in data["skills"] if entry.get("repository") == repository]
    if not matching:
        raise SyncError(f"No skill in {SKILLS_LOCK.name} is pinned to {repository}")
    commit = resolve_ref(repository, update_ref)
    for entry in matching:
        entry["ref"] = update_ref
        entry["commit"] = commit
    return len(matching)


def sync(update_ref: str | None = None, repository: str | None = None) -> int:
    """Fetch the pinned upstream snapshots, verify them, and regenerate mirrors."""
    try:
        data = load_lock()
        if update_ref:
            count = _retarget(data, update_ref, repository)
        elif repository:
            raise SyncError("--repository requires --update-ref")

        with tempfile.TemporaryDirectory(
            prefix=".skills-sync-",
            dir=REPO_ROOT,
        ) as temporary_name:
            temporary_root = Path(temporary_name)
            staged = temporary_root / "skills"

            for index, ((upstream, commit), entries) in enumerate(group_by_upstream(data).items()):
                archive = temporary_root / f"upstream-{index}.tar.gz"
                ref = entry_upstream(data, entries[0])[1]
                print(f"Fetching {upstream} {ref} ({commit[:12]})...")
                _download_archive(upstream, commit, archive)
                _extract_selected_skills(archive, staged, entries)
                apply_overrides(entries, staged)

            if update_ref:
                update_hashes(data, staged)
            else:
                drift = snapshot_problems(data, staged)
                if drift:
                    raise SyncError(
                        "Downloaded upstream content does not match skills.lock.json:\n  "
                        + "\n  ".join(drift)
                    )

            _replace_skills_tree(staged, temporary_root)

        if update_ref:
            _write_lock(data)
            print(
                f"Updated {SKILLS_LOCK.name}: {count} skill(s) now pinned to "
                f"{update_ref} of {repository or data['repository']}"
            )
        _sync_mirrors()
        return 0
    except (OSError, SyncError) as exc:
        print(f"Skill synchronization failed: {exc}", file=sys.stderr)
        return 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument(
        "--check",
        action="store_true",
        help="verify the pinned snapshot and mirrors without network access",
    )
    actions.add_argument(
        "--update-ref",
        metavar="REF",
        help="pin and vendor a new upstream branch, tag, or commit",
    )
    parser.add_argument(
        "--repository",
        metavar="URL",
        help=(
            "with --update-ref, re-pin only the skills pinned to this upstream "
            "repository instead of the default one"
        ),
    )
    args = parser.parse_args()
    if args.check:
        if args.repository:
            parser.error("--repository cannot be combined with --check")
        return check()
    return sync(update_ref=args.update_ref, repository=args.repository)


if __name__ == "__main__":
    sys.exit(main())
