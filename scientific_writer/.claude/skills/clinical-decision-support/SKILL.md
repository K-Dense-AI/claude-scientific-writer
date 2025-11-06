---
name: clinical-decision-support
description: "Generate professional clinical decision support (CDS) documents for pharmaceutical and clinical research settings, including patient cohort analyses (biomarker-stratified with outcomes) and treatment recommendation reports (evidence-based guidelines with decision algorithms). Supports GRADE evidence grading, statistical analysis (hazard ratios, survival curves, waterfall plots), biomarker integration, and regulatory compliance. Outputs publication-ready LaTeX/PDF format optimized for drug development, clinical research, and evidence synthesis."
---

# Clinical Decision Support Documents

## Description

Generate professional clinical decision support (CDS) documents for pharmaceutical companies, clinical researchers, and medical decision-makers. This skill specializes in analytical, evidence-based documents that inform treatment strategies and drug development:

1. **Patient Cohort Analysis** - Biomarker-stratified group analyses with statistical outcome comparisons
2. **Treatment Recommendation Reports** - Evidence-based clinical guidelines with GRADE grading and decision algorithms

All documents are generated as publication-ready LaTeX/PDF files optimized for pharmaceutical research, regulatory submissions, and clinical guideline development.

**Note:** For individual patient treatment plans at the bedside, use the `treatment-plans` skill instead. This skill focuses on group-level analyses and evidence synthesis for pharmaceutical/research settings.

## Capabilities

### Document Types

**Patient Cohort Analysis**
- Biomarker-based patient stratification (molecular subtypes, gene expression, IHC)
- Molecular subtype classification (e.g., GBM mesenchymal-immune-active vs proneural, breast cancer subtypes)
- Outcome metrics with statistical analysis (OS, PFS, ORR, DOR, DCR)
- Statistical comparisons between subgroups (hazard ratios, p-values, 95% CI)
- Survival analysis with Kaplan-Meier curves and log-rank tests
- Efficacy tables and waterfall plots
- Comparative effectiveness analyses
- Pharmaceutical cohort reporting (trial subgroups, real-world evidence)

**Treatment Recommendation Reports**
- Evidence-based treatment guidelines for specific disease states
- Strength of recommendation grading (GRADE system: 1A, 1B, 2A, 2B, 2C)
- Quality of evidence assessment (high, moderate, low, very low)
- Treatment algorithm flowcharts with TikZ diagrams
- Line-of-therapy sequencing based on biomarkers
- Decision pathways with clinical and molecular criteria
- Pharmaceutical strategy documents
- Clinical guideline development for medical societies

### Clinical Features

- **Biomarker Integration**: Genomic alterations (mutations, CNV, fusions), gene expression signatures, IHC markers, PD-L1 scoring
- **Statistical Analysis**: Hazard ratios, p-values, confidence intervals, survival curves, Cox regression, log-rank tests
- **Evidence Grading**: GRADE system (1A/1B/2A/2B/2C), Oxford CEBM levels, quality of evidence assessment
- **Clinical Terminology**: SNOMED-CT, LOINC, proper medical nomenclature, trial nomenclature
- **Regulatory Compliance**: HIPAA de-identification, confidentiality headers, ICH-GCP alignment
- **Professional Formatting**: Compact 0.5in margins, color-coded recommendations, publication-ready, suitable for regulatory submissions

## Pharmaceutical and Research Use Cases

This skill is specifically designed for pharmaceutical and clinical research applications:

**Drug Development**
- **Phase 2/3 Trial Analyses**: Biomarker-stratified efficacy and safety analyses
- **Subgroup Analyses**: Forest plots showing treatment effects across patient subgroups
- **Companion Diagnostic Development**: Linking biomarkers to drug response
- **Regulatory Submissions**: IND/NDA documentation with evidence summaries

**Medical Affairs**
- **KOL Education Materials**: Evidence-based treatment algorithms for thought leaders
- **Medical Strategy Documents**: Competitive landscape and positioning strategies
- **Advisory Board Materials**: Cohort analyses and treatment recommendation frameworks
- **Publication Planning**: Manuscript-ready analyses for peer-reviewed journals

**Clinical Guidelines**
- **Guideline Development**: Evidence synthesis with GRADE methodology for specialty societies
- **Consensus Recommendations**: Multi-stakeholder treatment algorithm development
- **Practice Standards**: Biomarker-based treatment selection criteria
- **Quality Measures**: Evidence-based performance metrics

**Real-World Evidence**
- **RWE Cohort Studies**: Retrospective analyses of patient cohorts from EMR data
- **Comparative Effectiveness**: Head-to-head treatment comparisons in real-world settings
- **Outcomes Research**: Long-term survival and safety in clinical practice
- **Health Economics**: Cost-effectiveness analyses by biomarker subgroup

## When to Use

Use this skill when you need to:

- **Analyze patient cohorts** stratified by biomarkers, molecular subtypes, or clinical characteristics
- **Generate treatment recommendation reports** with evidence grading for clinical guidelines or pharmaceutical strategies
- **Compare outcomes** between patient subgroups with statistical analysis (survival, response rates, hazard ratios)
- **Produce pharmaceutical research documents** for drug development, clinical trials, or regulatory submissions
- **Develop clinical practice guidelines** with GRADE evidence grading and decision algorithms
- **Document biomarker-guided therapy selection** at the population level (not individual patients)
- **Synthesize evidence** from multiple trials or real-world data sources
- **Create clinical decision algorithms** with flowcharts for treatment sequencing

**Do NOT use this skill for:**
- Individual patient treatment plans (use `treatment-plans` skill)
- Bedside clinical care documentation (use `treatment-plans` skill)
- Simple patient-specific treatment protocols (use `treatment-plans` skill)

## Document Structure

### Patient Cohort Analysis  
- **Executive Summary**: Cohort overview, key findings, clinical implications
- **Cohort Characteristics**: Demographics, baseline features, patient selection criteria
- **Biomarker Stratification**: Molecular subtypes, genomic alterations, IHC profiles
- **Treatment Exposure**: Therapies received, dosing, treatment duration by subgroup
- **Outcome Analysis**: Response rates (ORR, DCR), survival data (OS, PFS), DOR
- **Statistical Methods**: Kaplan-Meier survival curves, hazard ratios, log-rank tests, Cox regression
- **Subgroup Comparisons**: Biomarker-stratified efficacy, forest plots, statistical significance
- **Safety Profile**: Adverse events by subgroup, dose modifications, discontinuations
- **Clinical Recommendations**: Treatment implications based on biomarker profiles
- **Figures**: Waterfall plots, swimmer plots, survival curves, forest plots
- **Tables**: Demographics table, biomarker frequency, outcomes by subgroup

### Treatment Recommendation Reports
- **Clinical Context**: Disease state, epidemiology, current treatment landscape
- **Target Population**: Patient characteristics, biomarker criteria, staging
- **Evidence Review**: Systematic literature synthesis, guideline summary, trial data
- **Treatment Options**: Available therapies with mechanism of action
- **Evidence Grading**: GRADE assessment for each recommendation (1A, 1B, 2A, 2B, 2C)
- **Recommendations by Line**: First-line, second-line, subsequent therapies
- **Biomarker-Guided Selection**: Decision criteria based on molecular profiles
- **Treatment Algorithms**: TikZ flowcharts showing decision pathways
- **Monitoring Protocol**: Safety assessments, efficacy monitoring, dose modifications
- **Special Populations**: Elderly, renal/hepatic impairment, comorbidities
- **References**: Full bibliography with trial names and citations

## Output Format

- **Primary**: LaTeX/PDF with 0.5in margins for compact, data-dense presentation
- **Style**: Publication-ready, pharmaceutical-grade, suitable for regulatory submissions
- **Colors**: 
  - Recommendation boxes (green=strong recommendation, yellow=conditional, blue=research needed)
  - Biomarker stratification (color-coded molecular subtypes)
  - Statistical significance (color-coded p-values, hazard ratios)
- **Tables**: 
  - Demographics with baseline characteristics
  - Biomarker frequency by subgroup
  - Outcomes table (ORR, PFS, OS, DOR by molecular subtype)
  - Adverse events by cohort
  - Evidence summary tables with GRADE ratings
- **Figures**: 
  - Kaplan-Meier survival curves with log-rank p-values
  - Waterfall plots showing best response
  - Forest plots for subgroup analyses
  - TikZ decision algorithm flowcharts
  - Swimmer plots for individual patient timelines
- **Statistics**: Hazard ratios with 95% CI, p-values, median survival times
- **Compliance**: De-identification per HIPAA Safe Harbor, confidentiality notices for proprietary data

## Integration

This skill integrates with:
- **scientific-writing**: Citation management, statistical reporting, evidence synthesis
- **clinical-reports**: Medical terminology, HIPAA compliance, regulatory documentation
- **scientific-schematics**: TikZ flowcharts for decision algorithms and treatment pathways
- **treatment-plans**: Individual patient applications of cohort-derived insights (bidirectional)

## Key Differentiators from Treatment-Plans Skill

**Clinical Decision Support (this skill):**
- **Audience**: Pharmaceutical companies, clinical researchers, guideline committees, medical affairs
- **Scope**: Population-level analyses, evidence synthesis, guideline development
- **Focus**: Biomarker stratification, statistical comparisons, evidence grading
- **Output**: Multi-page analytical documents (5-15 pages typical) with extensive figures and tables
- **Use Cases**: Drug development, regulatory submissions, clinical practice guidelines, medical strategy
- **Example**: "Analyze 60 HER2+ breast cancer patients by hormone receptor status with survival outcomes"

**Treatment-Plans Skill:**
- **Audience**: Clinicians, patients, care teams
- **Scope**: Individual patient care planning
- **Focus**: SMART goals, patient-specific interventions, monitoring plans
- **Output**: Concise 1-4 page actionable care plans
- **Use Cases**: Bedside clinical care, EMR documentation, patient-centered planning
- **Example**: "Create treatment plan for a 55-year-old patient with newly diagnosed type 2 diabetes"

**When to use each:**
- Use **clinical-decision-support** for: cohort analyses, biomarker stratification studies, treatment guideline development, pharmaceutical strategy documents
- Use **treatment-plans** for: individual patient care plans, treatment protocols for specific patients, bedside clinical documentation

## Example Usage

### Patient Cohort Analysis

**Example 1: NSCLC Biomarker Stratification**
```
> Analyze a cohort of 45 NSCLC patients stratified by PD-L1 expression (<1%, 1-49%, ≥50%) 
> receiving pembrolizumab. Include outcomes: ORR, median PFS, median OS with hazard ratios 
> comparing PD-L1 ≥50% vs <50%. Generate Kaplan-Meier curves and waterfall plot.
```

**Example 2: GBM Molecular Subtype Analysis**
```
> Generate cohort analysis for 30 GBM patients classified into Cluster 1 (Mesenchymal-Immune-Active) 
> and Cluster 2 (Proneural) molecular subtypes. Compare outcomes including median OS, 6-month PFS rate, 
> and response to TMZ+bevacizumab. Include biomarker profile table and statistical comparison.
```

**Example 3: Breast Cancer HER2 Cohort**
```
> Analyze 60 HER2-positive metastatic breast cancer patients treated with trastuzumab-deruxtecan, 
> stratified by prior trastuzumab exposure (yes/no). Include ORR, DOR, median PFS with forest plot 
> showing subgroup analyses by hormone receptor status, brain metastases, and number of prior lines.
```

### Treatment Recommendation Report

**Example 1: HER2+ Metastatic Breast Cancer Guidelines**
```
> Create evidence-based treatment recommendations for HER2-positive metastatic breast cancer including 
> biomarker-guided therapy selection. Use GRADE system to grade recommendations for first-line 
> (trastuzumab+pertuzumab+taxane), second-line (trastuzumab-deruxtecan), and third-line options. 
> Include decision algorithm flowchart based on brain metastases, hormone receptor status, and prior therapies.
```

**Example 2: Advanced NSCLC Treatment Algorithm**
```
> Generate treatment recommendation report for advanced NSCLC based on PD-L1 expression, EGFR mutation, 
> ALK rearrangement, and performance status. Include GRADE-graded recommendations for each molecular subtype, 
> TikZ flowchart for biomarker-directed therapy selection, and evidence tables from KEYNOTE-189, FLAURA, 
> and CheckMate-227 trials.
```

**Example 3: Multiple Myeloma Line-of-Therapy Sequencing**
```
> Create treatment algorithm for newly diagnosed multiple myeloma through relapsed/refractory setting. 
> Include GRADE recommendations for transplant-eligible vs ineligible, high-risk cytogenetics considerations, 
> and sequencing of daratumumab, carfilzomib, and CAR-T therapy. Provide flowchart showing decision points 
> at each line of therapy.
```

## Key Features

### Biomarker Classification
- Genomic: Mutations, CNV, gene fusions
- Expression: RNA-seq, IHC scores
- Molecular subtypes: Disease-specific classifications
- Clinical actionability: Therapy selection guidance

### Outcome Metrics
- Survival: OS (overall survival), PFS (progression-free survival)
- Response: ORR (objective response rate), DOR (duration of response), DCR (disease control rate)
- Quality: ECOG performance status, symptom burden
- Safety: Adverse events, dose modifications

### Statistical Methods
- Survival analysis: Kaplan-Meier curves, log-rank tests
- Group comparisons: t-tests, chi-square, Fisher's exact
- Effect sizes: Hazard ratios, odds ratios with 95% CI
- Significance: p-values, multiple testing corrections

### Evidence Grading

**GRADE System**
- **1A**: Strong recommendation, high-quality evidence
- **1B**: Strong recommendation, moderate-quality evidence  
- **2A**: Weak recommendation, high-quality evidence
- **2B**: Weak recommendation, moderate-quality evidence
- **2C**: Weak recommendation, low-quality evidence

**Recommendation Strength**
- **Strong**: Benefits clearly outweigh risks
- **Conditional**: Trade-offs exist, patient values important
- **Research**: Insufficient evidence, clinical trials needed

## Best Practices

### For Cohort Analyses

1. **Patient Selection Transparency**: Clearly document inclusion/exclusion criteria, patient flow, and reasons for exclusions
2. **Biomarker Clarity**: Specify assay methods, platforms (e.g., FoundationOne, Caris), cut-points, and validation status
3. **Statistical Rigor**: 
   - Report hazard ratios with 95% confidence intervals, not just p-values
   - Include median follow-up time for survival analyses
   - Specify statistical tests used (log-rank, Cox regression, Fisher's exact)
   - Account for multiple comparisons when appropriate
4. **Outcome Definitions**: Use standard criteria:
   - Response: RECIST 1.1, iRECIST for immunotherapy
   - Adverse events: CTCAE version 5.0
   - Performance status: ECOG or Karnofsky
5. **Survival Data Presentation**:
   - Median OS/PFS with 95% CI
   - Landmark survival rates (6-month, 12-month, 24-month)
   - Number at risk tables below Kaplan-Meier curves
   - Censoring clearly indicated
6. **Subgroup Analyses**: Pre-specify subgroups; clearly label exploratory vs pre-planned analyses
7. **Data Completeness**: Report missing data and how it was handled

### For Treatment Recommendation Reports

1. **Evidence Grading Transparency**: 
   - Use GRADE system consistently (1A, 1B, 2A, 2B, 2C)
   - Document rationale for each grade
   - Clearly state quality of evidence (high, moderate, low, very low)
2. **Comprehensive Evidence Review**: 
   - Include phase 3 randomized trials as primary evidence
   - Supplement with phase 2 data for emerging therapies
   - Note real-world evidence and meta-analyses
   - Cite trial names (e.g., KEYNOTE-189, CheckMate-227)
3. **Biomarker-Guided Recommendations**:
   - Link specific biomarkers to therapy recommendations
   - Specify testing methods and validated assays
   - Include FDA/EMA approval status for companion diagnostics
4. **Clinical Actionability**: Every recommendation should have clear implementation guidance
5. **Decision Algorithm Clarity**: TikZ flowcharts should be unambiguous with clear yes/no decision points
6. **Special Populations**: Address elderly, renal/hepatic impairment, pregnancy, drug interactions
7. **Monitoring Guidance**: Specify safety labs, imaging, and frequency
8. **Update Frequency**: Date recommendations and plan for periodic updates

### General Best Practices

1. **De-identification**: Remove all 18 HIPAA identifiers before document generation (Safe Harbor method)
2. **Regulatory Compliance**: Include confidentiality notices for proprietary pharmaceutical data
3. **Publication-Ready Formatting**: Use 0.5in margins, professional fonts, color-coded sections
4. **Reproducibility**: Document all statistical methods to enable replication
5. **Conflict of Interest**: Disclose pharmaceutical funding or relationships when applicable

## References

See the `references/` directory for detailed guidance on:
- Patient cohort analysis and stratification methods
- Treatment recommendation development
- Clinical decision algorithms
- Biomarker classification and interpretation
- Outcome analysis and statistical methods
- Evidence synthesis and grading systems

## Templates

See the `assets/` directory for LaTeX templates:
- `cohort_analysis_template.tex` - Biomarker-stratified patient cohort analysis with statistical comparisons
- `treatment_recommendation_template.tex` - Evidence-based clinical practice guidelines with GRADE grading
- `clinical_pathway_template.tex` - TikZ decision algorithm flowcharts for treatment sequencing
- `biomarker_report_template.tex` - Molecular subtype classification and genomic profile reports
- `evidence_synthesis_template.tex` - Systematic evidence review and meta-analysis summaries

**Template Features:**
- 0.5in margins for compact presentation
- Color-coded recommendation boxes
- Professional tables for demographics, biomarkers, outcomes
- Built-in support for Kaplan-Meier curves, waterfall plots, forest plots
- GRADE evidence grading tables
- Confidentiality headers for pharmaceutical documents

## Scripts

See the `scripts/` directory for analysis and visualization tools:
- `generate_survival_analysis.py` - Kaplan-Meier curve generation with log-rank tests, hazard ratios, 95% CI
- `create_waterfall_plot.py` - Best response visualization for cohort analyses
- `create_forest_plot.py` - Subgroup analysis visualization with confidence intervals
- `create_cohort_tables.py` - Demographics, biomarker frequency, and outcomes tables
- `build_decision_tree.py` - TikZ flowchart generation for treatment algorithms
- `biomarker_classifier.py` - Patient stratification algorithms by molecular subtype
- `calculate_statistics.py` - Hazard ratios, Cox regression, log-rank tests, Fisher's exact
- `validate_cds_document.py` - Quality and compliance checks (HIPAA, statistical reporting standards)
- `grade_evidence.py` - Automated GRADE assessment helper for treatment recommendations

