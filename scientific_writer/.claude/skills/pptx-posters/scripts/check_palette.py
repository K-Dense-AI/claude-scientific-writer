#!/usr/bin/env python3
"""Report declared WCAG contrast and heuristic palette separation."""

from __future__ import annotations

import argparse
import itertools
import sys
from typing import Any

from _common import CliError, contrast_ratio, emit_json, parse_hex_color, relative_luminance
from _manifest import load_and_validate_manifest

THRESHOLDS = {"normal_text": 4.5, "large_text": 3.0, "non_text": 3.0}


def _lstar(color: str) -> float:
    luminance = relative_luminance(color)
    delta = 6.0 / 29.0
    transformed = (
        luminance ** (1.0 / 3.0)
        if luminance > delta**3
        else luminance / (3.0 * delta**2) + 4.0 / 29.0
    )
    return 116.0 * transformed - 16.0


def audit_palette(document: dict[str, Any]) -> dict[str, Any]:
    palette = document["palette"]
    colors = {
        color_id: parse_hex_color(value, context=f"palette.colors.{color_id}")
        for color_id, value in palette["colors"].items()
    }
    declared: list[dict[str, Any]] = []
    issues: list[dict[str, Any]] = []
    for pair in palette["contrast_pairs"]:
        foreground = colors[pair["foreground_color_id"]]
        background = colors[pair["background_color_id"]]
        ratio = contrast_ratio(foreground, background)
        threshold = THRESHOLDS[pair["usage"]]
        passed = ratio + 1e-9 >= threshold
        declared.append(
            {
                "id": pair["id"],
                "foreground_color_id": pair["foreground_color_id"],
                "foreground": foreground,
                "background_color_id": pair["background_color_id"],
                "background": background,
                "usage": pair["usage"],
                "ratio": round(ratio, 3),
                "threshold": threshold,
                "pass": passed,
            }
        )
        if not passed:
            issues.append(
                {
                    "code": "DECLARED_CONTRAST_FAILURE",
                    "pair_id": pair["id"],
                    "message": (
                        f"{ratio:.2f}:1 is below {threshold:.1f}:1 for "
                        f"{pair['usage']}"
                    ),
                }
            )

    pairwise: list[dict[str, Any]] = []
    for first_id, second_id in itertools.combinations(colors, 2):
        first = colors[first_id]
        second = colors[second_id]
        pairwise.append(
            {
                "first_color_id": first_id,
                "second_color_id": second_id,
                "contrast_ratio": round(contrast_ratio(first, second), 3),
                "grayscale_delta_lstar": round(abs(_lstar(first) - _lstar(second)), 3),
            }
        )
    return {
        "schema_version": "1.0",
        "pass": not issues,
        "declared_contrast_pairs": declared,
        "pairwise_screen": pairwise,
        "redundant_encoding_confirmed": palette[
            "data_series_redundant_encoding"
        ],
        "issues": issues,
        "standards_basis": {
            "normal_text": "WCAG 2.2 SC 1.4.3, 4.5:1",
            "large_text": (
                "WCAG 2.2 SC 1.4.3, 3:1; large text is at least 18 pt, "
                "or 14 pt and bold"
            ),
            "non_text": (
                "WCAG 2.2 SC 1.4.11, 3:1 for graphical parts required "
                "to understand content"
            ),
        },
        "pairwise_notice": (
            "Pairwise contrast and CIE L* separation are screening data, not a "
            "color-vision accessibility certification. Keep direct labels and "
            "redundant shape, marker, pattern, or line-style encoding."
        ),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Audit an approved poster manifest's declared sRGB foreground/background "
            "pairs against WCAG 2.2 and report heuristic pairwise separation. "
            "No network is used."
        )
    )
    parser.add_argument("manifest", help="approved local poster manifest JSON")
    parser.add_argument("--output", help="optional new JSON report path")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
        _, document, validation = load_and_validate_manifest(
            args.manifest,
            verify_assets=False,
            require_approval=True,
            enforce_contrast=False,
        )
        report = audit_palette(document)
        report["manifest"] = {
            "path": validation["manifest_path"],
            "content_sha256": validation["content_sha256"],
        }
        emit_json(report, output=args.output)
        return 0 if report["pass"] else 1
    except CliError as exc:
        parser.exit(2, f"error: {exc}\n")


if __name__ == "__main__":
    sys.exit(main())
