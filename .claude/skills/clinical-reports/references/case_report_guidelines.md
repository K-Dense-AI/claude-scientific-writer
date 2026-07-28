# CARE Case-Report Drafting

## Current source

The official CARE site continues to identify the **2013 CARE Checklist** as the core checklist. The 2017 explanation and elaboration supplies rationale and examples. CARE is reporting guidance for case reports; it does not authorize record access, establish consent, prove de-identification, or replace journal instructions.

## Thirteen checklist headings

Preserve the official structure:

1. title;
2. key words;
3. abstract;
4. introduction;
5. patient information;
6. clinical findings;
7. timeline;
8. diagnostic assessment;
9. therapeutic intervention;
10. follow-up and outcomes;
11. discussion;
12. patient perspective;
13. informed consent.

Use the official checklist and explanation for subitems. The local validator checks only that all headings have an allowed status and verified fact references; it does not judge clinical accuracy or CARE adherence.

## Safe use

- Begin with `assets/case_report_template.json`.
- Use de-identified source facts, not copied charts or free-text records.
- Keep direct identifiers and contact details out of the draft manifest.
- Represent chronology with relative study/case offsets when authorized and scientifically adequate; do not alter chronology to disguise conflicts.
- Preserve diagnostic and therapeutic statements as attributed facts from authorized records. Do not independently diagnose, rationalize treatment, or recommend care.
- Attribute the patient perspective to an authorized source; never invent a quote.
- Keep uncertainty, missing follow-up, adverse outcomes, and limitations visible.
- Do not claim novelty until an accountable author has reviewed the literature.
- Avoid causal or general treatment claims from a single case.

## Consent and privacy

CARE includes informed consent as an item, but a template cannot obtain or verify consent.

- Record only a consent status verified by the responsible human reviewer.
- Do not create a stock statement asserting that consent was obtained.
- Consent for publication and HIPAA de-identification are separate questions.
- De-identification does not necessarily remove all re-identification risk, particularly for rare conditions, small communities, images, unusual timelines, or distinctive combinations.
- Journal, institution, law, ethics-board policy, and circumstances involving minors, deceased persons, or persons unable to consent require qualified review.

## Fail-closed statuses

Each CARE item uses one of:

- `verified_present` — supported by one or more verified source-fact IDs;
- `not_applicable_with_rationale` — a qualified reviewer supplied a recorded rationale;
- `missing` — blocks structural readiness;
- `conflict` — source records disagree and human resolution is required.

The consent item cannot be waived by the script. A missing or unresolved consent status blocks publication handoff.

## Qualified review

Before any journal handoff, accountable authors and the appropriate clinical, privacy/legal, and institutional reviewers must verify:

- source accuracy and chronology;
- consent and authorization;
- privacy and image/metadata handling;
- terminology and clinical interpretation;
- discussion claims and citations;
- conflicts, limitations, and adverse outcomes;
- the target journal’s current instructions.

A structural result of `STRUCTURE_COMPLETE_REVIEW_REQUIRED` is not permission to submit.
