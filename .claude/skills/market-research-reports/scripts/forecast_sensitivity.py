#!/usr/bin/env python3
"""Generate deterministic scenario forecasts and one-way growth sensitivity."""

from __future__ import annotations

import argparse
from typing import Any

from _common import (
    ValidationError,
    error_exit,
    parse_currency,
    parse_iso_date,
    parse_number,
    parse_year,
    read_json,
    require_identifier,
    require_list,
    require_object,
    require_text,
    require_unique_identifiers,
    write_json_report,
)

MAX_VALUE = 1e18
MAX_HORIZON = 50
MAX_SCENARIOS = 20


def _identifiers(value: Any, context: str, *, minimum: int = 0) -> list[str]:
    items = require_list(value, context, minimum=minimum, maximum=100)
    parsed = [
        require_identifier(item, f"{context}[{index}]")
        for index, item in enumerate(items)
    ]
    require_unique_identifiers(parsed, context)
    return parsed


def _integer(value: Any, context: str, minimum: int, maximum: int) -> int:
    if type(value) is not int:
        raise ValidationError(f"{context} must be an integer")
    if not minimum <= value <= maximum:
        raise ValidationError(f"{context} must be between {minimum} and {maximum}")
    return value


def _metadata(payload: dict[str, Any]) -> dict[str, Any]:
    raw = require_object(payload.get("metadata"), "metadata")
    required = (
        "series_id",
        "description",
        "geography",
        "currency",
        "base_year",
        "price_basis",
        "unit",
        "measure_type",
        "as_of_date",
        "source_ids",
    )
    missing = [field for field in required if field not in raw]
    if missing:
        raise ValidationError(f"metadata is missing: {', '.join(missing)}")
    currency = parse_currency(raw["currency"], "metadata.currency", allow_empty=True)
    base_year_text = require_text(
        raw["base_year"], "metadata.base_year", allow_empty=True, maximum=4
    )
    base_year: int | None = None
    if base_year_text:
        base_year = parse_year(base_year_text, "metadata.base_year")
    price_basis = require_text(raw["price_basis"], "metadata.price_basis", maximum=20)
    if price_basis not in {
        "nominal",
        "real",
        "current",
        "constant",
        "not-applicable",
    }:
        raise ValidationError("metadata.price_basis has an unsupported value")
    if currency and (base_year is None or price_basis == "not-applicable"):
        raise ValidationError(
            "monetary forecasts require currency, base_year, and price_basis"
        )
    measure_type = require_text(
        raw["measure_type"], "metadata.measure_type", maximum=20
    )
    if measure_type not in {"stock", "flow", "index", "share", "count", "rate", "price"}:
        raise ValidationError("metadata.measure_type has an unsupported value")
    return {
        "series_id": require_identifier(raw["series_id"], "metadata.series_id"),
        "description": require_text(raw["description"], "metadata.description"),
        "geography": require_text(raw["geography"], "metadata.geography"),
        "currency": currency,
        "base_year": base_year,
        "price_basis": price_basis,
        "unit": require_text(raw["unit"], "metadata.unit", maximum=80),
        "measure_type": measure_type,
        "as_of_date": parse_iso_date(raw["as_of_date"], "metadata.as_of_date"),
        "source_ids": _identifiers(
            raw["source_ids"], "metadata.source_ids", minimum=1
        ),
    }


def _rate_path(value: Any, context: str, horizon: int) -> list[float]:
    items = require_list(value, context, minimum=horizon, maximum=horizon)
    return [
        parse_number(
            item,
            f"{context}[{index}]",
            minimum=-0.99,
            maximum=10.0,
        )
        for index, item in enumerate(items)
    ]


def _project(
    start_year: int, start_value: float, rates: list[float]
) -> list[dict[str, float | int]]:
    observations: list[dict[str, float | int]] = [
        {"year": start_year, "value": start_value}
    ]
    value = start_value
    for offset, rate in enumerate(rates, start=1):
        value *= 1.0 + rate
        if value > MAX_VALUE:
            raise ValidationError("forecast exceeds the supported numeric bound")
        observations.append(
            {"year": start_year + offset, "value": value, "growth_rate": rate}
        )
    return observations


def _cagr(start: float, end: float, periods: int) -> float | None:
    if periods <= 0 or start <= 0.0 or end < 0.0:
        return None
    return (end / start) ** (1.0 / periods) - 1.0


def forecast(payload: dict[str, Any]) -> dict[str, Any]:
    schema_version = require_text(
        payload.get("schema_version"), "schema_version", maximum=10
    )
    if schema_version != "1.0":
        raise ValidationError("schema_version must be '1.0'")
    metadata = _metadata(payload)
    start_year = parse_year(payload.get("start_year"), "start_year")
    start_value = parse_number(
        payload.get("start_value"),
        "start_value",
        minimum=0.0,
        maximum=MAX_VALUE,
    )
    horizon = _integer(
        payload.get("horizon_years"),
        "horizon_years",
        minimum=1,
        maximum=MAX_HORIZON,
    )

    raw_scenarios = require_list(
        payload.get("scenarios"),
        "scenarios",
        minimum=2,
        maximum=MAX_SCENARIOS,
    )
    scenario_ids: list[str] = []
    unique_paths: set[tuple[float, ...]] = set()
    scenario_results: list[dict[str, Any]] = []
    scenario_rates: dict[str, list[float]] = {}
    for index, item in enumerate(raw_scenarios):
        row = require_object(item, f"scenarios[{index}]")
        if "probability" in row:
            raise ValidationError(
                f"scenarios[{index}].probability is not accepted; do not assign "
                "probabilities without a separately validated probabilistic model"
            )
        scenario_id = require_identifier(
            row.get("scenario_id"), f"scenarios[{index}].scenario_id"
        )
        scenario_ids.append(scenario_id)
        rates = _rate_path(
            row.get("annual_growth_rates"),
            f"scenarios[{index}].annual_growth_rates",
            horizon,
        )
        unique_paths.add(tuple(rates))
        scenario_rates[scenario_id] = rates
        assumptions = require_list(
            row.get("assumptions"),
            f"scenarios[{index}].assumptions",
            minimum=1,
            maximum=100,
        )
        observations = _project(start_year, start_value, rates)
        scenario_results.append(
            {
                "scenario_id": scenario_id,
                "label": require_text(
                    row.get("label"), f"scenarios[{index}].label", maximum=120
                ),
                "source_ids": _identifiers(
                    row.get("source_ids", []),
                    f"scenarios[{index}].source_ids",
                ),
                "assumptions": [
                    require_text(
                        assumption,
                        f"scenarios[{index}].assumptions[{position}]",
                    )
                    for position, assumption in enumerate(assumptions)
                ],
                "annual_growth_rates": rates,
                "observations": observations,
                "endpoint": observations[-1]["value"],
                "cagr": _cagr(start_value, float(observations[-1]["value"]), horizon),
            }
        )
    require_unique_identifiers(scenario_ids, "scenario IDs")
    if len(unique_paths) < 2:
        raise ValidationError("at least two scenarios must use different rate paths")

    sensitivity = require_object(payload.get("sensitivity"), "sensitivity")
    base_scenario_id = require_identifier(
        sensitivity.get("base_scenario_id"), "sensitivity.base_scenario_id"
    )
    if base_scenario_id not in scenario_rates:
        raise ValidationError(
            "sensitivity.base_scenario_id must reference one of the scenarios"
        )
    shifts_raw = require_list(
        sensitivity.get("growth_rate_shifts"),
        "sensitivity.growth_rate_shifts",
        minimum=2,
        maximum=21,
    )
    shifts = [
        parse_number(
            value,
            f"sensitivity.growth_rate_shifts[{index}]",
            minimum=-0.5,
            maximum=0.5,
        )
        for index, value in enumerate(shifts_raw)
    ]
    if len(shifts) != len(set(shifts)):
        raise ValidationError("sensitivity.growth_rate_shifts must be unique")
    sensitivity_results: list[dict[str, Any]] = []
    for shift in sorted(shifts):
        shifted_rates = [rate + shift for rate in scenario_rates[base_scenario_id]]
        if any(rate < -0.99 or rate > 10.0 for rate in shifted_rates):
            raise ValidationError(
                f"sensitivity shift {shift} produces an out-of-bounds growth rate"
            )
        observations = _project(start_year, start_value, shifted_rates)
        sensitivity_results.append(
            {
                "growth_rate_shift": shift,
                "annual_growth_rates": shifted_rates,
                "endpoint": observations[-1]["value"],
                "observations": observations,
            }
        )

    ranges: list[dict[str, float | int]] = []
    for offset in range(horizon + 1):
        values = [
            float(result["observations"][offset]["value"])
            for result in scenario_results
        ]
        ranges.append(
            {
                "year": start_year + offset,
                "minimum": min(values),
                "maximum": max(values),
            }
        )

    return {
        "schema_version": "1.0",
        "metadata": metadata,
        "start_year": start_year,
        "start_value": start_value,
        "horizon_years": horizon,
        "scenarios": scenario_results,
        "scenario_range_by_year": ranges,
        "sensitivity": {
            "base_scenario_id": base_scenario_id,
            "results": sensitivity_results,
        },
        "interpretation": (
            "Ranges are conditional on documented scenarios and are not confidence "
            "intervals or assigned probabilities."
        ),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Generate bounded local scenario forecasts and one-way growth-rate "
            "sensitivity. No network or random sampling is used."
        )
    )
    parser.add_argument("input", help="Local .json forecast input")
    parser.add_argument("--output", help="Optional local .json result")
    parser.add_argument(
        "--force", action="store_true", help="Replace an existing --output file"
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        payload = require_object(read_json(args.input), "root")
        write_json_report(forecast(payload), args.output, force=args.force)
        return 0
    except ValidationError as exc:
        return error_exit(exc)


if __name__ == "__main__":
    raise SystemExit(main())
