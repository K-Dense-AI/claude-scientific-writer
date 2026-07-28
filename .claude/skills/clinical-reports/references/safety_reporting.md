# Safety Reporting Boundaries

Safety reporting is role-, product-, phase-, source-, jurisdiction-, and time-dependent. This skill formats verified aggregate counts only. It does not determine seriousness, severity, causality, expectedness, reportability, clock start, destination, format, or follow-up.

## Core distinctions

- **Adverse event (AE)**: an untoward medical occurrence temporally associated with a medicinal product; causality is not required.
- **Adverse reaction / suspected adverse reaction**: a causal relationship is at least reasonably possible or otherwise meets the applicable regional definition.
- **Seriousness**: outcome or regulatory criterion such as death, life-threatening experience at the time, hospitalization, disability/incapacity, congenital anomaly, or another medically important event.
- **Severity**: intensity. A severe event is not automatically serious; a serious event need not be severe in intensity.
- **Expectedness**: comparison with the applicable reference safety information under the governing procedure.

Only an authorized qualified safety professional may make or approve these assessments.

## ICH routes

### E2A — pre-approval expedited reporting

ICH E2A (Step 4, 27 October 1994) defines standards for expedited reporting during clinical development. It describes minimum information for an initial report and the distinction among serious, unexpected, and suspected reactions.

Do not apply E2A as a universal post-approval rule or encode its timelines without the current regional requirement and sponsor procedure.

### E2B(R3) — ICSR electronic data and message specification

E2B(R3) defines data elements and electronic transmission for individual case safety reports. It covers pre- and post-approval ICSRs within scope. It does not:

- decide whether a case is reportable;
- define an aggregate safety table;
- replace E2A, E2D(R1), or regional rules;
- validate clinical coding or narrative accuracy.

The ICH index listed E2B(R3) Q&As at Step 5 dated 18 July 2025 when checked. Use the current implementation guide, Q&As, code lists, regional implementation guide, and receiving-system rules.

### E2D(R1) — post-approval individual cases

ICH adopted E2D(R1), **Post-Approval Safety Data: Definitions and Standards for Management and Reporting of Individual Case Safety Reports**, on 15 September 2025.

It addresses post-approval ICSR sources and case management, including organized data collection systems, literature, digital platforms, and patient-support programs. It explicitly directs users to:

- E2B for ICSR structure/format/data elements;
- E2C for periodic aggregate safety reporting;
- regional/local requirements where they differ.

Do not use the aggregate formatter for an ICSR or use E2D(R1) to invent missing case data.

### E2C(R2) — periodic aggregate reporting

Where applicable, E2C(R2) addresses periodic benefit-risk evaluation reporting. Applicability and regional format require qualified review. Aggregate tables in this skill are display aids, not periodic reports.

## FDA IND safety reporting

For applicable US IND studies, 21 CFR 312.32 controls sponsor IND safety reporting. FDA issued final sponsor and investigator safety-reporting guidances in December 2025. The sponsor guidance includes aggregate-data assessment considerations; the investigator guidance clarifies investigator-to-sponsor and IRB responsibilities.

FDA’s IND safety-reporting page, current 23 June 2026 when checked, states:

- sponsors report qualifying potential serious risks under 21 CFR 312.32;
- unexpected fatal or life-threatening suspected adverse reactions have a 7-calendar-day outer limit after the relevant sponsor determination/receipt described by the regulation;
- other qualifying reports generally use the applicable 15-calendar-day requirement;
- as of 1 April 2026, commercial IND reports under 21 CFR 312.32(c)(1)(i) use FDA AEMS with E2B(R3), with stated exemptions for noncommercial INDs;
- other categories described on the page use the applicable eCTD route.

This summary is not a reporting clock or filing instruction. The responsible sponsor, investigator, IRB/IEC, and regulatory professionals must consult the current regulation, guidance, protocol, and procedures for each event.

## Aggregate formatter input

`format_adverse_events.py` accepts only aggregate rows:

- analysis set;
- treatment group;
- MedDRA version;
- system organ class;
- preferred term;
- subjects affected;
- event count;
- denominator.

It also requires a populated `clinical_trial_safety_aggregate_template.json` sidecar
that records authorization, protocol/SAP/data-cut references, analysis set, counting
and threshold rules, MedDRA version/language, provenance, and pending human reviews.

It rejects row-level identifiers, verbatim narratives, case IDs, and onset dates. It checks arithmetic and group consistency but does not verify:

- MedDRA term/code validity;
- coding quality or hierarchy placement;
- treatment relatedness;
- seriousness or fatality;
- analysis-set correctness;
- deduplication;
- whether a subject appears in multiple terms or SOCs;
- statistical inference.

## MedDRA caveats

MedDRA 29.0 (March 2026; transition date 4 May 2026) was current when this skill was refreshed. A report must use the study/sponsor-authorized dictionary version, not automatically the newest version.

State the exact version and language. Terms can change currency, names, or hierarchy across releases; codes can persist through renames. Use licensed official files and MedDRA Points to Consider. A syntax checker cannot validate coding.

## Required handoff

Every aggregate table must disclose:

- analysis set and denominator per group;
- whether values are subjects, events, or both;
- MedDRA version and language;
- counting rules and threshold supplied by the protocol/SAP;
- missing or suppressed cells;
- no inferential claim unless separately verified;
- qualified safety and statistical review required;
- not suitable for individual-case submission.
