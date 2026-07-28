# Evidence and Provenance Workflow

## Core separation

Drafting and evidence verification are different activities.

- **Drafting** organizes language from already recorded evidence IDs. A draft may remain
  incomplete and uncertain.
- **Verification** requires an accountable human to open the source, confirm the exact
  support and locator, check bibliographic metadata, and record who verified it and
  when.
- A fluent sentence is not evidence. Search snippets, generated summaries, memory, and
  another paper's reference list are discovery aids, not verified support.

## Registries

The scaffold creates five linked records:

1. `source_manifest.json` assigns each source an `E` ID and records identifiers,
   location, confidentiality class, and verification state.
2. `claims.csv` assigns each claim a `C` ID, stores a hash rather than raw claim text,
   and maps the claim to one or more verified `E` IDs.
3. `consistency_manifest.json` binds numeric facts, methods, outcomes, analysis intent,
   units, denominators, sample sizes, and result locations.
4. `authorship.json` records human authorship criteria, CRediT roles, accountability,
   declarations, and AI use.
5. `reporting_coverage.json` records high-level coverage without scoring or certifying
   the manuscript.

These registries contain metadata, not full source documents. Do not paste unpublished
manuscripts, peer-review files, PHI, sensitive datasets, proprietary content, or source
documents into them.

## Claim markers

Append machine-readable markers to every factual or numeric assertion while drafting:

```text
[claim:C001] [evidence:E001,E002]
```

An alternative citation marker is `[@E001]`. Keep the claim and evidence markers on the
same line until the audit passes. A final publisher conversion may replace evidence IDs
with rendered citations only after preserving an auditable mapping.

## Verification procedure

For each source:

1. Open the authoritative source or record.
2. Confirm title, author or organization, publication state, year, and identifiers.
3. Record the exact supporting location, such as section, page, table, figure, or
   registry field.
4. Confirm that the source supports the claim's direction, population, intervention or
   exposure, outcome, time point, and uncertainty.
5. Record caveats, retractions, corrections, expressions of concern, or version status.
6. Mark the source verified only after a named human completes the check.

For each claim:

1. Classify it as factual, numeric, method, result, interpretive, or declaration.
2. Hash the normalized claim text and store the hash in `claims.csv`.
3. Map it to verified evidence IDs.
4. Record uncertainty and whether the analysis was confirmatory, exploratory,
   descriptive, or not applicable.
5. Keep unsupported or conflicting claims out of submission-ready prose. If useful,
   retain them in a clearly marked unresolved-issues log.

## Drafting gates

Do not infer or complete missing:

- citations, identifiers, quotations, or source locators;
- data values, denominators, units, sample sizes, or statistical results;
- methods, protocol details, analysis decisions, or deviations;
- approvals, consent, registrations, author contributions, conflicts, funding, or
  availability statements.

Use explicit missing states. Preserve negative, null, adverse, unexpected, and
inconclusive findings. Never convert absence of evidence into evidence of no effect.

## Final audit

Run:

```bash
python3 scripts/validate_manifest.py source_manifest.json --kind source --require-verified
python3 scripts/audit_claims.py manuscript.md claims.csv source_manifest.json
python3 scripts/check_consistency.py consistency_manifest.json
python3 scripts/check_references.py source_manifest.json
```

Tool output contains IDs and line numbers, not manuscript or source text. A passing
machine audit supports review; it does not replace human scientific judgment.
