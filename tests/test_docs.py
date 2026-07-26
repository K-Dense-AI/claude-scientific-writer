"""Regression tests for documentation and generated instruction consistency."""

import importlib.util
from pathlib import Path
import re
from urllib.parse import unquote


ROOT = Path(__file__).parents[1]
SYNC_SCRIPT = ROOT / "scripts" / "sync_skills.py"


def _load_sync_module():
    spec = importlib.util.spec_from_file_location("sync_skills_docs", SYNC_SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_documented_example_files_exist():
    assert (ROOT / "example_api_usage.py").is_file()
    assert (ROOT / "docs" / "examples" / "grants" / "NSF_draft1.pdf").is_file()


def test_plugin_template_is_generated_from_canonical_instructions():
    sync_skills = _load_sync_module()
    template = ROOT / "templates" / "CLAUDE.scientific-writer.md"

    assert template.read_text(encoding="utf-8") == sync_skills.expected_instructions_template()


def test_instruction_surfaces_do_not_reference_removed_parallel_wrapper():
    paths = [
        ROOT / "CLAUDE.md",
        ROOT / ".claude" / "WRITER.md",
        ROOT / "scientific_writer" / ".claude" / "WRITER.md",
        ROOT / "templates" / "CLAUDE.scientific-writer.md",
    ]
    for path in paths:
        text = path.read_text(encoding="utf-8")
        assert "parallel_web.py" not in text
        assert "parallel-cli search" in text


def test_skills_document_has_one_section_per_locked_skill():
    text = (ROOT / "docs" / "SKILLS.md").read_text(encoding="utf-8")
    sections = re.findall(r"^### (\d+)\.", text, flags=re.MULTILINE)

    assert sections == [str(index) for index in range(1, 27)]


def test_first_party_markdown_file_links_resolve():
    documents = [
        ROOT / "README.md",
        ROOT / "CONTRIBUTING.md",
        ROOT / "scripts" / "README.md",
        *sorted((ROOT / "docs").glob("*.md")),
    ]
    missing = []
    for document in documents:
        text = document.read_text(encoding="utf-8")
        for target in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", text):
            target = target.strip().split(maxsplit=1)[0]
            if (
                not target
                or target.startswith(("#", "http://", "https://", "mailto:"))
            ):
                continue
            relative = unquote(target.split("#", 1)[0])
            resolved = (document.parent / relative).resolve()
            if not resolved.exists():
                missing.append(f"{document.relative_to(ROOT)} -> {target}")

    assert missing == []
