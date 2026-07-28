#!/usr/bin/env python3
"""Validate a complete, evidence-linked competitor-feature matrix CSV."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from _common import (
    MAX_ROWS,
    ValidationError,
    error_exit,
    parse_iso_date,
    read_csv_records,
    read_json,
    require_identifier,
    require_list,
    require_object,
    require_text,
    split_ids,
    write_json_report,
)

REQUIRED_FIELDS = (
    "competitor_id",
    "competitor_name",
    "feature_id",
    "feature_name",
    "status",
    "evidence_source_ids",
    "as_of_date",
    "geography",
    "product_scope",
    "notes",
)
STATUSES = {"yes", "no", "partial", "unknown", "not-applicable"}


def _source_ids(path: str | Path) -> set[str]:
    if Path(path).suffix.lower() == ".csv":
        records: list[dict[str, Any]] = read_csv_records(
            path, required_fields=("source_id",)
        )
    elif Path(path).suffix.lower() == ".json":
        payload = read_json(path)
        if isinstance(payload, dict):
            raw = require_list(
                payload.get("sources"), "sources", minimum=1, maximum=MAX_ROWS
            )
        else:
            raw = require_list(payload, "sources", minimum=1, maximum=MAX_ROWS)
        records = [
            require_object(record, f"sources[{index}]")
            for index, record in enumerate(raw)
        ]
    else:
        raise ValidationError("source ledger must be .csv or .json")
    identifiers: set[str] = set()
    for index, record in enumerate(records):
        source_id = require_identifier(
            record.get("source_id"), f"sources[{index}].source_id"
        )
        if source_id in identifiers:
            raise ValidationError(f"duplicate source_id in ledger: {source_id}")
        identifiers.add(source_id)
    return identifiers


def validate(
    rows: list[dict[str, str]], known_source_ids: set[str] | None = None
) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    competitors: dict[str, str] = {}
    features: dict[str, str] = {}
    pairs: set[tuple[str, str]] = set()
    scope_values: set[tuple[str, str, str]] = set()
    cited_ids: set[str] = set()
    status_counts: dict[str, int] = {}

    for index, row in enumerate(rows, start=2):
        context = f"row {index}"
        try:
            competitor_id = require_identifier(
                row["competitor_id"], f"{context}.competitor_id"
            )
            competitor_name = require_text(
                row["competitor_name"], f"{context}.competitor_name", maximum=200
            )
            existing_competitor = competitors.get(competitor_id)
            if existing_competitor and existing_competitor != competitor_name:
                raise ValidationError(
                    f"{context}: competitor_id {competitor_id} has inconsistent names"
                )
            competitors[competitor_id] = competitor_name

            feature_id = require_identifier(row["feature_id"], f"{context}.feature_id")
            feature_name = require_text(
                row["feature_name"], f"{context}.feature_name", maximum=200
            )
            existing_feature = features.get(feature_id)
            if existing_feature and existing_feature != feature_name:
                raise ValidationError(
                    f"{context}: feature_id {feature_id} has inconsistent names"
                )
            features[feature_id] = feature_name

            pair = (competitor_id, feature_id)
            if pair in pairs:
                raise ValidationError(
                    f"{context}: duplicate competitor-feature pair "
                    f"{competitor_id}/{feature_id}"
                )
            pairs.add(pair)

            status = require_text(row["status"], f"{context}.status", maximum=20)
            if status not in STATUSES:
                raise ValidationError(
                    f"{context}.status must be one of {', '.join(sorted(STATUSES))}"
                )
            status_counts[status] = status_counts.get(status, 0) + 1
            evidence_ids = split_ids(
                row["evidence_source_ids"],
                f"{context}.evidence_source_ids",
                allow_empty=True,
            )
            if status not in {"unknown", "not-applicable"} and not evidence_ids:
                raise ValidationError(
                    f"{context}: status {status!r} requires evidence_source_ids"
                )
            cited_ids.update(evidence_ids)

            as_of_date = parse_iso_date(row["as_of_date"], f"{context}.as_of_date")
            geography = require_text(
                row["geography"], f"{context}.geography", maximum=200
            )
            product_scope = require_text(
                row["product_scope"], f"{context}.product_scope", maximum=500
            )
            scope_values.add((as_of_date, geography, product_scope))
            require_text(row["notes"], f"{context}.notes", allow_empty=True)
        except ValidationError as exc:
            errors.append(str(exc))

    expected_pairs = {
        (competitor_id, feature_id)
        for competitor_id in competitors
        for feature_id in features
    }
    missing_pairs = sorted(expected_pairs - pairs)
    if missing_pairs:
        preview = ", ".join(f"{a}/{b}" for a, b in missing_pairs[:20])
        suffix = "" if len(missing_pairs) <= 20 else ", ..."
        errors.append(
            f"matrix is incomplete; missing {len(missing_pairs)} pairs: "
            f"{preview}{suffix}"
        )
    if len(scope_values) > 1:
        errors.append(
            "matrix rows use inconsistent as_of_date/geography/product_scope values"
        )

    missing_sources: list[str] = []
    if known_source_ids is None:
        warnings.append(
            "evidence IDs were syntax-checked but not cross-checked; pass "
            "--source-ledger for referential integrity"
        )
    else:
        missing_sources = sorted(cited_ids - known_source_ids)
        if missing_sources:
            errors.append(
                "evidence IDs missing from source ledger: "
                + ", ".join(missing_sources)
            )

    return {
        "valid": not errors,
        "row_count": len(rows),
        "competitor_count": len(competitors),
        "feature_count": len(features),
        "expected_pair_count": len(expected_pairs),
        "status_counts": dict(sorted(status_counts.items())),
        "cited_source_count": len(cited_ids),
        "warnings": warnings,
        "errors": errors,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Validate a strict local competitor-feature matrix for complete coverage, "
            "consistent scope, and evidence links."
        )
    )
    parser.add_argument("matrix", help="Local .csv competitor matrix")
    parser.add_argument(
        "--source-ledger",
        help="Optional local .csv/.json source ledger for ID cross-checking",
    )
    parser.add_argument("--output", help="Optional local .json validation report")
    parser.add_argument(
        "--force", action="store_true", help="Replace an existing --output file"
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        rows = read_csv_records(args.matrix, required_fields=REQUIRED_FIELDS)
        known = _source_ids(args.source_ledger) if args.source_ledger else None
        report = validate(rows, known)
        write_json_report(report, args.output, force=args.force)
        return 0 if report["valid"] else 1
    except ValidationError as exc:
        return error_exit(exc)


if __name__ == "__main__":
    raise SystemExit(main())
