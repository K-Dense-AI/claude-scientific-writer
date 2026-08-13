"""Tests for scientific_writer.core."""

import asyncio
from pathlib import Path

import pytest

from scientific_writer.core import (
    create_completion_check_stop_hook,
    create_output_project,
    ensure_output_folder,
    find_bundled_agent_dir,
    find_instructions_file,
    get_data_files,
    load_system_instructions,
    process_data_files,
    resolve_agent_dirs,
    resolve_auto_continue,
    setup_claude_skills,
)


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


def test_agents_dir_receives_the_payload_when_the_project_uses_it(tmp_path):
    """Projects that adopted the vendor-neutral .agents/ layout get the same skills."""
    package_dir = tmp_path / "package"
    work_dir = tmp_path / "work"
    package_dir.mkdir()
    _make_bundled_claude(package_dir, "writer v2", "skill v2")
    (work_dir / ".agents").mkdir(parents=True)

    setup_claude_skills(package_dir, work_dir)

    for agent_dir in (".claude", ".agents"):
        assert (work_dir / agent_dir / "WRITER.md").read_text() == "writer v2"
        assert (work_dir / agent_dir / "skills" / "demo-skill" / "SKILL.md").read_text() == "skill v2"


def test_agents_dir_is_not_created_when_absent(tmp_path):
    """A project without .agents/ does not suddenly grow one."""
    package_dir = tmp_path / "package"
    work_dir = tmp_path / "work"
    package_dir.mkdir()
    work_dir.mkdir()
    _make_bundled_claude(package_dir, "writer v2", "skill v2")

    setup_claude_skills(package_dir, work_dir)

    assert resolve_agent_dirs(work_dir) == [work_dir / ".claude"]
    assert not (work_dir / ".agents").exists()


def test_bundled_payload_can_be_shipped_as_dot_agents(tmp_path):
    package_dir = tmp_path / "package"
    work_dir = tmp_path / "work"
    (package_dir / ".agents" / "skills" / "demo-skill").mkdir(parents=True)
    (package_dir / ".agents" / "WRITER.md").write_text("writer v3")
    (package_dir / ".agents" / "skills" / "demo-skill" / "SKILL.md").write_text("skill v3")

    assert find_bundled_agent_dir(package_dir) == package_dir / ".agents"

    setup_claude_skills(package_dir, work_dir)

    assert (work_dir / ".claude" / "WRITER.md").read_text() == "writer v3"


def test_plugin_manifest_is_refreshed_on_upgrade(tmp_path):
    package_dir = tmp_path / "package"
    work_dir = tmp_path / "work"
    package_dir.mkdir()
    _make_bundled_claude(package_dir, "writer v2", "skill v2")
    (package_dir / ".claude" / "plugin.json").write_text('{"name": "v2"}')
    (work_dir / ".claude").mkdir(parents=True)
    (work_dir / ".claude" / "plugin.json").write_text('{"name": "v1"}')

    setup_claude_skills(package_dir, work_dir)

    assert (work_dir / ".claude" / "plugin.json").read_text() == '{"name": "v2"}'


def test_instructions_are_found_across_layouts(tmp_path):
    """.claude/ wins over .agents/, which wins over root AGENTS.md and CLAUDE.md."""
    work_dir = tmp_path / "work"
    work_dir.mkdir()
    assert find_instructions_file(work_dir) is None

    (work_dir / "CLAUDE.md").write_text("root claude")
    assert load_system_instructions(work_dir) == "root claude"

    (work_dir / "AGENTS.md").write_text("root agents")
    assert load_system_instructions(work_dir) == "root agents"

    (work_dir / ".agents").mkdir()
    (work_dir / ".agents" / "WRITER.md").write_text("agents writer")
    assert load_system_instructions(work_dir) == "agents writer"

    (work_dir / ".claude").mkdir()
    (work_dir / ".claude" / "WRITER.md").write_text("claude writer")
    assert load_system_instructions(work_dir) == "claude writer"


def test_missing_instructions_fall_back_with_a_warning(tmp_path, caplog):
    work_dir = tmp_path / "work"
    work_dir.mkdir()

    with caplog.at_level("WARNING", logger="scientific_writer.core"):
        instructions = load_system_instructions(work_dir)

    assert "scientific writing assistant" in instructions
    assert any("AGENTS.md" in record.getMessage() for record in caplog.records)


def test_missing_bundle_logs_warning_instead_of_silence(tmp_path, caplog):
    package_dir = tmp_path / "package"  # no .claude inside
    work_dir = tmp_path / "work"
    package_dir.mkdir()
    work_dir.mkdir()

    with caplog.at_level("WARNING", logger="scientific_writer.core"):
        setup_claude_skills(package_dir, work_dir)

    assert any("claude" in record.message.lower() for record in caplog.records)


def test_stop_hook_blocks_once_then_allows_stop():
    hook = create_completion_check_stop_hook(auto_continue=True, max_continuations=1)

    first = asyncio.run(
        hook({"hook_event_name": "Stop", "stop_hook_active": False}, None, {})
    )
    second = asyncio.run(
        hook({"hook_event_name": "Stop", "stop_hook_active": False}, None, {})
    )

    assert first["decision"] == "block"
    assert "verify" in first["reason"]
    assert second == {}


def test_stop_hook_disabled_allows_stop():
    hook = create_completion_check_stop_hook(auto_continue=False)
    assert (
        asyncio.run(
            hook({"hook_event_name": "Stop", "stop_hook_active": False}, None, {})
        )
        == {}
    )


def test_resolve_auto_continue_environment_override():
    assert resolve_auto_continue(True, {"SCIENTIFIC_WRITER_AUTO_CONTINUE": "false"}) is False
    assert resolve_auto_continue(False, {"SCIENTIFIC_WRITER_AUTO_CONTINUE": "yes"}) is True
    assert resolve_auto_continue(False, {}) is False


def test_relative_output_folder_is_anchored_to_cwd(tmp_path):
    assert ensure_output_folder(tmp_path, "custom") == (tmp_path / "custom").resolve()


def test_create_output_project_is_collision_safe(tmp_path):
    first = create_output_project(tmp_path, "Create a concise report")
    second = create_output_project(tmp_path, "Create a concise report")

    assert first != second
    for project in (first, second):
        assert {path.name for path in project.iterdir()} == {
            "data",
            "drafts",
            "figures",
            "final",
            "references",
            "sources",
        }


def test_explicit_data_files_resolve_against_cwd(tmp_path):
    source = tmp_path / "results.csv"
    source.write_text("value\n1\n")

    assert get_data_files(tmp_path, ["results.csv"]) == [source.resolve()]
    with pytest.raises(FileNotFoundError):
        get_data_files(tmp_path, ["missing.csv"])


def test_process_data_files_preserves_inputs_and_avoids_collisions(tmp_path):
    source = tmp_path / "results.csv"
    source.write_text("value\n1\n")
    project = tmp_path / "project"

    first = process_data_files(tmp_path, [source], str(project))
    second = process_data_files(tmp_path, [source], str(project))

    assert source.exists()
    assert first is not None and first["errors"] == []
    assert second is not None and second["errors"] == []
    assert (project / "data" / "results.csv").read_text() == source.read_text()
    assert (project / "data" / "results_2.csv").read_text() == source.read_text()


def test_process_data_files_only_reports_successful_copies(tmp_path):
    missing = tmp_path / "missing.csv"
    result = process_data_files(tmp_path, [missing], str(tmp_path / "project"))

    assert result is not None
    assert result["all_files"] == []
    assert result["data_files"] == []
    assert result["errors"]
