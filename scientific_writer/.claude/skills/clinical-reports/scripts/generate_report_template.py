#!/usr/bin/env python3
"""Copy a fail-closed structured clinical-report template to a local path."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.dont_write_bytecode = True

from _common import (  # noqa: E402
    ValidationError,
    load_json_object,
    local_input_path,
    local_output_path,
)

TOOL = "generate_report_template"
TEMPLATES = {
    "case-report": "case_report_template.json",
    "radiology-scaffold": "radiology_report_template.json",
    "pathology-scaffold": "pathology_report_template.json",
    "lab-scaffold": "lab_report_template.json",
    "csr": "clinical_trial_csr_template.json",
    "trial-results": "clinical_trial_results_template.json",
    "trial-protocol-checklist": "trial_protocol_reporting_checklist.json",
    "safety-aggregate": "clinical_trial_safety_aggregate_template.json",
    "adverse-event-csv": "adverse_event_aggregate_input_template.csv",
    "research-summary": "research_summary_template.json",
    "deidentification-checklist": "deidentification_process_checklist.json",
    "quality-review": "quality_review_checklist.json",
    "provenance": "provenance_manifest_template.json",
    "terminology": "terminology_manifest_template.json",
    "consistency": "consistency_manifest_template.json",
}


def template_directory() -> Path:
    """Return the fixed bundled asset directory."""
    return Path(__file__).resolve().parent.parent / "assets"


def list_templates() -> str:
    """Return a stable machine-readable-friendly list."""
    lines = ["Available fail-closed templates:"]
    lines.extend(f"- {name}: {TEMPLATES[name]}" for name in sorted(TEMPLATES))
    return "\n".join(lines) + "\n"


def generate_template(
    template_type: str,
    raw_output: str,
    *,
    overwrite: bool = False,
) -> Path:
    """Copy one fixed asset without interpolation or clinical content."""
    if template_type not in TEMPLATES:
        raise ValidationError(f"unknown template type: {template_type}")
    source = template_directory() / TEMPLATES[template_type]
    suffix = source.suffix.lower()
    validated_source = local_input_path(
        str(source),
        suffixes={suffix},
        max_bytes=1_000_000,
    )
    if suffix == ".json":
        load_json_object(str(validated_source))
    output = local_output_path(
        raw_output,
        suffixes={suffix},
        overwrite=overwrite,
    )
    output.write_bytes(validated_source.read_bytes())
    return output


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Copy a bundled fail-closed JSON/CSV template. No interpolation, "
            "network access, clinical inference, signing, filing, or submission."
        )
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--list", action="store_true", help="List template types")
    mode.add_argument("--type", choices=sorted(TEMPLATES), help="Template type")
    parser.add_argument("-o", "--output", help="Required local output when --type is used")
    parser.add_argument("--overwrite", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.list:
        if args.output:
            print("--output is not used with --list", file=sys.stderr)
            return 2
        print(list_templates(), end="")
        return 0
    if not args.output:
        print("--output is required with --type", file=sys.stderr)
        return 2
    try:
        output = generate_template(args.type, args.output, overwrite=args.overwrite)
        print(f"Created blocked draft template: {output}")
        print("Qualified review is required; this output is not for clinical use or submission.")
        return 0
    except (OSError, ValidationError) as exc:
        print(f"{TOOL}: BLOCKED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
