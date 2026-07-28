#!/usr/bin/env python3
"""Check PPTX shape bounds, overlap, reading order, and final font size."""

from __future__ import annotations

import argparse
import math
import sys
from typing import Any

from _common import CliError, emit_json
from _manifest import load_and_validate_manifest
from _pptx import analyze_layout


def _positive_float(value: str) -> float:
    try:
        number = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected a number") from exc
    if not math.isfinite(number) or number <= 0:
        raise argparse.ArgumentTypeError("value must be finite and greater than zero")
    return number


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Inspect direct PPTX shape bounding boxes for overlap and out-of-bounds "
            "placement, list package reading order, and screen explicit font sizes "
            "at final print scale. No rendering or network access occurs."
        )
    )
    parser.add_argument("pptx", help="local macro-free .pptx file")
    source = parser.add_mutually_exclusive_group()
    source.add_argument(
        "--manifest",
        help="approved poster manifest supplying print scale and font requirement",
    )
    source.add_argument(
        "--print-scale",
        type=_positive_float,
        default=None,
        help="physical-artboard/canvas scale when no manifest is supplied",
    )
    parser.add_argument(
        "--minimum-font-pt-final",
        type=_positive_float,
        help=(
            "final-output font threshold; default is manifest value or an explicit "
            "18 pt project heuristic"
        ),
    )
    parser.add_argument("--output", help="optional new JSON report path")
    return parser


def _manifest_settings(path: str) -> tuple[float, float, dict[str, Any]]:
    _, document, validation = load_and_validate_manifest(
        path,
        verify_assets=False,
        require_approval=True,
    )
    scale = float(validation["physical_output"]["print_scale"])
    minimum = float(document["quality"]["minimum_font_pt_final"])
    basis = {
        "kind": document["quality"]["font_guidance_basis"],
        "source_id": document["quality"]["font_guidance_source_id"],
    }
    return scale, minimum, {
        "document": document,
        "validation": validation,
        "font_basis": basis,
    }


def apply_manifest_checks(
    report: dict[str, Any],
    document: dict[str, Any],
    validation: dict[str, Any],
) -> None:
    """Append approved-canvas and direct reading-order mismatches to a report."""
    expected = validation["canvas"]
    actual = report["slide_size"]
    if (
        abs(float(expected["width_in"]) - float(actual["width_in"])) > 0.001
        or abs(float(expected["height_in"]) - float(actual["height_in"])) > 0.001
    ):
        report["issues"].append(
            {
                "code": "CANVAS_MISMATCH",
                "message": "PPTX slide dimensions do not match the approved manifest",
                "expected": expected,
                "actual": actual,
            }
        )
    expected_order = [
        {
            "order": int(element["reading_order"]),
            "name": (
                f"R{int(element['reading_order']):03d}_"
                f"{'TEXT' if element['type'] == 'text' else 'IMAGE'}_"
                f"{element['id']}"
            ),
        }
        for element in document["elements"]
    ]
    actual_order = (
        report["slides"][0]["reading_order"] if report["slides"] else []
    )
    if actual_order != expected_order:
        report["issues"].append(
            {
                "code": "READING_ORDER_MISMATCH",
                "message": (
                    "direct PPTX shape order/names do not match the approved manifest"
                ),
                "expected": expected_order,
                "actual": actual_order,
            }
        )


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
        manifest_context: dict[str, Any] | None = None
        if args.manifest:
            print_scale, manifest_minimum, manifest_context = _manifest_settings(
                args.manifest
            )
            minimum_font = (
                args.minimum_font_pt_final
                if args.minimum_font_pt_final is not None
                else manifest_minimum
            )
        else:
            print_scale = args.print_scale if args.print_scale is not None else 1.0
            minimum_font = (
                args.minimum_font_pt_final
                if args.minimum_font_pt_final is not None
                else 18.0
            )
        report = analyze_layout(
            args.pptx,
            print_scale=print_scale,
            minimum_font_pt_final=minimum_font,
        )
        if manifest_context is not None:
            validation = manifest_context["validation"]
            apply_manifest_checks(
                report,
                manifest_context["document"],
                validation,
            )
            report["manifest"] = {
                "path": validation["manifest_path"],
                "content_sha256": validation["content_sha256"],
            }
            report["minimum_font_basis"] = manifest_context["font_basis"]
        else:
            report["minimum_font_basis"] = {
                "kind": (
                    "caller_supplied"
                    if args.minimum_font_pt_final is not None
                    else "project_heuristic"
                ),
                "source_id": None,
            }
        report["pass"] = not report["issues"]
        emit_json(report, output=args.output)
        return 0 if report["pass"] else 1
    except CliError as exc:
        parser.exit(2, f"error: {exc}\n")


if __name__ == "__main__":
    sys.exit(main())
