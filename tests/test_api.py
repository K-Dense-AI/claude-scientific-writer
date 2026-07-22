"""Tests for scientific_writer.api runtime contracts and result building."""

import asyncio
from datetime import datetime, timezone
import os
from pathlib import Path
from types import SimpleNamespace

from scientific_writer import api
from scientific_writer.utils import scan_paper_directory


def _collect(agen):
    async def collect():
        return [event async for event in agen]

    return asyncio.run(collect())


class TestEffortLevelModels:
    def test_three_effort_levels_exist(self):
        assert set(api.EFFORT_LEVEL_MODELS) == {"low", "medium", "high"}

    def test_effort_level_model_assignments(self):
        assert api.EFFORT_LEVEL_MODELS["low"] == "claude-haiku-4-5"
        assert api.EFFORT_LEVEL_MODELS["medium"] == "claude-opus-4-8"
        assert api.EFFORT_LEVEL_MODELS["high"] == "claude-opus-4-8"

    def test_no_effort_level_uses_fable(self):
        for model in api.EFFORT_LEVEL_MODELS.values():
            assert "fable" not in model.lower()

    def test_map_is_shared_with_core(self):
        from scientific_writer.core import EFFORT_LEVEL_MODELS

        assert api.EFFORT_LEVEL_MODELS is EFFORT_LEVEL_MODELS


def test_build_paper_result_uses_explicit_utc_creation_time(tmp_path):
    paper_dir = tmp_path / "20250101_120000_demo_topic"
    (paper_dir / "final").mkdir(parents=True)
    (paper_dir / "final" / "report.md").write_text("complete")
    file_info = scan_paper_directory(paper_dir)
    created_at = datetime(2026, 7, 22, 20, 0, tzinfo=timezone.utc)

    result = api._build_paper_result(paper_dir, file_info, created_at=created_at)

    assert datetime.fromisoformat(result.metadata.created_at) == created_at
    assert result.status == "success"


def test_build_paper_result_accepts_image_only_output_and_sources(tmp_path):
    paper_dir = tmp_path / "20250101_120000_infographic"
    (paper_dir / "final").mkdir(parents=True)
    (paper_dir / "sources").mkdir()
    image = paper_dir / "final" / "infographic.png"
    source = paper_dir / "sources" / "search.json"
    image.write_bytes(b"png")
    source.write_text("{}")

    result = api._build_paper_result(paper_dir, scan_paper_directory(paper_dir))

    assert result.status == "success"
    assert result.compilation_success is False
    assert result.files.final_artifacts == [str(image)]
    assert result.files.sources == [str(source)]
    assert str(image) in result.files.artifacts


def test_find_most_recent_output_does_not_return_stale_directory(tmp_path):
    stale = tmp_path / "20200101_000000_stale"
    stale.mkdir()
    os.utime(stale, (1, 1))

    assert api._find_most_recent_output(tmp_path, start_time=100) is None


def test_generate_paper_honors_inputs_key_output_and_usage(tmp_path, monkeypatch):
    work_dir = tmp_path / "work"
    work_dir.mkdir()
    (work_dir / ".claude").mkdir()
    (work_dir / ".claude" / "WRITER.md").write_text("Use staged inputs.")
    data_file = work_dir / "results.csv"
    data_file.write_text("x,y\n1,2\n")
    captured = {}

    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setattr(api, "setup_claude_skills", lambda package_dir, work_dir: None)

    async def fake_query(prompt, options):
        captured["prompt"] = prompt
        captured["options"] = options
        project = next((work_dir / "custom").iterdir())
        staged = project / "data" / "results.csv"
        assert staged.read_text() == data_file.read_text()
        (project / "final" / "report.md").write_text("# Complete")
        yield SimpleNamespace(
            usage={
                "input_tokens": 11,
                "output_tokens": 7,
                "cache_creation_input_tokens": 3,
                "cache_read_input_tokens": 5,
            },
            content=[SimpleNamespace(text="done")],
        )

    monkeypatch.setattr(api, "claude_query", fake_query)

    events = _collect(
        api.generate_paper(
            "Analyze results.csv",
            cwd=str(work_dir),
            output_dir="custom",
            api_key="test-key",
            effort_level="high",
            data_files=["results.csv"],
            track_token_usage=True,
            auto_continue=False,
        )
    )

    result = next(event for event in events if event["type"] == "result")
    options = captured["options"]
    assert Path(result["paper_directory"]).parent == work_dir / "custom"
    assert result["status"] == "success"
    assert result["token_usage"]["total_tokens"] == 18
    assert result["token_usage"]["cache_read_input_tokens"] == 5
    assert options.env["ANTHROPIC_API_KEY"] == "test-key"
    assert options.skills == "all"
    assert options.effort == "high"
    assert "results.csv" in captured["prompt"]
    assert any(event["type"] == "text" and event["content"] == "done" for event in events)
    assert "ANTHROPIC_API_KEY" not in os.environ


def test_generate_paper_reports_missing_input_without_calling_sdk(tmp_path, monkeypatch):
    work_dir = tmp_path / "work"
    work_dir.mkdir()
    (work_dir / ".claude").mkdir()
    (work_dir / ".claude" / "WRITER.md").write_text("Instructions")
    called = False

    monkeypatch.setattr(api, "setup_claude_skills", lambda package_dir, work_dir: None)

    async def fake_query(prompt, options):
        nonlocal called
        called = True
        yield SimpleNamespace()

    monkeypatch.setattr(api, "claude_query", fake_query)
    events = _collect(
        api.generate_paper(
            "Analyze missing data",
            cwd=str(work_dir),
            api_key="test-key",
            data_files=["missing.csv"],
        )
    )

    result = events[-1]
    assert result["type"] == "result"
    assert result["status"] == "failed"
    assert "Input file not found" in result["errors"][0]
    assert called is False
