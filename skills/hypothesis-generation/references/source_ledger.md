# Dated Source Ledger

Verification and research cutoff: **2026-07-23**.

Machine-readable ledger: `assets/source_ledger.csv`.

## Search boundary

Research used `parallel-cli` search against official or primary domains with focused queries for:

- NIH rigor, reproducibility, and the 2026 replication initiative;
- Cochrane PICO and the original well-built clinical-question article;
- FINER’s attributed historical source and current interpretation;
- Platt’s original strong-inference essay;
- COS/OSF preregistration and Registered Reports;
- SPIRIT 2025 and CONSORT 2025;
- causal questions, counterfactuals, estimands, and bias;
- negative controls, HARKing, multiplicity, reproducibility, and replication;
- NIST/UNESCO responsible AI and primary evidence on output homogenization;
- human, animal, biosafety, biosecurity, dual-use, data, and regulatory gates.

Searches prioritized official domains and primary publications. Full-text extraction or search excerpts were used to verify titles, dates, versions, and relevant passages. This was a targeted skill refresh, not a systematic review, patent search, or proof of scientific novelty.

## Core methodology sources

### Question formulation

- `SRC-COCHRANE-PICO` — current Cochrane Handbook Chapter 2. PICO is used for intervention-effect review questions, with objectives defined in advance and stakeholder input where appropriate.
- `SRC-PICO-ORIGINAL` — Richardson et al., 1995, *The well-built clinical question*. Foundational four-part clinical-question article.
- `SRC-FINER-1988` — Hulley and Cummings, *Designing Clinical Research*, first edition metadata (1988). It is the earliest FINER-attributed source located in this refresh.
- `SRC-FINER-CURRENT` — Werner and Willis, 2023, current FINER interpretation.

**Historical limitation:** the available targeted search confirmed the 1988 book’s bibliographic metadata and later attribution but did not establish the exact first printed use or coinage of the FINER mnemonic. The skill therefore does not claim that provenance as proven.

### Multiple hypotheses and falsification

- `SRC-PLATT-1964` — John R. Platt, “Strong Inference,” *Science* 146:347–353, DOI `10.1126/science.146.3642.347`.
- `SRC-NEG-CONTROL` — Lipsitch, Tchetgen Tchetgen, and Cohen, 2010, negative controls for confounding and bias, DOI `10.1097/EDE.0b013e3181d61eeb`.
- `SRC-HARKING` — Kerr, 1998, HARKing, DOI `10.1207/s15327957pspr0203_4`.
- `SRC-ASA-PVALUE` — ASA statement: thresholds alone do not support scientific conclusions; p-values do not measure hypothesis truth or effect importance; full reporting is required.

### Rigor, reproducibility, and replication

- `SRC-NIH-RIGOR` — NIH guidance on scientific premise, rigorous design, relevant biological variables, authentication, and transparency.
- `SRC-NIH-REPLICATION` — NIH’s agency-wide replication and reproducibility initiative, page reviewed June 22, 2026.
- `SRC-NASEM-RR` — National Academies 2019 consensus report defining computational reproducibility and replicability with new data.
- `SRC-TOP` — Transparency and Openness Promotion guidelines.
- `SRC-NIH-DMS` — NIH Data Management and Sharing Policy.

Open practices remain subject to consent, privacy, community governance, intellectual property, export control, and security restrictions.

## Preregistration and intervention trials

- `SRC-COS-PREREG` — preregistration separates planned from unplanned work; transparent exploration remains valuable.
- `SRC-OSF-REG` — current OSF registration/preregistration implementation guidance.
- `SRC-COS-RR` — Registered Reports and results-blind protocol review.
- `SRC-SPIRIT-2025` — current 34-item randomized-trial protocol guideline; supersedes SPIRIT 2013.
- `SRC-CONSORT-2025` — current 30-item randomized-trial result-reporting guideline, including open science, harms, outcomes, intervention details, and important changes.

SPIRIT and CONSORT are reporting guidelines, not design-quality, ethics, regulatory, or efficacy certifications.

## Causal inference and estimands

- `SRC-WHATIF` — Hernán and Robins, *Causal Inference: What If*. The author page linked the latest revision found during verification.
- `SRC-ICH-E9R1` — ICH E9(R1), defining the estimand as the precise treatment-effect target and aligning planning, design, analysis, sensitivity analysis, and interpretation.

These sources ground the distinctions among target causal contrast, estimator, and estimate, and the explicit treatment of confounding, selection, collider, measurement, and intervention-definition assumptions.

## Responsible AI

- `SRC-NIST-GENAI` — NIST AI 600-1, covering confabulation, privacy, harmful bias/homogenization, information integrity, dangerous recommendations, and human–AI configuration.
- `SRC-UNESCO-AI` — human rights, privacy, accountability, transparency, diversity, and human oversight.
- `SRC-DOSHI-HAUSER` — Doshi and Hauser, 2024, DOI `10.1126/sciadv.adn5290`. In the studied story-writing task, AI-assisted outputs were more similar to one another while some individual creativity measures improved.

The primary homogenization result is task-specific. The skill treats idea homogenization as a plausible risk, not a universal measured effect across scientific domains.

## Ethics and oversight

### Humans

- `SRC-HHS-COMMON-RULE` — U.S. Common Rule/45 CFR 46 portal.
- `SRC-BELMONT` — respect for persons, beneficence, and justice.
- `SRC-HELSINKI` — World Medical Association Declaration of Helsinki, revised October 2024.

An authorized IRB/REC or equivalent must determine applicability; the skill does not self-declare exemption.

### Animals

- `SRC-OLAW-PHS` — PHS Policy and IACUC/Assurance requirements for covered work.
- `SRC-ARRIVE` — ARRIVE 2.0 reporting guidance.

### Biosafety and dual use

- `SRC-NIH-RSNA` — NIH Guidelines for research involving recombinant or synthetic nucleic acid molecules.
- `SRC-NIH-BIOSEC` — current NIH biosafety/biosecurity portal.
- `SRC-BMBL` — CDC/NIH BMBL sixth edition.
- `SRC-WHO-LIFE` — WHO Global Guidance Framework for the Responsible Use of the Life Sciences.

### U.S. dual-use transition status

At the verification date:

- `SRC-EO-14292` directed revision/replacement of the 2024 DURC/PEPP policy and pause/termination actions for covered dangerous gain-of-function research.
- `SRC-NIH-NOT-25-112` stated the Executive Order superseded NIH’s 2024 implementation and rescinded NOT-OD-25-061.
- `SRC-ASPR-DURC` still described the 2024 policy as awaiting revision or replacement and promised an update when the revised policy became available.

This status is time-sensitive. Recheck current federal, funder, award, institutional, and jurisdiction-specific rules before any related work. Do not use this ledger as clearance.

## Source-use rules

1. Verify each citation and identifier against the live primary source before publication or registration.
2. Recheck time-sensitive policy after the cutoff date.
3. Link every scientific claim to evidence in `assets/evidence_ledger_template.csv`.
4. Include challenging, null, and limitation evidence, not only support.
5. Do not infer novelty from this source ledger; it documents the skill refresh, not a user’s research topic.
6. Do not expose a sensitive research question in an external search query without authorization.
