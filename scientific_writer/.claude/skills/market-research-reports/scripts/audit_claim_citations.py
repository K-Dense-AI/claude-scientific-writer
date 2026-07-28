#!/usr/bin/env python3
"""Audit claim-to-source mappings in local CSV ledgers."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from _common import (
    MAX_ROWS,
    ValidationError,
    error_exit,
    parse_currency,
    parse_iso_date,
    parse_year,
    read_csv_records,
    read_json,
    require_identifier,
    require_list,
    require_object,
    require_text,
    require_unique_identifiers,
    split_ids,
    write_json_report,
)

CLAIM_FIELDS = (
    "claim_id",
    "claim_text",
    "claim_type",
    "source_ids",
    "calculation_id",
    "assumption_ids",
    "location",
    "as_of_date",
    "geography",
    "currency",
    "base_year",
    "price_basis",
    "measure_type",
    "unit",
    "taxonomy",
    "taxonomy_version",
    "revision_status",
    "confidence",
    "notes",
)
CLAIM_TYPES = {
    "quantitative_fact",
    "quantitative_estimate",
    "calculation",
    "forecast",
    "qualitative_fact",
    "opinion",
    "recommendation",
}
QUANTITATIVE_TYPES = {
    "quantitative_fact",
    "quantitative_estimate",
    "calculation",
    "forecast",
}
EVIDENCE_REQUIRED_TYPES = CLAIM_TYPES - {"opinion", "recommendation"}
REVISION_STATUSES = {
    "preliminary",
    "revised",
    "final",
    "current",
    "vintage",
    "unknown",
    "not-applicable",
}
CONFIDENCE_LEVELS = {"high", "medium", "low", "not-assessed"}
MEASURE_TYPES = {
    "stock",
    "flow",
    "index",
    "share",
    "count",
    "rate",
    "price",
    "not-applicable",
}


def _load_sources(path: str | Path) -> list[dict[str, Any]]:
    suffix = Path(path).suffix.lower()
    if suffix == ".csv":
        return read_csv_records(
            path,
            required_fields=("source_id", "publication_date", "retrieval_date"),
        )
    if suffix == ".json":
        payload = read_json(path)
        raw = (
            require_list(
                payload.get("sources"), "sources", minimum=1, maximum=MAX_ROWS
            )
            if isinstance(payload, dict)
            else require_list(payload, "sources", minimum=1, maximum=MAX_ROWS)
        )
        return [
            require_object(record, f"sources[{index}]")
            for index, record in enumerate(raw)
        ]
    raise ValidationError("source ledger must be .csv or .json")


def _source_index(records: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    for position, record in enumerate(records):
        context = f"sources[{position}]"
        source_id = require_identifier(record.get("source_id"), f"{context}.source_id")
        if source_id in index:
            raise ValidationError(f"duplicate source_id: {source_id}")
        publication = require_text(
            record.get("publication_date"), f"{context}.publication_date", maximum=10
        )
        if publication != "not-stated":
            if len(publication) == 4:
                parse_year(publication, f"{context}.publication_date")
            else:
                parse_iso_date(publication, f"{context}.publication_date")
        parse_iso_date(record.get("retrieval_date"), f"{context}.retrieval_date")
        index[source_id] = record
    return index


def audit(
    claims: list[dict[str, str]], sources: list[dict[str, Any]]
) -> dict[str, Any]:
    source_index = _source_index(sources)
    errors: list[str] = []
    warnings: list[str] = []
    claim_ids: list[str] = []
    cited_source_ids: set[str] = set()
    type_counts: dict[str, int] = {}
    uncited_claims: list[str] = []

    for row_number, claim in enumerate(claims, start=2):
        context = f"claim row {row_number}"
        try:
            claim_id = require_identifier(claim["claim_id"], f"{context}.claim_id")
            claim_ids.append(claim_id)
            claim_text = require_text(claim["claim_text"], f"{context}.claim_text")
            if any(marker in claim_text.upper() for marker in ("[TBD]", "[TODO]")):
                warnings.append(f"{claim_id}: claim text contains a placeholder")

            claim_type = require_text(
                claim["claim_type"], f"{context}.claim_type", maximum=30
            )
            if claim_type not in CLAIM_TYPES:
                raise ValidationError(
                    f"{context}.claim_type must be one of "
                    f"{', '.join(sorted(CLAIM_TYPES))}"
                )
            type_counts[claim_type] = type_counts.get(claim_type, 0) + 1

            source_ids = split_ids(
                claim["source_ids"], f"{context}.source_ids", allow_empty=True
            )
            cited_source_ids.update(source_ids)
            if claim_type in EVIDENCE_REQUIRED_TYPES and not source_ids:
                uncited_claims.append(claim_id)
                raise ValidationError(
                    f"{context}: {claim_type} requires at least one source_id"
                )
            missing_sources = sorted(set(source_ids) - set(source_index))
            if missing_sources:
                raise ValidationError(
                    f"{context}: source IDs are absent from the ledger: "
                    f"{', '.join(missing_sources)}"
                )

            calculation_id = require_text(
                claim["calculation_id"],
                f"{context}.calculation_id",
                allow_empty=True,
                maximum=96,
            )
            if calculation_id:
                require_identifier(calculation_id, f"{context}.calculation_id")
            assumption_ids = split_ids(
                claim["assumption_ids"],
                f"{context}.assumption_ids",
                allow_empty=True,
            )
            if claim_type in {"calculation", "forecast"} and not calculation_id:
                raise ValidationError(
                    f"{context}: {claim_type} requires calculation_id"
                )
            if claim_type == "forecast" and not assumption_ids:
                raise ValidationError(
                    f"{context}: forecast requires assumption_ids"
                )

            require_text(claim["location"], f"{context}.location")
            parse_iso_date(claim["as_of_date"], f"{context}.as_of_date")
            require_text(claim["geography"], f"{context}.geography")
            currency = parse_currency(
                claim["currency"], f"{context}.currency", allow_empty=True
            )
            base_year = require_text(
                claim["base_year"],
                f"{context}.base_year",
                allow_empty=True,
                maximum=4,
            )
            if base_year:
                parse_year(base_year, f"{context}.base_year")
            price_basis = require_text(
                claim["price_basis"], f"{context}.price_basis", maximum=20
            )
            if price_basis not in {
                "nominal",
                "real",
                "current",
                "constant",
                "not-applicable",
            }:
                raise ValidationError(
                    f"{context}.price_basis has an unsupported value"
                )
            if currency and (not base_year or price_basis == "not-applicable"):
                raise ValidationError(
                    f"{context}: monetary claims require base_year and price_basis"
                )

            measure_type = require_text(
                claim["measure_type"], f"{context}.measure_type", maximum=20
            )
            if measure_type not in MEASURE_TYPES:
                raise ValidationError(
                    f"{context}.measure_type has an unsupported value"
                )
            unit = require_text(claim["unit"], f"{context}.unit")
            if claim_type in QUANTITATIVE_TYPES and (
                measure_type == "not-applicable" or unit == "not-applicable"
            ):
                raise ValidationError(
                    f"{context}: quantitative claims require an explicit unit "
                    "and measure_type"
                )

            require_text(
                claim["taxonomy"], f"{context}.taxonomy", allow_empty=True
            )
            require_text(
                claim["taxonomy_version"],
                f"{context}.taxonomy_version",
                allow_empty=True,
            )
            revision_status = require_text(
                claim["revision_status"],
                f"{context}.revision_status",
                maximum=20,
            )
            if revision_status not in REVISION_STATUSES:
                raise ValidationError(
                    f"{context}.revision_status has an unsupported value"
                )
            confidence = require_text(
                claim["confidence"], f"{context}.confidence", maximum=20
            )
            if confidence not in CONFIDENCE_LEVELS:
                raise ValidationError(
                    f"{context}.confidence must be one of "
                    f"{', '.join(sorted(CONFIDENCE_LEVELS))}"
                )
            require_text(claim["notes"], f"{context}.notes", allow_empty=True)
        except ValidationError as exc:
            errors.append(str(exc))

    try:
        require_unique_identifiers(claim_ids, "claim ledger")
    except ValidationError as exc:
        errors.append(str(exc))

    unused_sources = sorted(set(source_index) - cited_source_ids)
    if unused_sources:
        warnings.append(
            f"{len(unused_sources)} source ledger entries are not mapped to a claim"
        )
    return {
        "valid": not errors,
        "claim_count": len(claims),
        "source_count": len(source_index),
        "claim_type_counts": dict(sorted(type_counts.items())),
        "cited_source_count": len(cited_source_ids),
        "uncited_claim_ids": sorted(set(uncited_claims)),
        "unused_source_ids": unused_sources,
        "warnings": warnings,
        "errors": errors,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Audit a strict local claims CSV against a local source ledger. "
            "Every evidence claim must map to explicit source IDs."
        )
    )
    parser.add_argument("claims", help="Local .csv claims ledger")
    parser.add_argument("sources", help="Local .csv or .json source ledger")
    parser.add_argument("--output", help="Optional local .json audit report")
    parser.add_argument(
        "--force", action="store_true", help="Replace an existing --output file"
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        claims = read_csv_records(args.claims, required_fields=CLAIM_FIELDS)
        report = audit(claims, _load_sources(args.sources))
        write_json_report(report, args.output, force=args.force)
        return 0 if report["valid"] else 1
    except ValidationError as exc:
        return error_exit(exc)


if __name__ == "__main__":
    raise SystemExit(main())
