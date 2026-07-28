"""Select reporting guidance and check non-scoring coverage metadata."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from _common import (
    InputError,
    Issue,
    emit_report,
    is_nonempty_string,
    issue,
    read_json,
    require_list,
    require_object,
    run,
)

TOOL = "select_reporting_guidelines"
REGISTRY_PATH = (
    Path(__file__).resolve().parents[1] / "assets" / "reporting_guidelines.json"
)
DISCLAIMER = (
    "Selection and coverage are non-scoring aids. They do not reproduce an official "
    "checklist, appraise study quality, certify compliance, or replace the current "
    "guideline and target-journal instructions."
)


def load_registry() -> dict[str, dict[str, Any]]:
    root = require_object(read_json(REGISTRY_PATH), "registry")
    if root.get("schema_version") != "1.0":
        raise InputError("unsupported reporting-guideline registry version")
    raw_items = require_list(root.get("guidelines"), "guidelines")
    registry: dict[str, dict[str, Any]] = {}
    for raw_item in raw_items:
        item = require_object(raw_item, "guideline")
        guideline_id = item.get("id")
        if not is_nonempty_string(guideline_id) or guideline_id in registry:
            raise InputError("registry guideline IDs must be non-empty and unique")
        registry[guideline_id] = item
    return registry


def _condition_matches(item: dict[str, Any], args: argparse.Namespace) -> bool:
    conditions = require_object(item.get("conditions", {}), "conditions")
    for flag in ("ai", "llm", "routinely_collected", "qualitative_component"):
        required = conditions.get(flag)
        if required is True and not getattr(args, flag):
            return False
    return True


def select_guidelines(
    registry: dict[str, dict[str, Any]],
    args: argparse.Namespace,
) -> tuple[list[str], list[str], list[Issue]]:
    primary: list[str] = []
    extensions: list[str] = []
    issues: list[Issue] = []
    for guideline_id, item in registry.items():
        designs = require_list(
            item.get("study_designs"), f"{guideline_id}.study_designs"
        )
        if args.study_design not in designs:
            continue
        if bool(item.get("protocol")) != bool(args.protocol):
            continue
        if not _condition_matches(item, args):
            continue
        if item.get("role") == "primary":
            primary.append(guideline_id)
        elif item.get("role") == "extension":
            extensions.append(guideline_id)

    if not primary:
        issues.append(
            issue("warning", "NO_PRIMARY_LOCAL_MATCH", item_id=args.study_design)
        )
    if args.llm and not args.ai:
        issues.append(issue("error", "LLM_REQUIRES_AI_FLAG", location="arguments"))
    return sorted(primary), sorted(extensions), issues


def check_coverage(
    registry: dict[str, dict[str, Any]],
    coverage_path: str,
) -> tuple[list[Issue], dict[str, Any]]:
    data = require_object(read_json(coverage_path), "coverage")
    if data.get("schema_version") != "1.0":
        raise InputError("unsupported reporting-coverage schema version")
    guideline_id = data.get("guideline_id")
    if guideline_id not in registry:
        raise InputError("coverage guideline_id is not in the bundled registry")
    guideline = registry[guideline_id]
    expected = {
        item["id"]: item
        for item in (
            require_object(raw, "coverage_topic")
            for raw in require_list(guideline.get("coverage_topics"), "coverage_topics")
        )
    }

    issues: list[Issue] = []
    observed: dict[str, dict[str, Any]] = {}
    for index, raw_item in enumerate(require_list(data.get("items"), "items")):
        item = require_object(raw_item, f"items[{index}]")
        topic_id = item.get("topic_id")
        if topic_id not in expected:
            issues.append(
                issue("error", "UNKNOWN_COVERAGE_TOPIC", location=f"items[{index}]")
            )
            continue
        if topic_id in observed:
            issues.append(
                issue("error", "DUPLICATE_COVERAGE_TOPIC", item_id=str(topic_id))
            )
            continue
        observed[str(topic_id)] = item
        status = item.get("status")
        if status not in {"addressed", "not_applicable", "missing"}:
            issues.append(
                issue("error", "INVALID_COVERAGE_STATUS", item_id=str(topic_id))
            )
        if status == "addressed":
            locations = item.get("locations")
            if (
                not isinstance(locations, list)
                or not locations
                or not all(is_nonempty_string(value) for value in locations)
            ):
                issues.append(
                    issue(
                        "error",
                        "ADDRESSED_TOPIC_WITHOUT_LOCATION",
                        item_id=str(topic_id),
                    )
                )
        if status == "not_applicable" and not is_nonempty_string(item.get("rationale")):
            issues.append(
                issue(
                    "error", "NOT_APPLICABLE_WITHOUT_RATIONALE", item_id=str(topic_id)
                )
            )
        if status == "missing":
            issues.append(
                issue("error", "COVERAGE_TOPIC_MISSING", item_id=str(topic_id))
            )

    for topic_id in sorted(set(expected) - set(observed)):
        issues.append(issue("error", "COVERAGE_TOPIC_NOT_RECORDED", item_id=topic_id))

    summary = {
        "guideline_id": guideline_id,
        "topics_expected": len(expected),
        "topics_recorded": len(observed),
        "coverage_status": (
            "incomplete"
            if any(item.severity == "error" for item in issues)
            else "all_bundled_topics_addressed"
        ),
        "disclaimer": DISCLAIMER,
    }
    return issues, summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Use the bundled offline registry to select candidate reporting guidance "
            "or validate a non-scoring coverage record."
        )
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    select_parser = subparsers.add_parser(
        "select",
        help="select candidate guidelines from study metadata",
    )
    select_parser.add_argument("--study-design", required=True)
    select_parser.add_argument("--protocol", action="store_true")
    select_parser.add_argument("--ai", action="store_true")
    select_parser.add_argument("--llm", action="store_true")
    select_parser.add_argument("--routinely-collected", action="store_true")
    select_parser.add_argument("--qualitative-component", action="store_true")

    check_parser = subparsers.add_parser(
        "check",
        help="validate high-level coverage metadata",
    )
    check_parser.add_argument("coverage", help="UTF-8 JSON coverage record")
    return parser


def cli() -> int:
    args = build_parser().parse_args()
    registry = load_registry()
    if args.command == "select":
        primary, extensions, issues = select_guidelines(registry, args)
        summary = {
            "study_design": args.study_design,
            "primary": primary,
            "extensions": extensions,
            "disclaimer": DISCLAIMER,
        }
    else:
        issues, summary = check_coverage(registry, args.coverage)
    return emit_report(TOOL, issues, summary=summary)


if __name__ == "__main__":
    run(TOOL, cli)
