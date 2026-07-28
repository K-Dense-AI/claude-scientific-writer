#!/usr/bin/env python3
"""Check documented privacy process without determining compliance."""

from __future__ import annotations

import argparse
import sys

from _common import (
    Issue,
    ValidationError,
    direct_identifier_key_paths,
    error_report,
    load_package,
    print_report,
    report_payload,
    validate_package_structure,
)


def check_privacy_process(documents: dict[str, dict]) -> dict:
    issues = validate_package_structure(documents)
    if issues:
        return report_payload(
            "privacy_process",
            issues,
            counts={"structural_issues": len(issues)},
        )

    handoff = documents["intended_use_handoff_record"]
    classification = handoff["data_classification"]
    privacy = handoff["privacy_process"]

    for document_type, document in documents.items():
        if document["data_classification"] != classification:
            issues.append(
                Issue(
                    "DATA_CLASSIFICATION_MISMATCH",
                    f"{document_type}:$.data_classification",
                )
            )
        if document["subject_ref"] != handoff["subject_ref"]:
            issues.append(
                Issue(
                    "SUBJECT_REFERENCE_MISMATCH",
                    f"{document_type}:$.subject_ref",
                )
            )
        for path in direct_identifier_key_paths(document):
            issues.append(
                Issue(
                    "DIRECT_IDENTIFIER_FIELD_NAME_PROHIBITED",
                    f"{document_type}:{path}",
                )
            )

    if privacy["data_classification"] != classification:
        issues.append(
            Issue(
                "PRIVACY_CLASSIFICATION_MISMATCH",
                (
                    "intended_use_handoff_record:"
                    "$.privacy_process.data_classification"
                ),
            )
        )

    required_true = (
        "local_authorization_confirmed",
        "minimum_necessary_confirmed",
        "no_external_tools_confirmed",
        "no_prompt_log_example_copy_confirmed",
    )
    for field in required_true:
        if privacy[field] is not True:
            issues.append(
                Issue(
                    "PRIVACY_ATTESTATION_REQUIRED",
                    f"intended_use_handoff_record:$.privacy_process.{field}",
                )
            )

    for field in (
        "authorized_environment_reference",
        "retention_policy_reference",
    ):
        if not privacy[field].strip():
            issues.append(
                Issue(
                    "PRIVACY_REFERENCE_REQUIRED",
                    f"intended_use_handoff_record:$.privacy_process.{field}",
                )
            )

    if privacy["data_disposition_status"] == "pending":
        issues.append(
            Issue(
                "DATA_DISPOSITION_NOT_DOCUMENTED",
                (
                    "intended_use_handoff_record:"
                    "$.privacy_process.data_disposition_status"
                ),
            )
        )

    if classification == "synthetic":
        if not handoff["subject_ref"].startswith("SYNTHETIC-"):
            issues.append(
                Issue(
                    "SYNTHETIC_REFERENCE_NOT_MARKED",
                    "intended_use_handoff_record:$.subject_ref",
                )
            )
        if privacy["privacy_review_status"] not in {
            "not_applicable_synthetic",
            "completed_by_qualified_reviewer",
        }:
            issues.append(
                Issue(
                    "SYNTHETIC_PRIVACY_STATUS_PENDING",
                    (
                        "intended_use_handoff_record:"
                        "$.privacy_process.privacy_review_status"
                    ),
                )
            )
    else:
        if (
            privacy["privacy_review_status"]
            != "completed_by_qualified_reviewer"
        ):
            issues.append(
                Issue(
                    "QUALIFIED_PRIVACY_REVIEW_REQUIRED",
                    (
                        "intended_use_handoff_record:"
                        "$.privacy_process.privacy_review_status"
                    ),
                )
            )
        if not privacy["privacy_reviewer_role"].strip():
            issues.append(
                Issue(
                    "PRIVACY_REVIEWER_ROLE_REQUIRED",
                    (
                        "intended_use_handoff_record:"
                        "$.privacy_process.privacy_reviewer_role"
                    ),
                )
            )
        if privacy["reviewed_at"] is None:
            issues.append(
                Issue(
                    "PRIVACY_REVIEW_TIME_REQUIRED",
                    (
                        "intended_use_handoff_record:"
                        "$.privacy_process.reviewed_at"
                    ),
                )
            )
        issues.append(
            Issue(
                "PATIENT_DERIVED_FREE_TEXT_REQUIRES_LOCAL_REVIEW",
                "$",
                "warning",
            )
        )

    issues.sort(key=lambda item: (item.path, item.code))
    return report_payload(
        "privacy_process",
        issues,
        counts={
            "documents_checked": len(documents),
            "direct_identifier_field_paths": sum(
                len(direct_identifier_key_paths(document))
                for document in documents.values()
            ),
        },
        extra={
            "deidentification_determined": False,
            "hipaa_compliance_determined": False,
            "external_processing_authorized": False,
            "values_scanned_or_echoed": False,
        },
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Check local authorization, minimization, no-external-tool, "
            "qualified-review, retention, and direct-field declarations. "
            "This is not a de-identification or compliance determination."
        )
    )
    parser.add_argument("package", help="Complete local package directory")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        documents, _ = load_package(args.package)
        report = check_privacy_process(documents)
    except ValidationError as exc:
        report = error_report("privacy_process", exc)
    print_report(report)
    return 1 if report["status"] == "fail" else 0


if __name__ == "__main__":
    sys.exit(main())
