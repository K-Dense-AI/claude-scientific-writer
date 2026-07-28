# Reporting-Guideline Selection and Coverage

## Purpose and limits

Reporting guidelines help authors report study design, conduct, analysis, and findings
completely enough for appraisal. They do not make a study rigorous, replace a protocol,
repair missing methods, appraise risk of bias, certify compliance, or predict acceptance.
The bundled selector and coverage checker are deliberately non-scoring [SW-S06, SW-S12].

Always open the current official statement, checklist, explanation-and-elaboration
document, relevant extensions, and target-journal instructions. The bundled registry is
a dated routing aid, not a copy of any official checklist.

## Current major guidance as researched

- **Randomized-trial results:** CONSORT 2025. The joint official site provides the
  statement, checklist, expanded checklist, flow diagram, and explanation and
  elaboration [SW-S07, SW-S08].
- **Randomized-trial protocols:** SPIRIT 2025 and its participant-timeline resources
  [SW-S07, SW-S09].
- **Systematic reviews and meta-analyses:** PRISMA 2020. Choose relevant extensions,
  such as protocol, scoping-review, search, or diagnostic-accuracy guidance, from the
  official PRISMA and EQUATOR sites [SW-S10, SW-S06].
- **Cohort, case-control, and cross-sectional studies:** STROBE and the applicable
  design-specific checklist [SW-S11].
- **Diagnostic-accuracy studies:** STARD 2015; add STARD-AI for an AI-centered
  diagnostic-accuracy study [SW-S12, SW-S13].
- **Clinical prediction models:** TRIPOD+AI 2024 covers regression and machine-learning
  prediction-model studies and replaces TRIPOD 2015; add TRIPOD-LLM for biomedical or
  healthcare LLM studies within its scope [SW-S14].
- **Case reports:** CARE 2013, including consent-sensitive reporting [SW-S15].
- **In vivo animal research:** ARRIVE 2.0, using both the Essential 10 and Recommended
  Set as appropriate [SW-S16].
- **Healthcare quality improvement:** SQUIRE 2.0 [SW-S17].
- **Health economic evaluations:** CHEERS 2022 [SW-S18].
- **Qualitative research:** use SRQR generally and verify whether COREQ or another
  design-specific guideline is more appropriate through EQUATOR [SW-S06].

For AI intervention trials or protocols, check CONSORT-AI or SPIRIT-AI in addition to
the current parent statement. For routinely collected data, harms, equity, patient-
reported outcomes, clusters, noninferiority, pilot studies, and other special designs,
search EQUATOR for a current extension [SW-S06].

## Selector

Use the offline registry:

```bash
python3 scripts/select_reporting_guidelines.py select --study-design randomized_trial
python3 scripts/select_reporting_guidelines.py select --study-design randomized_trial --protocol
python3 scripts/select_reporting_guidelines.py select --study-design diagnostic_accuracy --ai
python3 scripts/select_reporting_guidelines.py select --study-design prediction_model --ai --llm
```

The result is a candidate set. A human must confirm:

- the actual design and article type;
- whether a protocol or results report is being written;
- every relevant extension;
- current version and corrections;
- target-journal requirements.

If no local match exists, search the official EQUATOR library rather than forcing the
nearest guideline.

## Coverage record

The bundled `coverage_topics` are original high-level prompts. They do not reproduce
official item wording or numbering.

For each topic, record:

- `addressed`, with manuscript locations;
- `not_applicable`, with a rationale;
- `missing`.

Then run:

```bash
python3 scripts/select_reporting_guidelines.py check reporting_coverage.json
```

A pass means every bundled topic has an allowed status and location or rationale. It
does not mean every official checklist item is satisfied or well reported.

## Workflow

1. Select candidate guidance during planning.
2. Open the official statement and explanation document.
3. Record prospective items in the protocol, registry, or analysis plan where
   applicable.
4. Draft the manuscript from evidence and methods records.
5. Complete the official checklist with actual manuscript locations.
6. Record missing items honestly; do not invent information to fill them.
7. Submit the official checklist or flow diagram if the journal requires it.
8. Re-check guideline and journal versions immediately before submission.

## Frequent errors

- treating a checklist as a design-quality score;
- claiming adherence when only a subset was reviewed;
- using an outdated parent statement while overlooking a current update;
- omitting a relevant extension;
- writing a missing method into the paper as though it occurred;
- checking boxes without recording manuscript locations;
- assuming a journal endorsement means submission requirements are identical across
  article types.
