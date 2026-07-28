# Safety and Scope

## Intended Use

Use this skill only to create or check research, evaluation, documentation, and governance artifacts from synthetic or aggregate data.

Acceptable examples:

- an intended-use statement for a retrospective model evaluation;
- an aggregate subgroup performance report;
- a statistical analysis plan;
- a GRADE evidence-profile shell for a human panel;
- a release-gate traceability matrix;
- a de-identification process checklist.

## Prohibited Use

Do not:

- accept or produce a record about a person;
- infer a diagnosis, prognosis, phenotype, biomarker class, or eligibility for a person;
- recommend or compare care options for a person;
- provide medication, dose, schedule, monitoring, or contraindication instructions;
- triage, assign urgency, create an alarm, or suggest escalation;
- deploy logic in an EHR, bedside tool, portal, order set, or alerting workflow;
- represent output as clinical advice, a validated medical device, or an authorized clinical system;
- claim legal, regulatory, quality-system, or HIPAA compliance.

No disclaimer makes an otherwise prohibited workflow acceptable.

## Stop Conditions

Stop and do not process the input when any of the following is present:

- names, record numbers, contact details, precise locations, or person-linked dates;
- row-level records, timelines, notes, images, signals, or sequences;
- a request about “this patient,” “this result,” or an individual case;
- instructions to choose a therapy, test, dose, disposition, or urgency;
- instructions to push output to a live clinical system;
- an assertion that passing a checklist proves authorization or compliance.

Explain the boundary briefly. For care, direct the requester to a licensed healthcare professional and locally validated, appropriately authorized systems. For privacy, regulatory, or legal determinations, direct them to qualified organizational reviewers.

## Required Intended-Use Elements

An artifact is incomplete unless it states:

1. **Purpose** — the specific research or governance question.
2. **Users** — named roles, not “clinicians” broadly.
3. **Population scope** — aggregate cohort or synthetic data only.
4. **Decision role** — descriptive, evaluative, or governance support.
5. **Excluded uses** — every prohibited use above.
6. **Data level** — aggregate or synthetic, with no PHI/raw rows supplied.
7. **Limitations** — known gaps, assumptions, transportability, and failure modes.
8. **Human review** — required roles and approval status.
9. **Versioning** — owner, version, release date, changes, and retirement criteria.
10. **Monitoring** — drift, calibration, subgroup performance, incidents, and review cadence when applicable.

## Human Review Matrix

| Artifact | Minimum review roles |
|---|---|
| Evidence profile | systematic-review methodologist; domain experts; panel chair |
| Cohort report | statistician/epidemiologist; data steward; domain expert |
| Survival plan | statistician with time-to-event expertise; domain expert |
| Model/biomarker evaluation | prediction-model methodologist; assay/domain expert; fairness reviewer |
| Privacy checklist | privacy official or qualified de-identification expert |
| Logic traceability | system owner; independent validator; governance approver |
| Regulatory context | qualified legal/regulatory counsel |

Review completion must be recorded by the responsible organization. The scripts do not authenticate reviewers or approvals.

## Safe Language

Prefer:

- “The aggregate evaluation estimated…”
- “Performance differed across evaluated subgroups; causes and practical importance require review.”
- “The evidence panel judged certainty as…; rationale and sources are recorded.”
- “This checklist is complete; it is not a compliance determination.”
- “External validation has not been performed.”

Avoid:

- “The model is safe/fair/clinically valid.”
- “This biomarker means the patient should…”
- “The tool is FDA compliant/approved.”
- “The dataset is HIPAA compliant.”
- “The recommendation is Grade 1A” without the framework, panel process, outcome-specific judgments, and source trail.

## Audit Trail

Record:

- immutable artifact ID and version;
- source versions and access dates;
- data provenance and cut date;
- code version and command;
- declared thresholds before analysis;
- reviewer roles, dates, decisions, and unresolved objections;
- change reason, validation evidence, rollback plan, and retirement decision.

Do not put secrets, credentials, or patient information in audit logs.
