#!/usr/bin/env python3
"""Validate source-fact traceability without interpreting source content."""

from __future__ import annotations

import argparse
import sys

from _common import (
    Issue,
    ValidationError,
    all_fact_references,
    error_report,
    load_package,
    print_report,
    report_payload,
    validate_package_structure,
)


def validate_traceability(documents: dict[str, dict]) -> dict:
    issues = validate_package_structure(documents)
    if issues:
        return report_payload(
            "source_fact_traceability",
            issues,
            counts={"structural_issues": len(issues)},
        )

    manifest = documents["source_fact_manifest"]
    facts = manifest["facts"]
    fact_index = {
        fact["fact_id"]: (index, fact) for index, fact in enumerate(facts)
    }
    references = all_fact_references(documents)
    referenced_ids: set[str] = set()

    for path, fact_id in references:
        record = fact_index.get(fact_id)
        if record is None:
            issues.append(Issue("UNKNOWN_SOURCE_FACT_REFERENCE", path))
            continue
        referenced_ids.add(fact_id)
        index, fact = record
        verification = fact["verification"]
        if verification["status"] != "verified":
            issues.append(
                Issue(
                    "REFERENCED_FACT_NOT_VERIFIED",
                    f"source_fact_manifest:$.facts[{index}].verification.status",
                )
            )

    official_types = {
        "current_fda_labeling",
        "current_rems_material",
        "current_official_guidance",
        "local_policy",
    }
    for index, fact in enumerate(facts):
        base = f"source_fact_manifest:$.facts[{index}]"
        verification = fact["verification"]
        if verification["status"] == "verified":
            if not verification["verified_by_role"]:
                issues.append(
                    Issue(
                        "VERIFIED_FACT_REVIEWER_ROLE_MISSING",
                        f"{base}.verification.verified_by_role",
                    )
                )
            if verification["verified_at"] is None:
                issues.append(
                    Issue(
                        "VERIFIED_FACT_TIME_MISSING",
                        f"{base}.verification.verified_at",
                    )
                )
        source_type = fact["source"]["source_type"]
        applicability = fact["applicability"]
        if (
            source_type in official_types
            and applicability["status"]
            != "confirmed_by_authorized_clinician"
        ):
            issues.append(
                Issue(
                    "SOURCE_APPLICABILITY_NOT_CONFIRMED",
                    f"{base}.applicability.status",
                )
            )
        if (
            applicability["status"]
            == "confirmed_by_authorized_clinician"
            and (
                not applicability["confirmed_by_role"]
                or applicability["confirmed_at"] is None
            )
        ):
            issues.append(
                Issue(
                    "SOURCE_APPLICABILITY_CONFIRMATION_INCOMPLETE",
                    f"{base}.applicability",
                )
            )
        if fact["fact_id"] not in referenced_ids:
            issues.append(Issue("ORPHAN_SOURCE_FACT", base, "warning"))

    issues.sort(key=lambda item: (item.path, item.code))
    return report_payload(
        "source_fact_traceability",
        issues,
        counts={
            "facts": len(facts),
            "fact_references": len(references),
            "referenced_facts": len(referenced_ids),
        },
        extra={
            "source_content_interpreted": False,
            "source_applicability_determined_by_script": False,
        },
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Check that every package fact reference exists and points to a "
            "human-verified source fact. Source content is not interpreted."
        )
    )
    parser.add_argument("package", help="Complete local package directory")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        documents, _ = load_package(args.package)
        report = validate_traceability(documents)
    except ValidationError as exc:
        report = error_report("source_fact_traceability", exc)
    print_report(report)
    return 1 if report["status"] == "fail" else 0


if __name__ == "__main__":
    sys.exit(main())
