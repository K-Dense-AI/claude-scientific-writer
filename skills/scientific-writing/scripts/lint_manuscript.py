"""Lint manuscript Markdown for placeholders, language risks, and sensitive content."""

from __future__ import annotations

import argparse
import re
from typing import Any

from _common import (
    Issue,
    emit_report,
    issue,
    read_json,
    read_text,
    require_object,
    run,
)

TOOL = "lint_manuscript"
PLACEHOLDER_PATTERNS = (
    re.compile(r"\[\[\s*TODO\b", re.IGNORECASE),
    re.compile(r"\b(?:TODO|TBD|TK)\b", re.IGNORECASE),
    re.compile(r"\[\s*(?:insert|add|describe|replace)[^\]]*\]", re.IGNORECASE),
    re.compile(r"\blorem ipsum\b", re.IGNORECASE),
    re.compile(r"\bX{4,}\b"),
)
SENSITIVE_PATTERNS = (
    re.compile(r"\b(?:MRN|medical record number)\s*[:#]", re.IGNORECASE),
    re.compile(r"\b(?:SSN|social security number)\s*[:#]", re.IGNORECASE),
    re.compile(r"\b(?:DOB|date of birth)\s*[:#]", re.IGNORECASE),
    re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE),
    re.compile(
        r"\b(?:PHI|protected health information|patient name|participant name)\b",
        re.IGNORECASE,
    ),
    re.compile(r"\b(?:confidential|proprietary|trade secret)\b", re.IGNORECASE),
    re.compile(
        r"\b(?:peer[- ]review material|unpublished manuscript)\b", re.IGNORECASE
    ),
)
DECLARATION_RE = re.compile(
    r"\b(?:ethics (?:approval|committee)|IRB|informed consent|funded by|"
    r"conflict[s]? of interest|data (?:are|is) available|code (?:is|are) available)\b",
    re.IGNORECASE,
)
OVERSTATEMENT_RE = re.compile(
    r"\b(?:proves?|definitively|guarantees?|no limitations|universally|"
    r"highly significant|no effect)\b",
    re.IGNORECASE,
)
CAUSAL_RE = re.compile(
    r"\b(?:causes?|caused|proves?|demonstrates? that)\b", re.IGNORECASE
)
CLAIM_MARKER_RE = re.compile(r"\[claim:C[0-9]{3,8}\]")
EVIDENCE_MARKER_RE = re.compile(r"(?:\[evidence:E[0-9]|\[@E[0-9])")
OBSERVATIONAL_DESIGNS = {
    "observational",
    "cohort",
    "case_control",
    "cross_sectional",
    "routinely_collected_health_data",
}


def load_manifest(path: str | None) -> tuple[dict[str, Any] | None, list[Issue]]:
    if path is None:
        return None, [
            issue(
                "warning",
                "CONFIDENTIALITY_GATE_NOT_CHECKED",
                location="manifest",
            )
        ]
    data = require_object(read_json(path), "manuscript_manifest")
    issues: list[Issue] = []
    review = require_object(
        data.get("confidentiality_review"), "confidentiality_review"
    )
    if review.get("completed") is not True:
        issues.append(
            issue("error", "CONFIDENTIALITY_REVIEW_INCOMPLETE", location="manifest")
        )
    if review.get("policy_checked") is not True:
        issues.append(issue("error", "POLICY_REVIEW_INCOMPLETE", location="manifest"))
    return data, issues


def lint_text(text: str, manifest: dict[str, Any] | None) -> list[Issue]:
    issues: list[Issue] = []
    study_design = str((manifest or {}).get("study_design", "")).casefold()
    submission_ready = (manifest or {}).get("submission_ready") is True
    in_fence = False
    for line_number, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith(("```", "~~~")):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        location = f"line:{line_number}"
        for pattern in PLACEHOLDER_PATTERNS:
            if pattern.search(line):
                issues.append(
                    issue("error", "UNRESOLVED_PLACEHOLDER", location=location)
                )
                break
        for pattern in SENSITIVE_PATTERNS:
            if pattern.search(line):
                issues.append(
                    issue("warning", "POTENTIAL_RESTRICTED_CONTENT", location=location)
                )
                break
        if DECLARATION_RE.search(line) and not (
            CLAIM_MARKER_RE.search(line) and EVIDENCE_MARKER_RE.search(line)
        ):
            issues.append(
                issue(
                    "error", "DECLARATION_WITHOUT_EVIDENCE_MARKERS", location=location
                )
            )
        if OVERSTATEMENT_RE.search(line):
            issues.append(
                issue("warning", "POTENTIAL_OVERSTATEMENT", location=location)
            )
        if study_design in OBSERVATIONAL_DESIGNS and CAUSAL_RE.search(line):
            issues.append(
                issue(
                    "warning",
                    "CAUSAL_LANGUAGE_FOR_OBSERVATIONAL_DESIGN",
                    location=location,
                )
            )
        if submission_ready and "NOT FOR SUBMISSION" in line.upper():
            issues.append(
                issue("error", "DRAFT_BANNER_ON_READY_MANUSCRIPT", location=location)
            )
    if not text.strip():
        issues.append(issue("error", "EMPTY_MANUSCRIPT", location="document"))
    return issues


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Lint local Markdown without echoing source text. Flags unresolved "
            "placeholders, risky declarations, possible sensitive content, and "
            "language that needs human review."
        )
    )
    parser.add_argument("manuscript", help="UTF-8 Markdown manuscript")
    parser.add_argument(
        "--manifest",
        help="optional UTF-8 JSON manuscript manifest with confidentiality gates",
    )
    return parser


def cli() -> int:
    args = build_parser().parse_args()
    manifest, issues = load_manifest(args.manifest)
    text = read_text(args.manuscript, {".md", ".markdown"})
    issues.extend(lint_text(text, manifest))
    return emit_report(
        TOOL,
        issues,
        summary={"lines_checked": len(text.splitlines()), "raw_text_echoed": False},
    )


if __name__ == "__main__":
    run(TOOL, cli)
