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


def test_entries_group_by_their_effective_upstream():
    lock = {
        "repository": "https://github.com/K-Dense-AI/scientific-agent-skills",
        "ref": "v1",
        "commit": "a" * 40,
        "skills": [
            {"source": "writing", "destination": "writing"},
            {
                "source": "docx",
                "destination": "docx",
                "repository": "https://github.com/anthropics/skills",
                "ref": "main",
                "commit": "b" * 40,
            },
        ],
    }

    groups = sync_skills.group_by_upstream(lock)

    assert [entry["source"] for entry in groups[(lock["repository"], "a" * 40)]] == ["writing"]
    assert [entry["source"] for entry in groups[("https://github.com/anthropics/skills", "b" * 40)]] == [
        "docx"
    ]


def test_partial_per_skill_upstream_pin_is_rejected():
    with pytest.raises(sync_skills.SyncError, match="repository, ref, and commit together"):
        sync_skills._validate_entry_upstream(
            {"source": "docx", "repository": "https://github.com/anthropics/skills"}
        )


def _override_fixture(tmp_path):
    upstream = tmp_path / "skills" / "docx" / "scripts"
    upstream.mkdir(parents=True)
    (upstream / "tool.py").write_text("upstream\n")
    (upstream / "tool.py").chmod(0o755)
    overrides = tmp_path / "skill-overrides" / "docx" / "scripts"
    overrides.mkdir(parents=True)
    (overrides / "tool.py").write_text("local\n")
    entry = {
        "source": "docx",
        "destination": "docx",
        "overrides": {"scripts/tool.py": sync_skills.file_sha256(upstream / "tool.py")},
    }
    return entry, tmp_path / "skills", tmp_path / "skill-overrides"


def test_override_replaces_upstream_file_and_keeps_its_mode(tmp_path):
    entry, root, overrides_root = _override_fixture(tmp_path)

    sync_skills.apply_overrides([entry], root, overrides_root)

    target = root / "docx" / "scripts" / "tool.py"
    assert target.read_text() == "local\n"
    assert target.stat().st_mode & 0o777 == 0o755


def test_override_refuses_to_mask_a_changed_upstream_file(tmp_path):
    entry, root, overrides_root = _override_fixture(tmp_path)
    (root / "docx" / "scripts" / "tool.py").write_text("upstream changed\n")

    with pytest.raises(sync_skills.SyncError, match="Upstream changed skills/docx/scripts/tool.py"):
        sync_skills.apply_overrides([entry], root, overrides_root)


def test_locked_overrides_are_applied_to_the_vendored_snapshot():
    data = sync_skills.load_lock()

    assert sync_skills.override_problems(data, sync_skills.SKILLS_SOURCE) == []


def test_apache_licensed_skills_ship_their_license_text():
    data = sync_skills.load_lock()
    apache = [entry for entry in data["skills"] if entry.get("license") == "Apache-2.0"]

    assert sorted(entry["source"] for entry in apache) == ["docx", "pdf", "pptx", "xlsx"]
    for entry in apache:
        skill = sync_skills.SKILLS_SOURCE / entry["destination"]
        license_text = (skill / "LICENSE.txt").read_text(encoding="utf-8")
        assert license_text.lstrip().startswith("Apache License")
        assert "Version 2.0, January 2004" in license_text
        assert "license: Complete terms in LICENSE.txt" in (skill / "SKILL.md").read_text(encoding="utf-8")
