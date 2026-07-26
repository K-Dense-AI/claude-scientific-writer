"""Tests for scientific_writer.models timestamp behavior."""

from datetime import datetime, timezone

from scientific_writer.models import (
    DocumentFiles,
    DocumentMetadata,
    DocumentResult,
    PaperFiles,
    PaperMetadata,
    PaperResult,
    ProgressUpdate,
    TokenUsage,
)


def test_progress_update_timestamp_is_timezone_aware_utc():
    timestamp = ProgressUpdate().timestamp
    parsed = datetime.fromisoformat(timestamp)
    assert parsed.tzinfo is not None
    assert parsed.utcoffset().total_seconds() == 0
    # New contract: explicit offset form, not the legacy naive-utcnow + "Z" suffix
    assert timestamp.endswith("+00:00")
    assert abs((datetime.now(timezone.utc) - parsed).total_seconds()) < 60


def test_paper_metadata_created_at_is_timezone_aware_utc():
    created_at = PaperMetadata().created_at
    parsed = datetime.fromisoformat(created_at)
    assert parsed.tzinfo is not None
    assert parsed.utcoffset().total_seconds() == 0
    assert created_at.endswith("+00:00")


def test_token_usage_accumulates_sdk_mappings():
    usage = TokenUsage()
    usage.add_usage(
        {
            "input_tokens": 10,
            "output_tokens": 4,
            "cache_creation_input_tokens": 2,
            "cache_read_input_tokens": 8,
        }
    )

    assert usage.to_dict() == {
        "input_tokens": 10,
        "output_tokens": 4,
        "cache_creation_input_tokens": 2,
        "cache_read_input_tokens": 8,
        "total_tokens": 14,
    }


def test_document_aliases_preserve_backwards_compatibility():
    assert DocumentMetadata is PaperMetadata
    assert DocumentFiles is PaperFiles
    assert DocumentResult is PaperResult


def test_paper_files_serializes_generic_artifacts():
    files = PaperFiles(
        sources=["source.json"],
        final_artifacts=["report.docx"],
        draft_artifacts=["draft.md"],
        artifacts=["source.json", "draft.md", "report.docx"],
    )

    assert files.to_dict()["final_artifacts"] == ["report.docx"]
