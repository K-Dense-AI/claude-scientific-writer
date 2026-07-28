# Study Reporting and Appraisal

Checked 2026-07-23.

## First Principle

Choose by study purpose, design, and evaluation stage. A reporting guideline states what to report; it does not prove that the study was well designed, unbiased, clinically useful, safe, or effective.

Use risk-of-bias/applicability tools separately and preserve human judgments.

## Selection Map

| Study or artifact | Primary framework | Important companion |
|---|---|---|
| Observational cohort/case-control/cross-sectional | STROBE | RECORD for routinely collected data |
| Prediction model development or evaluation | TRIPOD+AI | PROBAST+AI |
| Tumor prognostic marker | REMARK | Appropriate risk-of-bias and assay guidance |
| Diagnostic accuracy | STARD | STARD-AI when the index test uses AI |
| Randomized AI intervention protocol | Current SPIRIT base | SPIRIT-AI extension |
| Randomized AI intervention report | Current CONSORT base | CONSORT-AI extension |
| Early-stage live AI support evaluation | DECIDE-AI | Design-specific guideline |
| Evidence profile | GRADE | Design-specific risk-of-bias tools |

## Observational Data

### STROBE

STROBE addresses reporting of cohort, case-control, and cross-sectional studies. Use the design-specific checklist and explanation material from the [STROBE site](https://www.strobe-statement.org/).

### RECORD

RECORD extends STROBE for routinely collected health data such as administrative, EHR, primary-care surveillance, and registry data. It emphasizes code lists/algorithms, database linkage, selection, cleaning, and data-access transparency. See the [RECORD site](https://www.record-statement.org/).

Neither framework authorizes this skill to read EHR rows.

## Prediction Models

### TRIPOD+AI

[TRIPOD+AI](https://www.bmj.com/content/385/bmj-2023-078378), published April 16, 2024, updates reporting guidance for development and evaluation of clinical prediction models using regression or machine-learning methods. It primarily targets non-generative models.

Report, at minimum:

- intended use, target population, outcome, horizon, and setting;
- data sources, eligibility, sampling, and preprocessing;
- predictor/outcome definitions and timing;
- missing data;
- sample-size rationale;
- full model specification or access;
- internal-validation method;
- discrimination and calibration with uncertainty;
- external validation and transportability;
- subgroup performance and fairness considerations;
- intended user, presentation, and limitations.

### PROBAST+AI

[PROBAST+AI](https://pubmed.ncbi.nlm.nih.gov/40127903), published March 24, 2025, replaces the original PROBAST for broad prediction-model assessment. It has two distinct parts:

- **model development** — quality and applicability;
- **model evaluation** — risk of bias and applicability.

Both parts use four domains:

1. participants and data sources;
2. predictors;
3. outcome;
4. analysis.

Applicability is assessed for participants/data sources, predictors, and outcome. Do not average signaling questions into a score. Domain and overall judgments require knowledgeable assessors and rationale.

## Biomarker Studies

Use the FDA-NIH [BEST Resource](https://www.ncbi.nlm.nih.gov/books/NBK326791/) for terminology. Distinguish:

- diagnostic;
- monitoring;
- pharmacodynamic/response;
- predictive;
- prognostic;
- safety;
- susceptibility/risk;
- surrogate endpoint biomarkers.

A biomarker is not itself a measure of how a person feels, functions, or survives. Analytical validation, clinical validation, and clinical utility are distinct.

For tumor prognostic markers, use [REMARK](https://www.equator-network.org/reporting-guidelines/reporting-recommendations-for-tumour-marker-prognostic-studies-remark). Report specimen handling, assay methods, prespecified hypotheses/cut points, participant flow, missing data, analysis, effect estimates, and validation.

## AI Diagnostic Accuracy

[STARD-AI](https://www.nature.com/articles/s41591-025-03953-8) was published September 15, 2025. It adds AI-specific or modified items to STARD 2015 for diagnostic-accuracy studies, including:

- dataset practices;
- AI index-test description and evaluation;
- algorithmic bias and fairness;
- applicability and generalizability;
- transparent participant flow and reference-standard handling.

Use STARD-AI with STARD. Do not use it for a prognostic prediction model merely because the model returns a class.

## AI Trial Protocols and Reports

[SPIRIT-AI](https://www.nature.com/articles/s41591-020-1037-7) and [CONSORT-AI](https://www.nature.com/articles/s41591-020-1034-x) were published September 9, 2020.

- Use SPIRIT-AI for protocols evaluating an AI intervention.
- Use CONSORT-AI for reports of randomized trials evaluating an AI intervention.
- Apply them with the current generic [SPIRIT 2025](https://pubmed.ncbi.nlm.nih.gov/40295741) or [CONSORT 2025](https://www.bmj.com/content/389/bmj-2024-081123) statement, respectively.

AI extensions emphasize the intervention version, input acquisition/quality handling, human-AI interaction, integration requirements, errors/failures, and analysis of performance.

## Early Live Evaluation

[DECIDE-AI](https://www.nature.com/articles/s41591-022-01772-9), published May 18, 2022, covers early-stage live clinical evaluation of AI-based decision-support systems and includes human factors, workflow, safety, and iterative change reporting.

Live evaluation affects real care and is outside this skill's execution boundary. Use the guideline only to understand documentation requirements. Such work requires an approved protocol, qualified investigators, safety oversight, validated systems, applicable authorization, and institutional governance.

## Cross-Cutting Reporting

Always disclose:

- prespecified versus exploratory work;
- all evaluated outcomes and analyses, including negative results;
- effect sizes and uncertainty;
- missingness and exclusions;
- conflicts, funding, and developer involvement;
- version and data cut dates;
- external validation;
- subgroup representation and performance;
- calibration and decision thresholds;
- human-factors methods;
- incidents, failures, drift, updates, and monitoring;
- access to protocol, analysis plan, code, model, and data when lawful and feasible.

Never state “reported according to” as proof of adherence without a completed checklist and human verification.
