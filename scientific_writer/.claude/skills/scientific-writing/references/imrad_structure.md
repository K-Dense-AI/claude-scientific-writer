# Manuscript Structure and Consistency

IMRAD is a useful default for many original-research reports, but the study design,
reporting guideline, article type, and current journal instructions control the final
structure [SW-S01, SW-S06].

## Title and abstract

The title should identify the work accurately without adding novelty, causality, design,
or population claims that the manuscript does not support.

Draft the abstract after the main text. Mirror, do not reinterpret:

- objective or question;
- design, setting, population or material, and key methods;
- analysis population and prespecified primary result;
- estimate, uncertainty, denominator, and harms where relevant;
- conclusion limited to the reported evidence.

Structured versus unstructured format is a venue decision. Do not apply a universal
format. Any number in the abstract must match the same concept and analysis set in the
main text and consistency registry.

## Introduction

Build a short evidence chain:

1. verified context;
2. what is known and uncertain;
3. the specific gap;
4. the objective, question, or prespecified hypothesis.

Do not claim that no prior work exists unless a suitable search verifies that claim.
Avoid previewing unsupported results or inflating significance.

## Methods

Methods should permit evaluation and, where feasible, reproduction. Cover the elements
applicable to the design:

- design, setting, dates, and protocol or registration;
- participants, specimens, datasets, or source population;
- eligibility, selection, sampling, exclusions, and analysis populations;
- interventions, exposures, comparators, materials, instruments, and versions;
- outcomes, predictors, thresholds, time points, and measurement methods;
- bias controls, randomization, allocation, and masking where applicable;
- sample-size rationale;
- missing data, transformations, covariates, multiplicity, sensitivity analyses, and
  statistical or computational methods;
- confirmatory, exploratory, and descriptive status;
- ethics, consent, privacy, data governance, and approvals only when verified;
- data, code, materials, and protocol access conditions.

Record deviations and timing. Never reconstruct a method from a result merely to make
the paper appear consistent.

## Results

Follow the declared objectives and outcomes. Report:

- participant, sample, or record flow;
- exclusions, missingness, attrition, and analysis populations;
- descriptive information needed for interpretation;
- prespecified primary and secondary results;
- estimates with units, denominators, sample sizes, and uncertainty;
- exploratory, sensitivity, subgroup, negative, null, adverse, unexpected, and
  inconclusive findings with correct labels;
- protocol or analysis deviations that affect interpretation.

Describe results before interpretation unless the venue combines Results and
Discussion. Do not equate a threshold crossing with scientific or practical importance.

## Discussion

Start from the verified findings, then:

- answer the objective at the supported level of certainty;
- compare with verified prior evidence;
- consider alternative explanations;
- distinguish statistical, scientific, clinical, and practical interpretation;
- explain limitations and likely consequences;
- bound generalizability to the studied population, material, setting, and period;
- identify implications without prescribing action beyond the evidence.

Do not introduce new results, methods, approvals, or citations that bypass verification.

## Declarations and end matter

Treat each statement as data, not boilerplate:

- author contributions and accountability;
- acknowledgments and permissions;
- funding and the funder's role;
- competing interests;
- ethics, consent, and registration;
- data, code, materials, and protocol availability;
- AI-use disclosure;
- references, figure legends, tables, and supplements.

Use verified or explicit not-applicable states. Never generate an approval identifier,
grant number, registration, author role, conflict declaration, or availability promise.

## Cross-section audit

Before submission, compare:

- objective ↔ outcome ↔ result ↔ conclusion;
- methods ↔ results;
- abstract ↔ main text ↔ tables ↔ figures ↔ supplement;
- units, denominators, sample sizes, labels, and time points;
- registration and protocol ↔ manuscript;
- in-text citations ↔ source manifest ↔ reference list.

Run `scripts/check_consistency.py` and complete a manual scientific review.
