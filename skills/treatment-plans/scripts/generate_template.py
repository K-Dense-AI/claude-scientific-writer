#!/usr/bin/env python3
"""Generate a fail-closed local JSON documentation package."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from _common import (
    IDENTIFIER_RE,
    TEMPLATE_FILES,
    ValidationError,
    atomic_write_json,
    copy_template_document,
    error_report,
    print_report,
    report_payload,
    safe_new_directory,
)


def generate_package(
    output_directory: str,
    *,
    subject_ref: str,
    classification: str,
    acknowledge_real_patient_local_processing: bool = False,
) -> dict:
    """Copy all templates without generating any clinical content."""

    if not IDENTIFIER_RE.fullmatch(subject_ref):
        raise ValidationError("SUBJECT_REFERENCE_FORMAT")
    allowed = {
        "synthetic",
        "deidentified_qualified_review",
        "real_patient_minimum_necessary",
    }
    if classification not in allowed:
        raise ValidationError("DATA_CLASSIFICATION_INVALID")
    if (
        classification == "real_patient_minimum_necessary"
        and not acknowledge_real_patient_local_processing
    ):
        raise ValidationError("REAL_PATIENT_LOCAL_ACK_REQUIRED")

    assets = Path(__file__).resolve().parents[1] / "assets"
    prepared: list[tuple[str, dict]] = []
    for _, (template_name, output_name) in TEMPLATE_FILES.items():
        document = copy_template_document(
            assets / template_name,
            subject_ref=subject_ref,
            classification=classification,
        )
        prepared.append((output_name, document))

    destination = safe_new_directory(output_directory)
    for output_name, document in prepared:
        atomic_write_json(destination / output_name, document)

    return report_payload(
        "generate_template",
        [],
        counts={"documents_generated": len(prepared)},
        extra={
            "generated_filenames": sorted(name for name, _ in prepared),
            "release_status": "blocked",
            "clinical_content_generated": False,
            "external_processing_authorized": False,
        },
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Create six local, generic JSON treatment-plan documentation "
            "templates. No clinical content is generated."
        )
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        help="New local directory; existing paths are rejected",
    )
    parser.add_argument(
        "--subject-ref",
        default="SYNTHETIC-CASE-001",
        help=(
            "Local pseudonymous identifier; never use a name, MRN, or other "
            "direct identifier"
        ),
    )
    parser.add_argument(
        "--classification",
        choices=[
            "synthetic",
            "deidentified_qualified_review",
            "real_patient_minimum_necessary",
        ],
        default="synthetic",
    )
    parser.add_argument(
        "--acknowledge-real-patient-local-processing",
        action="store_true",
        help=(
            "Required only for real_patient_minimum_necessary; confirms that "
            "the user will apply the documented local-only data gate"
        ),
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        report = generate_package(
            args.output_dir,
            subject_ref=args.subject_ref,
            classification=args.classification,
            acknowledge_real_patient_local_processing=(
                args.acknowledge_real_patient_local_processing
            ),
        )
    except ValidationError as exc:
        print_report(error_report("generate_template", exc))
        return 1
    print_report(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
