#!/usr/bin/env python3
"""Validate a fail-closed, author-approved local poster manifest."""

from __future__ import annotations

import argparse
import sys

from _common import CliError, emit_json
from _manifest import load_and_validate_manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Validate strict poster JSON, exact source IDs, local asset hashes, "
            "layout bounds, output requirements, and approval binding. No network "
            "is used."
        )
    )
    parser.add_argument("manifest", help="local poster manifest JSON")
    parser.add_argument(
        "--structure-only",
        action="store_true",
        help="validate asset paths syntactically without reading or hashing assets",
    )
    parser.add_argument(
        "--print-content-hash",
        action="store_true",
        help=(
            "allow draft approval and report the hash an author must approve; "
            "all other validation still runs"
        ),
    )
    parser.add_argument("--output", help="optional new JSON report path")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
        _, _, report = load_and_validate_manifest(
            args.manifest,
            verify_assets=not args.structure_only,
            require_approval=not args.print_content_hash,
        )
        emit_json(report, output=args.output)
        return 0
    except CliError as exc:
        parser.exit(2, f"error: {exc}\n")


if __name__ == "__main__":
    sys.exit(main())
