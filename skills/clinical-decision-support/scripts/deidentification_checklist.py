#!/usr/bin/env python3
"""Check documentation of a de-identification process without reading health data."""

from __future__ import annotations

import argparse
import sys
from typing import Any

from _common import (
    InputError,
    IssueLog,
    load_json_object,
    print_report,
    require_list,
    require_nonempty_text,
    source_ids,
    validate_references,
    write_json,
)

SAFE_HARBOR_IDS = {
    "names",
    "geography",
    "dates_and_ages",
    "telephone_numbers",
    "fax_numbers",
    "email_addresses",
    "social_security_numbers",
    "medical_record_numbers",
    "health_plan_numbers",
    "account_numbers",
    "certificate_license_numbers",
    "vehicle_identifiers",
    "device_identifiers",
    "web_urls",
    "ip_addresses",
    "biometric_identifiers",
    "full_face_images",
    "other_unique_identifiers",
}
ALLOWED_STATUS = {
    "not_present",
    "removed",
    "generalized",
    "expert_reviewed",
    "unresolved",
}
PLACEHOLDER_MARKERS = ("REPLACE_", "REQUIRES_", "YYYY-MM-DD")


def _find_placeholders(value: Any, location: str = "$") -> list[str]:
    findings: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            findings.extend(_find_placeholders(nested, f"{location}.{key}"))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            findings.extend(_find_placeholders(nested, f"{location}[{index}]"))
    elif isinstance(value, str) and any(marker in value for marker in PLACEHOLDER_MARKERS):
        findings.append(location)
    return findings


def check_documentation(document: dict[str, Any]) -> tuple[IssueLog, dict[str, Any]]:
    log = IssueLog()
    summary: dict[str, Any] = {
        "method": None,
        "documentation_complete": False,
        "deidentification_determined": False,
        "hipaa_compliance_determined": False,
        "unresolved_categories": [],
    }
    try:
        require_nonempty_text(document.get("schema_version"), "schema_version")
        require_nonempty_text(document.get("checklist_id"), "checklist_id")
        require_nonempty_text(document.get("title"), "title")
        known_sources = source_ids(document)
        validate_references(document.get("source_ids"), known_sources, "source_ids")

        method = require_nonempty_text(document.get("method"), "method")
        summary["method"] = method
        if method not in {"safe_harbor", "expert_determination", "undecided"}:
            log.errors.append("method is unsupported")
        if method == "undecided":
            log.errors.append("A qualified human must select and document a method")

        boundary = document.get("data_boundary")
        if not isinstance(boundary, dict):
            raise InputError("data_boundary must be an object")
        if boundary.get("raw_data_supplied") is not False:
            log.errors.append("data_boundary.raw_data_supplied must be false")
        if boundary.get("metadata_only") is not True:
            log.errors.append("data_boundary.metadata_only must be true")
        for field in ("data_context", "recipient_context", "release_context"):
            require_nonempty_text(boundary.get(field), f"data_boundary.{field}")

        entries = require_list(
            document.get("identifier_categories"),
            "identifier_categories",
            maximum=18,
        )
        observed_ids: set[str] = set()
        for index, entry in enumerate(entries):
            field = f"identifier_categories[{index}]"
            if not isinstance(entry, dict):
                raise InputError(f"{field} must be an object")
            identifier = require_nonempty_text(entry.get("id"), f"{field}.id")
            if identifier not in SAFE_HARBOR_IDS:
                log.errors.append(f"{field}.id is not a Safe Harbor category")
            if identifier in observed_ids:
                log.errors.append(f"Duplicate identifier category: {identifier}")
            observed_ids.add(identifier)
            status = require_nonempty_text(entry.get("status"), f"{field}.status")
            if status not in ALLOWED_STATUS:
                log.errors.append(f"{field}.status is unsupported")
            evidence = require_nonempty_text(entry.get("evidence"), f"{field}.evidence")
            if status == "unresolved":
                summary["unresolved_categories"].append(identifier)
            if evidence.lower().startswith(("example:", "value:")):
                log.errors.append(
                    f"{field}.evidence must not contain an example identifier or value"
                )
        missing_ids = sorted(SAFE_HARBOR_IDS - observed_ids)
        extra_ids = sorted(observed_ids - SAFE_HARBOR_IDS)
        if missing_ids:
            log.errors.append("Missing Safe Harbor categories: " + ", ".join(missing_ids))
        if extra_ids:
            log.errors.append("Unexpected categories: " + ", ".join(extra_ids))

        safe_harbor = document.get("safe_harbor_review")
        if not isinstance(safe_harbor, dict):
            raise InputError("safe_harbor_review must be an object")
        for field in (
            "actual_knowledge",
            "free_text",
            "derived_fields",
            "date_age_zip_rules",
        ):
            require_nonempty_text(safe_harbor.get(field), f"safe_harbor_review.{field}")
        if method == "safe_harbor":
            if summary["unresolved_categories"]:
                log.errors.append("Safe Harbor review has unresolved identifier categories")
            if safe_harbor.get("completed") is not True:
                log.errors.append("safe_harbor_review.completed must be true")
            require_nonempty_text(
                safe_harbor.get("reviewer_role"), "safe_harbor_review.reviewer_role"
            )
            require_nonempty_text(
                safe_harbor.get("review_date"), "safe_harbor_review.review_date"
            )

        expert = document.get("expert_determination_review")
        if not isinstance(expert, dict):
            raise InputError("expert_determination_review must be an object")
        if method == "expert_determination":
            for field in (
                "expert_qualification_reference",
                "method_document_reference",
                "risk_threshold_rationale",
                "residual_risk",
                "validity_period",
                "change_triggers",
                "review_date",
            ):
                require_nonempty_text(
                    expert.get(field), f"expert_determination_review.{field}"
                )
            if expert.get("completed") is not True:
                log.errors.append(
                    "expert_determination_review.completed must be true"
                )

        residual = document.get("residual_risk_review")
        if not isinstance(residual, dict):
            raise InputError("residual_risk_review must be an object")
        for field in (
            "linkage",
            "differencing",
            "rare_combinations",
            "longitudinal_patterns",
            "geography",
            "genomics",
            "prior_releases",
        ):
            require_nonempty_text(residual.get(field), f"residual_risk_review.{field}")
        if residual.get("completed") is not True:
            log.errors.append("residual_risk_review.completed must be true")

        review = document.get("human_review")
        if not isinstance(review, dict):
            raise InputError("human_review must be an object")
        if review.get("required") is not True:
            log.errors.append("human_review.required must be true")
        require_nonempty_text(review.get("role"), "human_review.role")
        require_nonempty_text(
            review.get("approval_boundary"), "human_review.approval_boundary"
        )
        if review.get("completed") is not True:
            log.errors.append("human_review.completed must be true")

        governance = document.get("governance")
        if not isinstance(governance, dict):
            raise InputError("governance must be an object")
        for field in (
            "version",
            "owner",
            "change_summary",
            "auditability",
            "monitoring",
        ):
            require_nonempty_text(governance.get(field), f"governance.{field}")

        if document.get("compliance_claims") is not False:
            log.errors.append("compliance_claims must be false")
        if review.get("completed") is True:
            placeholders = _find_placeholders(document)
            if placeholders:
                log.errors.append(
                    "Unresolved template placeholders remain: "
                    + ", ".join(placeholders[:10])
                )
    except InputError as exc:
        log.errors.append(str(exc))

    summary["documentation_complete"] = log.ok
    if log.ok:
        log.info.append(
            "Process documentation is complete; no de-identification or compliance determination was made"
        )
    return log, summary


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Check metadata documenting Safe Harbor or Expert Determination work. "
            "The script never reads a dataset and never determines compliance."
        )
    )
    parser.add_argument("input", help="Local checklist JSON")
    parser.add_argument("-o", "--output", help="Optional local JSON report")
    args = parser.parse_args()

    try:
        document = load_json_object(args.input)
        log, summary = check_documentation(document)
        report = log.as_dict()
        report["deidentification_review"] = summary
        if args.output:
            write_json(args.output, report)
        print_report(report)
    except InputError as exc:
        print_report(IssueLog(errors=[str(exc)]).as_dict())
        return 2
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
