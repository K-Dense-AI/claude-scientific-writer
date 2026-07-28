#!/usr/bin/env python3
"""Validate a local market-research source/evidence ledger."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import urlsplit

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
    write_json_report,
)

REQUIRED_FIELDS = (
    "source_id",
    "title",
    "publisher",
    "url",
    "source_type",
    "publication_date",
    "retrieval_date",
    "geography",
    "currency",
    "base_year",
    "price_basis",
    "measure_type",
    "unit",
    "taxonomy",
    "taxonomy_version",
    "revision_status",
    "method",
    "sample",
    "limitations",
    "license_or_terms",
    "archive_path",
)

SOURCE_TYPES = {
    "official_statistics",
    "regulator_filing",
    "company_filing",
    "survey",
    "interview",
    "academic",
    "industry_association",
    "paid_secondary",
    "news",
    "methodological_guidance",
    "other",
}
PRICE_BASES = {
    "nominal",
    "real",
    "current",
    "constant",
    "chained",
    "mixed",
    "not-applicable",
}
MEASURE_TYPES = {
    "stock",
    "flow",
    "index",
    "share",
    "count",
    "rate",
    "price",
    "mixed",
    "not-applicable",
}
REVISION_STATUSES = {
    "preliminary",
    "revised",
    "final",
    "current",
    "vintage",
    "unknown",
    "not-applicable",
}


def _publication_date(value: Any, context: str) -> str:
    text = require_text(value, context, maximum=10)
    if text == "not-stated":
        return text
    if len(text) == 4:
        parse_year(text, context)
        return text
    return parse_iso_date(text, context)


def _url(value: Any, context: str) -> str:
    text = require_text(value, context, maximum=2_048)
    parsed = urlsplit(text)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValidationError(f"{context} must be an absolute HTTP(S) URL")
    if parsed.username or parsed.password:
        raise ValidationError(f"{context} must not contain embedded credentials")
    return text


def _archive_path(value: Any, context: str) -> str:
    text = require_text(value, context, allow_empty=True, maximum=1_024)
    if not text:
        return ""
    path = PurePosixPath(text)
    if path.is_absolute() or ".." in path.parts:
        raise ValidationError(
            f"{context} must be a relative path without parent traversal"
        )
    return text


def _load_records(path: str | Path) -> list[dict[str, Any]]:
    suffix = Path(path).suffix.lower()
    if suffix == ".csv":
        return read_csv_records(path, required_fields=REQUIRED_FIELDS)
    if suffix == ".json":
        payload = read_json(path)
        if isinstance(payload, dict):
            records = require_list(
                payload.get("sources"), "sources", minimum=1, maximum=MAX_ROWS
            )
        else:
            records = require_list(payload, "source ledger", minimum=1, maximum=MAX_ROWS)
        return [require_object(row, f"sources[{index}]") for index, row in enumerate(records)]
    raise ValidationError("input must be .csv or .json")


def validate_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    valid_ids: list[str] = []
    type_counts: dict[str, int] = {}

    for index, record in enumerate(records, start=1):
        context = f"record {index}"
        missing = [field for field in REQUIRED_FIELDS if field not in record]
        if missing:
            errors.append(f"{context}: missing fields: {', '.join(missing)}")
            continue
        try:
            source_id = require_identifier(record["source_id"], f"{context}.source_id")
            valid_ids.append(source_id)
            require_text(record["title"], f"{context}.title")
            require_text(record["publisher"], f"{context}.publisher")
            _url(record["url"], f"{context}.url")

            source_type = require_text(
                record["source_type"], f"{context}.source_type", maximum=40
            )
            if source_type not in SOURCE_TYPES:
                raise ValidationError(
                    f"{context}.source_type must be one of "
                    f"{', '.join(sorted(SOURCE_TYPES))}"
                )
            type_counts[source_type] = type_counts.get(source_type, 0) + 1

            publication = _publication_date(
                record["publication_date"], f"{context}.publication_date"
            )
            retrieval = parse_iso_date(
                record["retrieval_date"], f"{context}.retrieval_date"
            )
            if len(publication) == 10 and date.fromisoformat(retrieval) < date.fromisoformat(
                publication
            ):
                raise ValidationError(
                    f"{context}.retrieval_date precedes publication_date"
                )
            if publication == "not-stated":
                warnings.append(f"{source_id}: publication date is not stated")

            require_text(record["geography"], f"{context}.geography")
            currency = parse_currency(
                record["currency"], f"{context}.currency", allow_empty=True
            )
            base_year_raw = require_text(
                record["base_year"], f"{context}.base_year", allow_empty=True, maximum=4
            )
            if base_year_raw:
                parse_year(base_year_raw, f"{context}.base_year")

            price_basis = require_text(
                record["price_basis"], f"{context}.price_basis", maximum=20
            )
            if price_basis not in PRICE_BASES:
                raise ValidationError(
                    f"{context}.price_basis must be one of "
                    f"{', '.join(sorted(PRICE_BASES))}"
                )
            if currency and (not base_year_raw or price_basis == "not-applicable"):
                raise ValidationError(
                    f"{context}: monetary evidence requires base_year and price_basis"
                )

            measure_type = require_text(
                record["measure_type"], f"{context}.measure_type", maximum=20
            )
            if measure_type not in MEASURE_TYPES:
                raise ValidationError(
                    f"{context}.measure_type must be one of "
                    f"{', '.join(sorted(MEASURE_TYPES))}"
                )
            require_text(record["unit"], f"{context}.unit")
            require_text(
                record["taxonomy"], f"{context}.taxonomy", allow_empty=True
            )
            require_text(
                record["taxonomy_version"],
                f"{context}.taxonomy_version",
                allow_empty=True,
            )

            revision_status = require_text(
                record["revision_status"], f"{context}.revision_status", maximum=20
            )
            if revision_status not in REVISION_STATUSES:
                raise ValidationError(
                    f"{context}.revision_status must be one of "
                    f"{', '.join(sorted(REVISION_STATUSES))}"
                )
            if revision_status == "unknown":
                warnings.append(f"{source_id}: revision status is unknown")

            require_text(record["method"], f"{context}.method")
            require_text(record["sample"], f"{context}.sample", allow_empty=True)
            require_text(record["limitations"], f"{context}.limitations")
            require_text(
                record["license_or_terms"], f"{context}.license_or_terms"
            )
            _archive_path(record["archive_path"], f"{context}.archive_path")
        except ValidationError as exc:
            errors.append(str(exc))

    try:
        require_unique_identifiers(valid_ids, "source ledger")
    except ValidationError as exc:
        errors.append(str(exc))

    return {
        "valid": not errors,
        "source_count": len(records),
        "source_type_counts": dict(sorted(type_counts.items())),
        "warnings": warnings,
        "errors": errors,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Validate a strict local CSV/JSON evidence ledger. "
            "No network requests are made."
        )
    )
    parser.add_argument("ledger", help="Local .csv or .json source ledger")
    parser.add_argument("--output", help="Optional local .json validation report")
    parser.add_argument(
        "--force", action="store_true", help="Replace an existing --output file"
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        report = validate_records(_load_records(args.ledger))
        write_json_report(report, args.output, force=args.force)
        return 0 if report["valid"] else 1
    except ValidationError as exc:
        return error_exit(exc)


if __name__ == "__main__":
    raise SystemExit(main())
