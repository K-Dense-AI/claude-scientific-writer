"""Tests for pinned upstream skill synchronization."""

import importlib.util
import io
import tarfile
from pathlib import Path

import pytest


SCRIPT_PATH = Path(__file__).parents[1] / "scripts" / "sync_skills.py"
SPEC = importlib.util.spec_from_file_location("sync_skills", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
sync_skills = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sync_skills)


def _add_file(archive: tarfile.TarFile, name: str, content: bytes) -> None:
    info = tarfile.TarInfo(name)
    info.size = len(content)
    info.mode = 0o644
    archive.addfile(info, io.BytesIO(content))


def test_extracts_only_selected_skills_with_destination_mapping(tmp_path):
    archive_path = tmp_path / "upstream.tar.gz"
    with tarfile.open(archive_path, "w:gz") as archive:
        _add_file(archive, "repo/skills/docx/SKILL.md", b"---\nname: docx\n---\n")
        _add_file(archive, "repo/skills/docx/references/guide.md", b"guide")
        _add_file(archive, "repo/skills/unselected/SKILL.md", b"not selected")

    destination = tmp_path / "skills"
    sync_skills._extract_selected_skills(
        archive_path,
        destination,
        [{"source": "docx", "destination": "document-skills/docx"}],
    )

    assert (destination / "document-skills" / "docx" / "SKILL.md").is_file()
    assert (destination / "document-skills" / "docx" / "references" / "guide.md").is_file()
    assert not (destination / "unselected").exists()


def test_rejects_links_in_selected_upstream_skill(tmp_path):
    archive_path = tmp_path / "upstream.tar.gz"
    with tarfile.open(archive_path, "w:gz") as archive:
        _add_file(archive, "repo/skills/demo/SKILL.md", b"---\nname: demo\n---\n")
        link = tarfile.TarInfo("repo/skills/demo/unsafe-link")
        link.type = tarfile.SYMTYPE
        link.linkname = "../../outside"
        archive.addfile(link)

    with pytest.raises(sync_skills.SyncError, match="Unsupported link"):
        sync_skills._extract_selected_skills(
            archive_path,
            tmp_path / "skills",
            [{"source": "demo", "destination": "demo"}],
        )


def test_snapshot_hash_detects_unexpected_local_content(tmp_path):
    root = tmp_path / "skills"
    skill = root / "demo"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("---\nname: demo\n---\n")
    lock = {
        "skills": [{"source": "demo", "destination": "demo", "sha256": ""}],
        "snapshot_sha256": "",
    }
    sync_skills.update_hashes(lock, root)

    assert sync_skills.snapshot_problems(lock, root) == []

    (root / "unexpected.txt").write_text("drift")
    assert "skills/ contains added, removed, or modified upstream content" in (
        sync_skills.snapshot_problems(lock, root)
    )
