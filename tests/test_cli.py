"""Tests for scientific_writer.cli."""

import inspect
import sys
from pathlib import Path

from scientific_writer import cli


def test_help_mentions_current_research_backend(capsys):
    cli._print_help()
    out = capsys.readouterr().out
    assert "Perplexity" not in out
    assert "Parallel" in out


def test_cli_source_has_no_stale_backend_or_blocking_sleep():
    source = inspect.getsource(cli)
    assert "Perplexity" not in source, "CLI still references the removed Perplexity backend"
    assert "time.sleep(" not in source, "blocking sleep inside the async event loop"


class TestResolveModel:
    def test_default_effort_is_medium_opus(self):
        assert cli._resolve_model() == "claude-opus-4-8"

    def test_effort_levels_resolve_via_shared_map(self):
        from scientific_writer.core import EFFORT_LEVEL_MODELS

        for level, model in EFFORT_LEVEL_MODELS.items():
            assert cli._resolve_model(level) == model

    def test_unknown_effort_falls_back_to_medium(self):
        assert cli._resolve_model("turbo") == "claude-opus-4-8"


def test_cli_forwards_execution_and_input_controls(monkeypatch):
    captured = {}

    def fake_main(**kwargs):
        captured.update(kwargs)
        return object()

    monkeypatch.setattr(cli, "main", fake_main)
    monkeypatch.setattr(cli.asyncio, "run", lambda coroutine: None)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "scientific-writer",
            "--effort",
            "high",
            "--track-token-usage",
            "--permission-mode",
            "acceptEdits",
            "--max-turns",
            "12",
            "--max-budget-usd",
            "3.5",
            "--max-auto-continuations",
            "0",
            "--consume-inputs",
        ],
    )

    cli.cli_main()

    assert captured == {
        "track_token_usage": True,
        "effort_level": "high",
        "permission_mode": "acceptEdits",
        "max_turns": 12,
        "max_budget_usd": 3.5,
        "max_auto_continuations": 0,
        "consume_inputs": True,
    }


def test_processed_input_signatures_prevent_unchanged_reimports(tmp_path):
    source = tmp_path / "data.csv"
    source.write_text("value\n1\n")
    signatures: dict[Path, tuple[int, int]] = {}
    processed_info = {
        "all_files": [
            {
                "original": str(source),
                "destination": str(tmp_path / "project" / "data.csv"),
            }
        ]
    }

    cli._remember_processed_inputs(processed_info, signatures)

    assert signatures[source.resolve()] == cli._input_signature(source)
    source.write_text("value\n1\n2\n")
    assert signatures[source.resolve()] != cli._input_signature(source)
