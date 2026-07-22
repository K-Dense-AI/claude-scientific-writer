"""Tests for scientific_writer.core."""

from pathlib import Path

from scientific_writer.core import setup_claude_skills


def _make_bundled_claude(package_dir: Path, writer_text: str, skill_text: str) -> None:
    """Create a minimal bundled .claude payload like the one shipped in the wheel."""
    claude = package_dir / ".claude"
    (claude / "skills" / "demo-skill").mkdir(parents=True)
    (claude / "WRITER.md").write_text(writer_text)
    (claude / "skills.lock.json").write_text('{"commit": "upstream-v2"}')
    (claude / "skills" / "demo-skill" / "SKILL.md").write_text(skill_text)


def test_copies_claude_dir_when_missing(tmp_path):
    package_dir = tmp_path / "package"
    work_dir = tmp_path / "work"
    package_dir.mkdir()
    work_dir.mkdir()
    _make_bundled_claude(package_dir, "writer v2", "skill v2")

    setup_claude_skills(package_dir, work_dir)

    assert (work_dir / ".claude" / "WRITER.md").read_text() == "writer v2"
    assert (work_dir / ".claude" / "skills.lock.json").read_text() == '{"commit": "upstream-v2"}'
    assert (work_dir / ".claude" / "skills" / "demo-skill" / "SKILL.md").read_text() == "skill v2"


def test_refreshes_bundled_skills_when_claude_exists(tmp_path):
    """A pre-existing .claude dir (very common for Claude Code users) must still
    receive the bundled WRITER.md and skills, refreshed to the packaged version."""
    package_dir = tmp_path / "package"
    work_dir = tmp_path / "work"
    package_dir.mkdir()
    _make_bundled_claude(package_dir, "writer v2", "skill v2")

    stale = work_dir / ".claude"
    (stale / "skills" / "demo-skill").mkdir(parents=True)
    (stale / "WRITER.md").write_text("writer v1")
    (stale / "skills.lock.json").write_text('{"commit": "upstream-v1"}')
    (stale / "skills" / "demo-skill" / "SKILL.md").write_text("skill v1")
    (stale / "skills" / "demo-skill" / "leftover.md").write_text("obsolete")

    setup_claude_skills(package_dir, work_dir)

    assert (work_dir / ".claude" / "WRITER.md").read_text() == "writer v2"
    assert (work_dir / ".claude" / "skills.lock.json").read_text() == '{"commit": "upstream-v2"}'
    assert (work_dir / ".claude" / "skills" / "demo-skill" / "SKILL.md").read_text() == "skill v2"
    # Bundled skill dirs are replaced wholesale so stale files don't linger
    assert not (work_dir / ".claude" / "skills" / "demo-skill" / "leftover.md").exists()


def test_preserves_user_files_when_refreshing(tmp_path):
    """User-owned content in .claude (settings, custom skills) must survive a refresh."""
    package_dir = tmp_path / "package"
    work_dir = tmp_path / "work"
    package_dir.mkdir()
    _make_bundled_claude(package_dir, "writer v2", "skill v2")

    existing = work_dir / ".claude"
    (existing / "skills" / "my-custom-skill").mkdir(parents=True)
    (existing / "settings.json").write_text('{"theme": "dark"}')
    (existing / "skills" / "my-custom-skill" / "SKILL.md").write_text("mine")

    setup_claude_skills(package_dir, work_dir)

    assert (work_dir / ".claude" / "settings.json").read_text() == '{"theme": "dark"}'
    assert (work_dir / ".claude" / "skills" / "my-custom-skill" / "SKILL.md").read_text() == "mine"
    # And the bundled content still arrived
    assert (work_dir / ".claude" / "WRITER.md").read_text() == "writer v2"
    assert (work_dir / ".claude" / "skills" / "demo-skill" / "SKILL.md").read_text() == "skill v2"


def test_missing_bundle_logs_warning_instead_of_silence(tmp_path, caplog):
    package_dir = tmp_path / "package"  # no .claude inside
    work_dir = tmp_path / "work"
    package_dir.mkdir()
    work_dir.mkdir()

    with caplog.at_level("WARNING", logger="scientific_writer.core"):
        setup_claude_skills(package_dir, work_dir)

    assert any("claude" in record.message.lower() for record in caplog.records)
