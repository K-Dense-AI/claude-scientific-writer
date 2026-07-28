#!/usr/bin/env python3
"""Check cross-record consistency without clinical interpretation."""

from __future__ import annotations

import argparse
import sys
from datetime import date
from typing import Any

from _common import (
    Issue,
    ValidationError,
    load_package,
    parse_iso_datetime,
    print_report,
    record_ids,
    report_payload,
    validate_package_structure,
    error_report,
)


def _collect_ids(documents: dict[str, dict]) -> list[tuple[str, str]]:
    values: list[tuple[str, str]] = []

    def collect(records: list, field: str, path: str) -> None:
        for index, record in enumerate(records):
            if isinstance(record, dict) and isinstance(record.get(field), str):
                values.append((f"{path}[{index}].{field}", record[field]))

    facts = documents["source_fact_manifest"]["facts"]
    collect(facts, "fact_id", "source_fact_manifest:$.facts")

    interventions = documents[
        "clinician_authored_intervention_record"
    ]["interventions"]
    collect(
        interventions,
        "intervention_id",
        "clinician_authored_intervention_record:$.interventions",
    )
    for index, record in enumerate(interventions):
        collect(
            record["parameters_as_supplied"],
            "parameter_id",
            (
                "clinician_authored_intervention_record:"
                f"$.interventions[{index}].parameters_as_supplied"
            ),
        )

    planning = documents["goals_monitoring_checkpoint_record"]
    collect(
        planning["goals"],
        "goal_id",
        "goals_monitoring_checkpoint_record:$.goals",
    )
    collect(
        planning["monitoring_items"],
        "monitoring_id",
        "goals_monitoring_checkpoint_record:$.monitoring_items",
    )
    collect(
        planning["checkpoints"],
        "checkpoint_id",
        "goals_monitoring_checkpoint_record:$.checkpoints",
    )

    entries = documents[
        "informed_preference_shared_decision_record"
    ]["entries"]
    collect(
        entries,
        "decision_id",
        "informed_preference_shared_decision_record:$.entries",
    )
    for index, record in enumerate(entries):
        collect(
            record["options_as_documented"],
            "option_id",
            (
                "informed_preference_shared_decision_record:"
                f"$.entries[{index}].options_as_documented"
            ),
        )

    transition = documents["transition_reconciliation_record"]
    collect(
        transition["handoff_items"],
        "item_id",
        "transition_reconciliation_record:$.handoff_items",
    )
    collect(
        transition["unresolved_items"],
        "item_id",
        "transition_reconciliation_record:$.unresolved_items",
    )
    return values


def _duplicate_reference_issues(
    value: Any, path: str = "$"
) -> list[Issue]:
    issues: list[Issue] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            nested_path = f"{path}.{key}"
            if key.endswith("_ids") and isinstance(nested, list):
                if len(nested) != len(set(nested)):
                    issues.append(
                        Issue("DUPLICATE_REFERENCE_IN_LIST", nested_path)
                    )
            issues.extend(_duplicate_reference_issues(nested, nested_path))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            issues.extend(
                _duplicate_reference_issues(nested, f"{path}[{index}]")
            )
    return issues


def check_consistency(documents: dict[str, dict]) -> dict:
    issues = validate_package_structure(documents)
    if issues:
        return report_payload(
            "cross_record_consistency",
            issues,
            counts={"structural_issues": len(issues)},
        )

    handoff_document = documents["intended_use_handoff_record"]
    subject_ref = handoff_document["subject_ref"]
    classification = handoff_document["data_classification"]
    for document_type, document in documents.items():
        if document["subject_ref"] != subject_ref:
            issues.append(
                Issue(
                    "SUBJECT_REFERENCE_MISMATCH",
                    f"{document_type}:$.subject_ref",
                )
            )
        if document["data_classification"] != classification:
            issues.append(
                Issue(
                    "DATA_CLASSIFICATION_MISMATCH",
                    f"{document_type}:$.data_classification",
                )
            )
        issues.extend(
            Issue(issue.code, f"{document_type}:{issue.path}", issue.level)
            for issue in _duplicate_reference_issues(document)
        )

    seen: set[str] = set()
    for path, identifier in _collect_ids(documents):
        if identifier in seen:
            issues.append(Issue("GLOBAL_RECORD_ID_COLLISION", path))
        seen.add(identifier)

    interventions = documents[
        "clinician_authored_intervention_record"
    ]["interventions"]
    for index, record in enumerate(interventions):
        start = record["start_date"]
        end = record["end_date"]
        if start is not None and end is not None:
            if date.fromisoformat(start) > date.fromisoformat(end):
                issues.append(
                    Issue(
                        "INTERVENTION_DATE_ORDER_INVALID",
                        (
                            "clinician_authored_intervention_record:"
                            f"$.interventions[{index}]"
                        ),
                    )
                )

    planning = documents["goals_monitoring_checkpoint_record"]
    goal_ids = record_ids(planning, "goals", "goal_id")
    intervention_ids = record_ids(
        documents["clinician_authored_intervention_record"],
        "interventions",
        "intervention_id",
    )
    for index, checkpoint in enumerate(planning["checkpoints"]):
        base = (
            "goals_monitoring_checkpoint_record:"
            f"$.checkpoints[{index}]"
        )
        for reference_index, goal_id in enumerate(
            checkpoint["linked_goal_ids"]
        ):
            if goal_id not in goal_ids:
                issues.append(
                    Issue(
                        "CHECKPOINT_UNKNOWN_GOAL",
                        f"{base}.linked_goal_ids[{reference_index}]",
                    )
                )
        for reference_index, intervention_id in enumerate(
            checkpoint["linked_intervention_ids"]
        ):
            if intervention_id not in intervention_ids:
                issues.append(
                    Issue(
                        "CHECKPOINT_UNKNOWN_INTERVENTION",
                        (
                            f"{base}.linked_intervention_ids"
                            f"[{reference_index}]"
                        ),
                    )
                )

    transition = documents["transition_reconciliation_record"]
    reconciliation = transition["medication_reconciliation"]
    if reconciliation["status"] == "pending_authorized_review":
        if reconciliation["completed_by_role"] or reconciliation[
            "completed_at"
        ] is not None:
            issues.append(
                Issue(
                    "PENDING_RECONCILIATION_HAS_COMPLETION_DATA",
                    (
                        "transition_reconciliation_record:"
                        "$.medication_reconciliation"
                    ),
                )
            )
    elif reconciliation["status"] == "not_applicable_by_authorized_clinician":
        if (
            reconciliation["source_list_fact_ids"]
            or reconciliation["destination_list_fact_ids"]
        ):
            issues.append(
                Issue(
                    "NOT_APPLICABLE_RECONCILIATION_HAS_LIST_REFERENCES",
                    (
                        "transition_reconciliation_record:"
                        "$.medication_reconciliation"
                    ),
                )
            )
    elif reconciliation["status"] == "completed_by_authorized_clinician":
        if (
            not reconciliation["completed_by_role"]
            or reconciliation["completed_at"] is None
        ):
            issues.append(
                Issue(
                    "COMPLETED_RECONCILIATION_MISSING_REVIEW",
                    (
                        "transition_reconciliation_record:"
                        "$.medication_reconciliation"
                    ),
                )
            )

    privacy = handoff_document["privacy_process"]
    signoff = handoff_document["clinician_signoff"]
    release = handoff_document["release_gate"]
    handoff = handoff_document["handoff"]

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

    if release["status"] == "released_for_authorized_documentation_handoff":
        if signoff["status"] != "signed":
            issues.append(
                Issue(
                    "RELEASE_WITHOUT_CLINICIAN_SIGNOFF",
                    "intended_use_handoff_record:$.release_gate.status",
                )
            )
        if release["blocker_codes"]:
            issues.append(
                Issue(
                    "RELEASE_WITH_BLOCKERS",
                    (
                        "intended_use_handoff_record:"
                        "$.release_gate.blocker_codes"
                    ),
                )
            )
        if handoff["acknowledgment_status"] != "acknowledged":
            issues.append(
                Issue(
                    "RELEASE_WITHOUT_HANDOFF_ACKNOWLEDGMENT",
                    (
                        "intended_use_handoff_record:"
                        "$.handoff.acknowledgment_status"
                    ),
                )
            )

    signed_at = (
        parse_iso_datetime(signoff["signed_at"])
        if signoff["signed_at"] is not None
        else None
    )
    released_at = (
        parse_iso_datetime(release["released_at"])
        if release["released_at"] is not None
        else None
    )
    sent_at = (
        parse_iso_datetime(handoff["sent_at"])
        if handoff["sent_at"] is not None
        else None
    )
    reviewed_at = (
        parse_iso_datetime(privacy["reviewed_at"])
        if privacy["reviewed_at"] is not None
        else None
    )

    if signed_at and released_at and signed_at > released_at:
        issues.append(
            Issue(
                "SIGNOFF_AFTER_RELEASE",
                "intended_use_handoff_record:$.release_gate.released_at",
            )
        )
    if released_at and sent_at and released_at > sent_at:
        issues.append(
            Issue(
                "RELEASE_AFTER_HANDOFF_SENT",
                "intended_use_handoff_record:$.handoff.sent_at",
            )
        )
    if reviewed_at and released_at and reviewed_at > released_at:
        issues.append(
            Issue(
                "PRIVACY_REVIEW_AFTER_RELEASE",
                "intended_use_handoff_record:$.privacy_process.reviewed_at",
            )
        )

    issues.sort(key=lambda item: (item.path, item.code))
    return report_payload(
        "cross_record_consistency",
        issues,
        counts={
            "global_record_ids": len(seen),
            "checkpoints": len(planning["checkpoints"]),
            "interventions": len(interventions),
        },
        extra={
            "clinical_semantics_compared": False,
            "date_intervals_inferred": False,
        },
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Check identifiers, links, classifications, status coherence, and "
            "explicit date order. Clinical text is not compared or interpreted."
        )
    )
    parser.add_argument("package", help="Complete local package directory")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        documents, _ = load_package(args.package)
        report = check_consistency(documents)
    except ValidationError as exc:
        report = error_report("cross_record_consistency", exc)
    print_report(report)
    return 1 if report["status"] == "fail" else 0


if __name__ == "__main__":
    sys.exit(main())
