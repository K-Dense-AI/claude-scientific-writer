"""Generate a local, explicitly incomplete manuscript workspace."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from _common import (
    InputError,
    emit_report,
    read_json,
    read_text,
    require_object,
    run,
    write_new_text,
)

TOOL = "scaffold_manuscript"
ASSET_DIR = Path(__file__).resolve().parents[1] / "assets"
DOCUMENT_ID_RE = re.compile(r"^[A-Za-z][A-Za-z0-9._-]{1,63}$")
GUIDELINE_ID_RE = re.compile(r"^[a-z][a-z0-9.-]{1,63}$")
TEMPLATE_FILES = {
    "manuscript.md": "manuscript_scaffold.md",
    "claims.csv": "claim_evidence_template.csv",
    "source_manifest.json": "source_manifest_template.json",
    "consistency_manifest.json": "consistency_manifest_template.json",
    "authorship.json": "authorship_template.json",
}


def _json_text(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def _prepare_manifest(
    *,
    document_id: str,
    study_design: str,
    guidelines: list[str],
) -> str:
    data = require_object(
        read_json(ASSET_DIR / "manuscript_manifest_template.json"),
        "manuscript_manifest_template",
    )
    data["document_id"] = document_id
    data["study_design"] = study_design
    data["reporting_guidelines"] = guidelines
    return _json_text(data)


def _prepare_coverage(guidelines: list[str]) -> str:
    data = require_object(
        read_json(ASSET_DIR / "reporting_coverage_template.json"),
        "reporting_coverage_template",
    )
    data["guideline_id"] = guidelines[0] if guidelines else "[[TODO:guideline-id]]"
    return _json_text(data)


def generate(
    output_dir: Path,
    *,
    document_id: str,
    study_design: str,
    guidelines: list[str],
) -> list[str]:
    if output_dir.exists() or output_dir.is_symlink():
        raise InputError("output directory already exists; refusing to overwrite")
    parent = output_dir.parent
    if not parent.is_dir() or parent.is_symlink():
        raise InputError("output parent must be an existing regular directory")

    prepared: dict[str, str] = {
        destination: read_text(ASSET_DIR / source, {Path(source).suffix})
        for destination, source in TEMPLATE_FILES.items()
    }
    prepared["manuscript_manifest.json"] = _prepare_manifest(
        document_id=document_id,
        study_design=study_design,
        guidelines=guidelines,
    )
    prepared["reporting_coverage.json"] = _prepare_coverage(guidelines)

    output_dir.mkdir(mode=0o700)
    for filename in sorted(prepared):
        write_new_text(
            output_dir / filename,
            prepared[filename],
            {Path(filename).suffix},
        )
    return sorted(prepared)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Create a deterministic local manuscript workspace. Generated files "
            "are marked incomplete and must pass all validators before submission."
        )
    )
    parser.add_argument("--output-dir", required=True, help="new directory to create")
    parser.add_argument("--document-id", required=True)
    parser.add_argument("--study-design", required=True)
    parser.add_argument(
        "--guideline",
        action="append",
        default=[],
        help="candidate reporting-guideline ID; repeat as needed",
    )
    return parser


def cli() -> int:
    args = build_parser().parse_args()
    if not DOCUMENT_ID_RE.fullmatch(args.document_id):
        raise InputError("document-id must be 2-64 safe identifier characters")
    if not DOCUMENT_ID_RE.fullmatch(args.study_design):
        raise InputError("study-design must be a safe identifier")
    guidelines = sorted(set(args.guideline))
    if any(not GUIDELINE_ID_RE.fullmatch(value) for value in guidelines):
        raise InputError("guideline IDs must be safe lowercase identifiers")
    files = generate(
        Path(args.output_dir),
        document_id=args.document_id,
        study_design=args.study_design,
        guidelines=guidelines,
    )
    return emit_report(
        TOOL,
        [],
        summary={
            "files_created": files,
            "submission_ready": False,
            "overwrites": False,
        },
    )


if __name__ == "__main__":
    run(TOOL, cli)
