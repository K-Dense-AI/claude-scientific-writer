"""Minimal, executable examples for the Scientific Writer async API."""

from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path
from typing import Any, Literal

from scientific_writer import generate_paper


async def generate_document(
    prompt: str,
    *,
    output_dir: str | None = None,
    data_files: list[str] | None = None,
    effort: Literal["low", "medium", "high"] = "medium",
    max_budget_usd: float | None = None,
) -> dict[str, Any]:
    """Generate one document and return its final result event."""
    result: dict[str, Any] | None = None
    async for event in generate_paper(
        query=prompt,
        output_dir=output_dir,
        data_files=data_files,
        effort_level=effort,
        max_budget_usd=max_budget_usd,
        track_token_usage=True,
    ):
        event_type = event["type"]
        if event_type == "text":
            print(event["content"], end="", flush=True)
        elif event_type == "progress":
            print(f"\n[{event['stage']}] {event['message']}", flush=True)
        elif event_type == "result":
            result = event

    if result is None:
        raise RuntimeError("Scientific Writer returned no result event")
    return result


async def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prompt", help="document-generation request")
    parser.add_argument("--output-dir")
    parser.add_argument("--data-file", action="append", default=[])
    parser.add_argument("--effort", choices=["low", "medium", "high"], default="medium")
    parser.add_argument("--max-budget-usd", type=float)
    parser.add_argument("--save-result", type=Path)
    args = parser.parse_args()

    result = await generate_document(
        args.prompt,
        output_dir=args.output_dir,
        data_files=args.data_file or None,
        effort=args.effort,
        max_budget_usd=args.max_budget_usd,
    )

    print(f"\nStatus: {result['status']}")
    print(f"Project: {result['paper_directory']}")
    print(f"Final artifacts: {len(result['files']['final_artifacts'])}")
    if result.get("token_usage"):
        print(f"Tokens: {result['token_usage']['total_tokens']:,}")

    if args.save_result:
        args.save_result.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    asyncio.run(main())
