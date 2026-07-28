# Privacy, De-identification, and Disclosure

## Boundary

The skill never reads PHI, raw records, free-text notes, images, sequences, or row-level data. The checklist records a human process; it does not de-identify data.

Do not paste sensitive information into a template to see whether it passes.

## HHS Methods

The HIPAA Privacy Rule at 45 CFR 164.514 provides two methods for de-identification:

1. **Expert Determination** — a qualified expert applies generally accepted statistical and scientific principles, determines that re-identification risk is very small, and documents methods and results.
2. **Safe Harbor** — specified identifiers of the individual and relatives, employers, or household members are removed, and the covered entity has no actual knowledge that the remaining information could identify an individual alone or in combination.

Primary sources:

- [HHS de-identification guidance](https://www.hhs.gov/hipaa/for-professionals/special-topics/de-identification/index.html)
- [45 CFR 164.514](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.514)

The checklist cannot determine whether an organization is a covered entity/business associate, whether information is PHI, or whether a method was correctly applied.

## Safe Harbor Categories

The human review must address all categories:

1. names;
2. geographic subdivisions smaller than a state, subject to ZIP-code rules;
3. date elements more specific than year, with the age-90 rule;
4. telephone numbers;
5. fax numbers;
6. email addresses;
7. Social Security numbers;
8. medical record numbers;
9. health-plan beneficiary numbers;
10. account numbers;
11. certificate/license numbers;
12. vehicle identifiers and serial numbers;
13. device identifiers and serial numbers;
14. web URLs;
15. IP addresses;
16. biometric identifiers;
17. full-face photographs and comparable images;
18. other unique identifying numbers, characteristics, or codes.

Parts and derivatives can still be identifiers. HHS specifically notes that free text is not exempt and can contain listed identifiers or identifying context.

## Expert Determination Record

Record without embedding the sensitive data:

- expert qualifications and independence;
- data context and recipients;
- anticipated data linkages and attacker knowledge;
- methods and assumptions;
- risk threshold and rationale;
- mitigation and residual risk;
- validity period and change triggers;
- documentation location and approval.

Do not claim that hashing, pseudonymization, encryption, a data-use agreement, or a low cell count alone constitutes Expert Determination.

## Aggregate Disclosure

Aggregate tables can still disclose information through:

- small cells;
- row/column totals;
- differencing across releases;
- rare combinations;
- nested geographies;
- longitudinal patterns;
- extreme values;
- genomics;
- external linkage.

Controls may include:

- minimum cell thresholds;
- primary suppression;
- complementary suppression;
- category aggregation;
- top/bottom coding;
- rounding or perturbation under an approved method;
- release coordination;
- query budgets;
- access controls and data-use agreements;
- secure enclaves;
- expert review.

There is no universal small-cell threshold that proves HIPAA de-identification. The table generator defaults to 11 only as a conservative operational safeguard and applies complementary suppression within a row. The data steward must select policy.

## Template Status Values

For each category use:

- `not_present` — documented inventory confirms absence;
- `removed` — documented transformation confirms removal;
- `generalized` — allowed generalization documented and approved;
- `expert_reviewed` — addressed under the referenced Expert Determination;
- `unresolved` — not complete.

Every non-unresolved status needs evidence text. Never include an example identifier in evidence.

## Actual-Knowledge and Residual-Risk Review

Document:

- free-text review;
- derived fields;
- linkage and differencing;
- unusual occupations or events;
- rare diseases/combinations;
- dates and ages;
- geography;
- longitudinal uniqueness;
- recipient context;
- prior releases;
- residual identifiers.

Escalate uncertainty. Do not mark the checklist complete merely because all obvious columns were removed.

## Output Language

Allowed:

> Documentation checklist complete for the selected method. This output is not a HIPAA compliance or de-identification determination.

Not allowed:

> HIPAA compliant.

> Safe to publish.

> Anonymous.

## Script

```bash
python3 scripts/deidentification_checklist.py \
  assets/deidentification_checklist_template.json
```

The distributed template is unresolved by design.
