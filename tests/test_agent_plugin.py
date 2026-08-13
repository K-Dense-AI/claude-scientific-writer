"""Tests for Agent Plugins specification conformance and the checker itself."""

import importlib.util
import json
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "validate_agent_plugin.py"
SPEC = importlib.util.spec_from_file_location("validate_agent_plugin", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)

PLUGIN_SCHEMA_ID = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
MCP_SCHEMA_ID = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"

MINIMAL_MANIFEST = {"$schema": PLUGIN_SCHEMA_ID, "name": "hello-plugin"}


def errors(diagnostics):
    """Return the error-level messages from a diagnostic list."""
    return [f"{d.location}: {d.message}" for d in diagnostics if d.level == "error"]


def warnings(diagnostics):
    """Return the warning-level messages from a diagnostic list."""
    return [f"{d.location}: {d.message}" for d in diagnostics if d.level == "warning"]


def build_plugin(root: Path, manifest=None, skills=None, mcp=None) -> Path:
    """Write a plugin package to root and return it."""
    root.mkdir(parents=True, exist_ok=True)
    (root / "plugin.json").write_text(json.dumps(MINIMAL_MANIFEST if manifest is None else manifest))
    for name, frontmatter in (skills or {}).items():
        skill_dir = root / "skills" / name
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "SKILL.md").write_text(f"---\n{frontmatter}\n---\n\nBody.\n")
    if mcp is not None:
        (root / "mcp.json").write_text(json.dumps(mcp))
    return root


# --------------------------------------------------------------------------
# This repository
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "root",
    [REPO_ROOT, REPO_ROOT / ".claude", REPO_ROOT / "scientific_writer" / ".claude"],
    ids=["repository", "claude-payload", "package-payload"],
)
def test_shipped_plugin_roots_conform(root):
    assert errors(validator.validate_plugin(root)) == []


def test_shipped_manifest_version_matches_pyproject():
    manifest = json.loads((REPO_ROOT / "plugin.json").read_text())
    pyproject = (REPO_ROOT / "pyproject.toml").read_text()
    assert f'version = "{manifest["version"]}"' in pyproject


def test_every_repository_skill_is_discoverable():
    diagnostics = validator.check_skills(REPO_ROOT)
    discovered = next(d for d in diagnostics if d.level == "info")
    on_disk = [
        directory
        for directory in (REPO_ROOT / "skills").iterdir()
        if directory.is_dir() and (directory / "SKILL.md").is_file()
    ]
    assert discovered.message == f"{len(on_disk)} skill(s) discoverable"


# --------------------------------------------------------------------------
# Manifest rules (spec section 5)
# --------------------------------------------------------------------------


def test_missing_manifest_rejects_the_plugin(tmp_path):
    (tmp_path / "skills" / "greet").mkdir(parents=True)
    (tmp_path / "skills" / "greet" / "SKILL.md").write_text("---\nname: greet\ndescription: Hi.\n---\n")
    diagnostics = validator.validate_plugin(tmp_path)
    assert any("manifest is missing" in message for message in errors(diagnostics))
    # A rejected plugin has no components discovered.
    assert not any(d.location.startswith("skills") for d in diagnostics)


def test_unsupported_spec_version_is_rejected(tmp_path):
    root = build_plugin(
        tmp_path, manifest={"$schema": "https://agent-plugins.org/schemas/9.9.9/plugin.schema.json", "name": "x"}
    )
    assert any("unsupported Agent Plugins version" in message for message in errors(validator.validate_plugin(root)))


def test_invalid_name_is_rejected(tmp_path):
    for bad in ["My-Plugin", "-start", "has--double", "too.many..dots", ""]:
        root = build_plugin(tmp_path / bad.replace(".", "_") or "empty", manifest={"$schema": PLUGIN_SCHEMA_ID, "name": bad})
        assert errors(validator.validate_plugin(root)), f"expected {bad!r} to be rejected"


def test_valid_names_are_accepted(tmp_path):
    for good in ["my-plugin", "acme.tools", "lint3r", "a"]:
        root = build_plugin(tmp_path / good, manifest={"$schema": PLUGIN_SCHEMA_ID, "name": good})
        assert errors(validator.validate_plugin(root)) == []


def test_unknown_top_level_field_is_reported_but_not_fatal(tmp_path):
    root = build_plugin(tmp_path, manifest={**MINIMAL_MANIFEST, "commands": ["./commands"]})
    diagnostics = validator.validate_plugin(root)
    assert errors(diagnostics) == []
    assert any("unknown top-level field 'commands'" in message for message in warnings(diagnostics))


def test_non_object_extensions_is_reported_but_not_fatal(tmp_path):
    root = build_plugin(tmp_path, manifest={**MINIMAL_MANIFEST, "extensions": "nope"})
    diagnostics = validator.validate_plugin(root)
    assert errors(diagnostics) == []
    assert any("'extensions' is not an object" in message for message in warnings(diagnostics))


def test_extension_namespace_must_be_reverse_domain(tmp_path):
    root = build_plugin(tmp_path, manifest={**MINIMAL_MANIFEST, "extensions": {"myclient": {"a": 1}}})
    assert any("reverse-domain identifier" in message for message in warnings(validator.validate_plugin(root)))


def test_reverse_domain_extension_namespace_is_accepted(tmp_path):
    manifest = {**MINIMAL_MANIFEST, "extensions": {"com.example.client": {"setting": True}}}
    root = build_plugin(tmp_path, manifest=manifest)
    diagnostics = validator.validate_plugin(root)
    assert errors(diagnostics) == []
    assert warnings(diagnostics) == []


def test_author_object_rejects_unknown_fields(tmp_path):
    manifest = {**MINIMAL_MANIFEST, "author": {"name": "K-Dense Inc.", "github": "k-dense"}}
    root = build_plugin(tmp_path, manifest=manifest)
    assert any("unknown field" in message for message in errors(validator.validate_plugin(root)))


# --------------------------------------------------------------------------
# Skills discovery (spec section 7.1)
# --------------------------------------------------------------------------


def test_nested_skills_are_not_discovered(tmp_path):
    root = build_plugin(tmp_path)
    nested = root / "skills" / "bundle" / "docx"
    nested.mkdir(parents=True)
    (nested / "SKILL.md").write_text("---\nname: docx\ndescription: Word files.\n---\n")
    diagnostics = validator.validate_plugin(root)
    assert errors(diagnostics) == []
    assert any("nested skills are not discovered: docx" in message for message in warnings(diagnostics))


def test_skill_name_must_match_directory(tmp_path):
    root = build_plugin(tmp_path, skills={"greet": "name: hello\ndescription: Say hi."})
    assert any("does not match its directory" in message for message in errors(validator.validate_plugin(root)))


def test_skill_description_length_is_enforced(tmp_path):
    long_description = "x" * 1025
    root = build_plugin(tmp_path, skills={"greet": f"name: greet\ndescription: {long_description}"})
    assert any("maximum 1024" in message for message in errors(validator.validate_plugin(root)))


def test_skill_metadata_mapping_is_parsed(tmp_path):
    frontmatter = 'name: greet\ndescription: "Say \\"hi\\" politely."\nmetadata:\n  version: "1.0"'
    root = build_plugin(tmp_path, skills={"greet": frontmatter})
    assert errors(validator.validate_plugin(root)) == []
    fields, problems = validator.parse_frontmatter(
        (root / "skills" / "greet" / "SKILL.md").read_text()
    )
    assert problems == []
    assert fields["description"] == 'Say "hi" politely.'
    assert fields["metadata"] == {"version": "1.0"}


def test_invalid_skill_does_not_invalidate_the_plugin(tmp_path):
    root = build_plugin(
        tmp_path,
        skills={"broken": "name: broken", "good": "name: good\ndescription: Fine."},
    )
    diagnostics = validator.validate_plugin(root)
    assert any("missing a non-empty 'description'" in message for message in errors(diagnostics))
    assert any(d.level == "info" and d.message == "2 skill(s) discoverable" for d in diagnostics)


def test_skills_path_that_is_not_a_directory_invalidates_the_component(tmp_path):
    root = build_plugin(tmp_path)
    (root / "skills").write_text("not a directory")
    assert any("is not a directory" in message for message in errors(validator.validate_plugin(root)))


# --------------------------------------------------------------------------
# MCP servers (spec sections 7.2 and 9)
# --------------------------------------------------------------------------


def test_valid_mcp_document_passes(tmp_path):
    mcp = {
        "$schema": MCP_SCHEMA_ID,
        "mcpServers": {
            "local": {"type": "stdio", "command": "./bin/server", "cwd": "${PLUGIN_DATA}/state"},
            "remote": {"type": "streamable-http", "url": "https://example.com/mcp"},
        },
    }
    root = build_plugin(tmp_path, mcp=mcp)
    diagnostics = validator.validate_plugin(root)
    assert errors(diagnostics) == []
    assert any(d.level == "info" and d.message == "2 MCP server(s) declared" for d in diagnostics)


def test_mcp_command_escaping_the_plugin_root_is_rejected(tmp_path):
    mcp = {"$schema": MCP_SCHEMA_ID, "mcpServers": {"s": {"type": "stdio", "command": "../bin/server"}}}
    root = build_plugin(tmp_path, mcp=mcp)
    assert any("bare executable token or a './' path" in message for message in errors(validator.validate_plugin(root)))


def test_mcp_relative_command_leaving_root_is_rejected(tmp_path):
    mcp = {"$schema": MCP_SCHEMA_ID, "mcpServers": {"s": {"type": "stdio", "command": "./../server"}}}
    root = build_plugin(tmp_path, mcp=mcp)
    assert any("resolves outside the plugin root" in message for message in errors(validator.validate_plugin(root)))


def test_mcp_reserved_env_names_are_rejected(tmp_path):
    mcp = {
        "$schema": MCP_SCHEMA_ID,
        "mcpServers": {"s": {"type": "stdio", "command": "server", "env": {"PLUGIN_ROOT": "/tmp"}}},
    }
    root = build_plugin(tmp_path, mcp=mcp)
    assert any("property name is not allowed" in message for message in errors(validator.validate_plugin(root)))


def test_mcp_unknown_transport_is_rejected(tmp_path):
    mcp = {"$schema": MCP_SCHEMA_ID, "mcpServers": {"s": {"type": "websocket", "url": "wss://example.com"}}}
    root = build_plugin(tmp_path, mcp=mcp)
    assert any("must match exactly one of" in message for message in errors(validator.validate_plugin(root)))


def test_unexpandable_placeholder_is_warned(tmp_path):
    mcp = {
        "$schema": MCP_SCHEMA_ID,
        "mcpServers": {"s": {"type": "stdio", "command": "server", "args": ["--home=${HOME}"]}},
    }
    root = build_plugin(tmp_path, mcp=mcp)
    diagnostics = validator.validate_plugin(root)
    assert errors(diagnostics) == []
    assert any("${HOME}" in message for message in warnings(diagnostics))


def test_mcp_json_that_is_not_a_file_invalidates_the_component(tmp_path):
    root = build_plugin(tmp_path)
    (root / "mcp.json").mkdir()
    assert any("not a regular file" in message for message in errors(validator.validate_plugin(root)))


# --------------------------------------------------------------------------
# Schema loading
# --------------------------------------------------------------------------


def test_vendored_schemas_declare_their_canonical_ids():
    for schema_id in (PLUGIN_SCHEMA_ID, MCP_SCHEMA_ID):
        version, schema = validator.load_vendored_schema(schema_id)
        assert version == "1.0.0"
        assert schema["$id"] == schema_id


def test_non_canonical_schema_id_is_rejected():
    with pytest.raises(ValueError):
        validator.load_vendored_schema("https://example.com/plugin.schema.json")
