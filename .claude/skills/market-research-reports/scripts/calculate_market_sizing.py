#!/usr/bin/env python3
"""Calculate bounded TAM/SAM/SOM scenarios and reconcile two sizing methods."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from _common import (
    ValidationError,
    error_exit,
    parse_currency,
    parse_fraction,
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

MAX_COMPONENTS = 1_000
MAX_SCENARIOS = 20
MAX_VALUE = 1e18


def _identifier_array(
    value: Any, context: str, *, minimum: int = 0
) -> list[str]:
    items = require_list(value, context, minimum=minimum, maximum=100)
    parsed = [
        require_identifier(item, f"{context}[{index}]")
        for index, item in enumerate(items)
    ]
    require_unique_identifiers(parsed, context)
    return parsed


def _metadata(payload: dict[str, Any]) -> dict[str, Any]:
    raw = require_object(payload.get("metadata"), "metadata")
    required = (
        "market_id",
        "market_definition",
        "geography",
        "currency",
        "base_year",
        "price_basis",
        "unit",
        "taxonomy",
        "taxonomy_version",
        "denominator_id",
        "as_of_date",
    )
    missing = [field for field in required if field not in raw]
    if missing:
        raise ValidationError(f"metadata is missing: {', '.join(missing)}")
    price_basis = require_text(raw["price_basis"], "metadata.price_basis", maximum=20)
    if price_basis not in {"nominal", "real", "current", "constant"}:
        raise ValidationError(
            "metadata.price_basis must be nominal, real, current, or constant"
        )
    return {
        "market_id": require_identifier(raw["market_id"], "metadata.market_id"),
        "market_definition": require_text(
            raw["market_definition"], "metadata.market_definition"
        ),
        "geography": require_text(raw["geography"], "metadata.geography"),
        "currency": parse_currency(raw["currency"], "metadata.currency"),
        "base_year": parse_year(raw["base_year"], "metadata.base_year"),
        "price_basis": price_basis,
        "unit": require_text(raw["unit"], "metadata.unit", maximum=80),
        "taxonomy": require_text(raw["taxonomy"], "metadata.taxonomy"),
        "taxonomy_version": require_text(
            raw["taxonomy_version"], "metadata.taxonomy_version"
        ),
        "denominator_id": require_identifier(
            raw["denominator_id"], "metadata.denominator_id"
        ),
        "as_of_date": parse_iso_date(raw["as_of_date"], "metadata.as_of_date"),
    }


def _top_down(payload: dict[str, Any], denominator_id: str) -> tuple[float, list[str]]:
    section = require_object(payload.get("top_down"), "top_down")
    components = require_list(
        section.get("components"),
        "top_down.components",
        minimum=1,
        maximum=MAX_COMPONENTS,
    )
    component_ids: list[str] = []
    coverage_keys: list[str] = []
    total = 0.0
    for index, item in enumerate(components):
        row = require_object(item, f"top_down.components[{index}]")
        component_id = require_identifier(
            row.get("component_id"),
            f"top_down.components[{index}].component_id",
        )
        component_ids.append(component_id)
        coverage_key = require_identifier(
            row.get("coverage_key"),
            f"top_down.components[{index}].coverage_key",
        )
        coverage_keys.append(coverage_key)
        row_denominator = require_identifier(
            row.get("denominator_id"),
            f"top_down.components[{index}].denominator_id",
        )
        if row_denominator != denominator_id:
            raise ValidationError(
                f"top_down component {component_id} uses denominator "
                f"{row_denominator!r}; expected {denominator_id!r}"
            )
        value = parse_number(
            row.get("value"),
            f"top_down.components[{index}].value",
            minimum=0.0,
            maximum=MAX_VALUE,
        )
        _identifier_array(
            row.get("source_ids"),
            f"top_down.components[{index}].source_ids",
            minimum=1,
        )
        _identifier_array(
            row.get("assumption_ids", []),
            f"top_down.components[{index}].assumption_ids",
        )
        total += value
        if total > MAX_VALUE:
            raise ValidationError("top_down TAM exceeds the supported numeric bound")
    require_unique_identifiers(component_ids, "top_down component IDs")
    require_unique_identifiers(
        coverage_keys,
        "top_down coverage keys (duplicate coverage can double count the market)",
    )
    return total, coverage_keys


def _bottom_up(
    payload: dict[str, Any], denominator_id: str
) -> tuple[float, list[str]]:
    section = require_object(payload.get("bottom_up"), "bottom_up")
    components = require_list(
        section.get("components"),
        "bottom_up.components",
        minimum=1,
        maximum=MAX_COMPONENTS,
    )
    component_ids: list[str] = []
    coverage_keys: list[str] = []
    total = 0.0
    for index, item in enumerate(components):
        row = require_object(item, f"bottom_up.components[{index}]")
        component_id = require_identifier(
            row.get("component_id"),
            f"bottom_up.components[{index}].component_id",
        )
        component_ids.append(component_id)
        coverage_key = require_identifier(
            row.get("coverage_key"),
            f"bottom_up.components[{index}].coverage_key",
        )
        coverage_keys.append(coverage_key)
        row_denominator = require_identifier(
            row.get("denominator_id"),
            f"bottom_up.components[{index}].denominator_id",
        )
        if row_denominator != denominator_id:
            raise ValidationError(
                f"bottom_up component {component_id} uses denominator "
                f"{row_denominator!r}; expected {denominator_id!r}"
            )
        customers = parse_number(
            row.get("customer_count"),
            f"bottom_up.components[{index}].customer_count",
            minimum=0.0,
            maximum=1e15,
        )
        annual_quantity = parse_number(
            row.get("annual_quantity_per_customer"),
            f"bottom_up.components[{index}].annual_quantity_per_customer",
            minimum=0.0,
            maximum=1e12,
        )
        price = parse_number(
            row.get("price_per_unit"),
            f"bottom_up.components[{index}].price_per_unit",
            minimum=0.0,
            maximum=1e15,
        )
        addressable_fraction = parse_fraction(
            row.get("addressable_fraction"),
            f"bottom_up.components[{index}].addressable_fraction",
        )
        _identifier_array(
            row.get("source_ids"),
            f"bottom_up.components[{index}].source_ids",
            minimum=1,
        )
        _identifier_array(
            row.get("assumption_ids", []),
            f"bottom_up.components[{index}].assumption_ids",
        )
        component_value = customers * annual_quantity * price * addressable_fraction
        if component_value > MAX_VALUE:
            raise ValidationError(
                f"bottom_up component {component_id} exceeds the numeric bound"
            )
        total += component_value
        if total > MAX_VALUE:
            raise ValidationError("bottom_up TAM exceeds the supported numeric bound")
    require_unique_identifiers(component_ids, "bottom_up component IDs")
    require_unique_identifiers(
        coverage_keys,
        "bottom_up coverage keys (duplicate coverage can double count the market)",
    )
    return total, coverage_keys


def _scenarios(payload: dict[str, Any]) -> list[dict[str, Any]]:
    raw_scenarios = require_list(
        payload.get("scenarios"),
        "scenarios",
        minimum=2,
        maximum=MAX_SCENARIOS,
    )
    scenarios: list[dict[str, Any]] = []
    scenario_ids: list[str] = []
    parameter_pairs: list[tuple[float, float]] = []
    for index, item in enumerate(raw_scenarios):
        row = require_object(item, f"scenarios[{index}]")
        scenario_id = require_identifier(
            row.get("scenario_id"), f"scenarios[{index}].scenario_id"
        )
        scenario_ids.append(scenario_id)
        serviceable = parse_fraction(
            row.get("serviceable_fraction"),
            f"scenarios[{index}].serviceable_fraction",
        )
        obtainable = parse_fraction(
            row.get("obtainable_share"),
            f"scenarios[{index}].obtainable_share",
        )
        parameter_pairs.append((serviceable, obtainable))
        assumptions = require_list(
            row.get("assumptions"),
            f"scenarios[{index}].assumptions",
            minimum=1,
            maximum=100,
        )
        parsed_assumptions = [
            require_text(value, f"scenarios[{index}].assumptions[{position}]")
            for position, value in enumerate(assumptions)
        ]
        scenarios.append(
            {
                "scenario_id": scenario_id,
                "label": require_text(
                    row.get("label"), f"scenarios[{index}].label", maximum=120
                ),
                "serviceable_fraction": serviceable,
                "obtainable_share": obtainable,
                "source_ids": _identifier_array(
                    row.get("source_ids", []),
                    f"scenarios[{index}].source_ids",
                ),
                "assumptions": parsed_assumptions,
            }
        )
    require_unique_identifiers(scenario_ids, "scenario IDs")
    if len(set(parameter_pairs)) < 2:
        raise ValidationError(
            "at least two scenarios must use different sizing assumptions"
        )
    return scenarios


def calculate(payload: dict[str, Any]) -> dict[str, Any]:
    schema_version = require_text(
        payload.get("schema_version"), "schema_version", maximum=10
    )
    if schema_version != "1.0":
        raise ValidationError("schema_version must be '1.0'")
    metadata = _metadata(payload)
    top_down_tam, top_keys = _top_down(payload, metadata["denominator_id"])
    bottom_up_tam, bottom_keys = _bottom_up(payload, metadata["denominator_id"])
    scenarios = _scenarios(payload)
    tolerance = parse_number(
        payload.get("reconciliation_tolerance_percent", 20.0),
        "reconciliation_tolerance_percent",
        minimum=0.0,
        maximum=100.0,
    )

    midpoint = (top_down_tam + bottom_up_tam) / 2.0
    reconciliation_percent = (
        0.0
        if midpoint == 0.0
        else abs(top_down_tam - bottom_up_tam) / midpoint * 100.0
    )
    warnings: list[str] = []
    if reconciliation_percent > tolerance:
        warnings.append(
            "top-down and bottom-up TAM estimates exceed the stated "
            "reconciliation tolerance; investigate scope, denominators, and assumptions"
        )
    if set(top_keys) != set(bottom_keys):
        warnings.append(
            "the methods use different coverage-key sets; explain the scope difference "
            "before treating them as direct reconciliation estimates"
        )

    scenario_results: list[dict[str, Any]] = []
    for scenario in scenarios:
        methods: dict[str, dict[str, float]] = {}
        for method, tam in (
            ("top_down", top_down_tam),
            ("bottom_up", bottom_up_tam),
        ):
            sam = tam * scenario["serviceable_fraction"]
            som = sam * scenario["obtainable_share"]
            methods[method] = {"tam": tam, "sam": sam, "som": som}
        scenario_results.append({**scenario, "methods": methods})

    all_som = [
        result["methods"][method]["som"]
        for result in scenario_results
        for method in ("top_down", "bottom_up")
    ]
    return {
        "schema_version": "1.0",
        "metadata": metadata,
        "method_estimates": {
            "top_down_tam": top_down_tam,
            "bottom_up_tam": bottom_up_tam,
        },
        "reconciliation": {
            "absolute_difference": abs(top_down_tam - bottom_up_tam),
            "difference_percent_of_midpoint": reconciliation_percent,
            "tolerance_percent": tolerance,
            "within_tolerance": reconciliation_percent <= tolerance,
        },
        "scenario_results": scenario_results,
        "som_range_across_methods_and_scenarios": {
            "minimum": min(all_som),
            "maximum": max(all_som),
        },
        "warnings": warnings,
        "interpretation": (
            "These are conditional scenario calculations, not a single asserted "
            "market truth."
        ),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Calculate local top-down and bottom-up TAM/SAM/SOM scenarios, "
            "detect duplicate coverage keys, and report reconciliation."
        )
    )
    parser.add_argument("input", help="Local .json market-sizing input")
    parser.add_argument("--output", help="Optional local .json result")
    parser.add_argument(
        "--force", action="store_true", help="Replace an existing --output file"
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        payload = require_object(read_json(args.input), "root")
        write_json_report(calculate(payload), args.output, force=args.force)
        return 0
    except ValidationError as exc:
        return error_exit(exc)


if __name__ == "__main__":
    raise SystemExit(main())
