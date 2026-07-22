#!/usr/bin/env python3
"""Vendor pinned writing skills from scientific-agent-skills and sync mirrors.

Skill content source of truth:
    https://github.com/K-Dense-AI/scientific-agent-skills

Local generated snapshots:
    skills/
    .claude/skills/
    scientific_writer/.claude/skills/

Agent instructions remain sourced from CLAUDE.md and are mirrored to the two
WRITER.md files.

Usage:
    python scripts/sync_skills.py
        Download the commit pinned in skills.lock.json and regenerate snapshots.
    python scripts/sync_skills.py --check
        Verify the vendored snapshot and mirrors without network access.
    python scripts/sync_skills.py --update-ref v2.55.0
        Resolve a new upstream tag/ref, refresh content, and rewrite the lock.
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
SKILLS_MIRRORS = [
    REPO_ROOT / ".claude" / "skills",
    REPO_ROOT / "scientific_writer" / ".claude" / "skills",
]
SKILLS_LOCK_MIRRORS = [
    REPO_ROOT / ".claude" / "skills.lock.json",
    REPO_ROOT / "scientific_writer" / ".claude" / "skills.lock.json",
]

INSTRUCTIONS_SOURCE = REPO_ROOT / "CLAUDE.md"
INSTRUCTIONS_MIRRORS = [
    REPO_ROOT / ".claude" / "WRITER.md",
    REPO_ROOT / "scientific_writer" / ".claude" / "WRITER.md",
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
        sources.add(source)
        destinations.add(destination)
    return data


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


def check() -> int:
    """Verify the pinned snapshot, generated mirrors, and instruction mirrors."""
    try:
        data = load_lock()
    except SyncError as exc:
        print(exc, file=sys.stderr)
        return 1

    problems = snapshot_problems(data, SKILLS_SOURCE)
    for mirror in SKILLS_MIRRORS:
        for entry in diff_trees(SKILLS_SOURCE, mirror):
            problems.append(f"{mirror.relative_to(REPO_ROOT)}: {entry}")
    for mirror in SKILLS_LOCK_MIRRORS:
        if not mirror.exists():
            problems.append(f"{mirror.relative_to(REPO_ROOT)}: missing")
        elif not filecmp.cmp(SKILLS_LOCK, mirror, shallow=False):
            problems.append(f"{mirror.relative_to(REPO_ROOT)}: differs from skills.lock.json")
    for mirror in INSTRUCTIONS_MIRRORS:
        if not mirror.exists():
            problems.append(f"{mirror.relative_to(REPO_ROOT)}: missing")
        elif not filecmp.cmp(INSTRUCTIONS_SOURCE, mirror, shallow=False):
            problems.append(f"{mirror.relative_to(REPO_ROOT)}: differs from CLAUDE.md")
    if problems:
        print("Pinned skill snapshots or mirrors are out of sync:")
        for problem in problems:
            print(f"  {problem}")
        print("\nRun `python scripts/sync_skills.py` to regenerate them.")
        return 1
    print(
        "Pinned upstream skill snapshot and mirrors are in sync "
        f"({data['ref']} at {data['commit'][:12]})."
    )
    return 0


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
    for mirror in INSTRUCTIONS_MIRRORS:
        mirror.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(INSTRUCTIONS_SOURCE, mirror)
        print(f"Synced CLAUDE.md -> {mirror.relative_to(REPO_ROOT)}")


def _write_lock(data: dict[str, Any]) -> None:
    """Atomically write updated upstream provenance and hashes."""
    temporary = SKILLS_LOCK.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, SKILLS_LOCK)


def sync(update_ref: str | None = None) -> int:
    """Fetch the pinned upstream snapshot, verify it, and regenerate mirrors."""
    try:
        data = load_lock()
        if update_ref:
            data["ref"] = update_ref
            data["commit"] = resolve_ref(data["repository"], update_ref)

        with tempfile.TemporaryDirectory(
            prefix=".skills-sync-",
            dir=REPO_ROOT,
        ) as temporary_name:
            temporary_root = Path(temporary_name)
            archive = temporary_root / "upstream.tar.gz"
            staged = temporary_root / "skills"

            print(
                f"Fetching {data['repository']} {data['ref']} "
                f"({data['commit'][:12]})..."
            )
            _download_archive(data["repository"], data["commit"], archive)
            _extract_selected_skills(archive, staged, data["skills"])

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
            print(f"Updated {SKILLS_LOCK.name} to {data['ref']} ({data['commit']})")
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
    args = parser.parse_args()
    return check() if args.check else sync(update_ref=args.update_ref)


if __name__ == "__main__":
    sys.exit(main())
