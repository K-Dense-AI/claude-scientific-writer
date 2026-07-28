#!/usr/bin/env python3
"""Inspect a PPTX ZIP/XML package without opening or executing it."""

from __future__ import annotations

import argparse
import sys

from _common import CliError, emit_json
from _pptx import inspect_pptx


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Boundedly inspect a local .pptx against the strict one-slide generated "
            "poster profile: package parts, macros, relationships, linked images, "
            "OLE/embedded content, ZIP paths/expansion, image signatures, title, "
            "text language, and picture alt text. Nothing is extracted, opened in "
            "PowerPoint, or executed."
        )
    )
    parser.add_argument("pptx", help="local .pptx file")
    parser.add_argument("--output", help="optional new JSON report path")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
        report = inspect_pptx(args.pptx)
        emit_json(report, output=args.output)
        return 0 if report["safe"] else 1
    except CliError as exc:
        parser.exit(2, f"error: {exc}\n")


if __name__ == "__main__":
    sys.exit(main())
