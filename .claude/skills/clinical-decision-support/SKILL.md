---
name: clinical-decision-support
description: "Generate professional clinical decision support (CDS) documents including individual patient treatment plans, patient cohort analyses (biomarker-stratified with outcomes), and treatment recommendation reports (evidence-based guidelines with decision algorithms). Supports GRADE evidence grading, statistical analysis (hazard ratios, survival curves), biomarker integration, and HIPAA compliance. Outputs compact LaTeX/PDF format for pharmaceutical and clinical research settings."
---

# Clinical Decision Support Documents

## Description

Generate professional clinical decision support (CDS) documents for medical professionals in pharmaceutical and clinical research settings. This skill supports three types of clinical documents:

1. **Individual Patient Treatment Plans** - Personalized treatment protocols for specific patients
2. **Patient Cohort Analysis** - Biomarker-stratified group analyses with outcome comparisons
3. **Treatment Recommendation Reports** - Evidence-based clinical guidelines and decision algorithms

All documents are generated as compact, professional LaTeX/PDF files optimized for clinical use.

## Capabilities

### Document Types

**Individual Patient Treatment Plans**
- Personalized recommendations based on patient-specific factors
- Condition-specific treatment protocols
- Medication dosing and schedules
- Monitoring and follow-up plans
- HIPAA-compliant de-identification

**Patient Cohort Analysis**
- Biomarker-based patient stratification
- Molecular subtype classification (e.g., GBM clusters, breast cancer subtypes)
- Outcome metrics (OS, PFS, ORR, response rates)
- Statistical comparisons between subgroups
- Survival analysis and efficacy tables

**Treatment Recommendation Reports**
- Evidence-based treatment guidelines
- Strength of recommendation grading (GRADE system)
- Treatment algorithm flowcharts
- Line-of-therapy sequencing
- Decision pathways with clinical criteria

### Clinical Features

- **Biomarker Integration**: Genomic alterations, gene expression, IHC markers
- **Statistical Analysis**: Hazard ratios, p-values, confidence intervals, survival curves
- **Evidence Grading**: GRADE, Oxford CEBM levels of evidence
- **Clinical Terminology**: SNOMED-CT, LOINC, proper medical nomenclature
- **Regulatory Compliance**: HIPAA de-identification, confidentiality headers
- **Professional Formatting**: Compact 0.5in margins, color-coded recommendations, publication-ready

## When to Use

Use this skill when you need to:

- Create treatment plans for individual patients with specific conditions
- Analyze patient cohorts stratified by biomarkers or clinical characteristics  
- Generate evidence-based treatment recommendations with decision algorithms
- Produce pharmaceutical-grade clinical analysis documents
- Compare outcomes between patient subgroups
- Document biomarker-guided therapy selection

## Document Structure

### Individual Treatment Plans
- **Executive Summary**: Condition overview and key recommendations
- **Patient Profile**: Demographics, comorbidities, risk factors
- **Treatment Protocol**: Medications, dosing, administration
- **Monitoring Plan**: Tests, frequency, parameters to track
- **Follow-up Schedule**: Visit frequency and assessments
- **References**: Evidence supporting recommendations

### Patient Cohort Analysis  
- **Executive Summary**: Cohort overview and key findings
- **Cohort Characteristics**: Demographics, baseline features
- **Biomarker Profile**: Molecular subtypes, genomic alterations
- **Treatment Outcomes**: Response rates, survival data
- **Statistical Analysis**: Subgroup comparisons, hazard ratios
- **Clinical Recommendations**: Treatment implications

### Treatment Recommendation Reports
- **Clinical Context**: Disease state, patient population
- **Evidence Review**: Literature synthesis, guideline summary
- **Treatment Options**: Available therapies with evidence grades
- **Recommendations**: Strength-graded treatment algorithms
- **Monitoring Protocol**: Safety and efficacy assessments
- **Decision Flowcharts**: TikZ-based clinical pathways

## Output Format

- **Primary**: LaTeX/PDF with 0.5in margins
- **Style**: Professional, compact, publication-ready
- **Colors**: Recommendation boxes (green=strong, yellow=conditional, blue=research)
- **Tables**: Patient demographics, biomarkers, outcomes, statistical comparisons
- **Figures**: Survival curves, waterfall plots, decision trees
- **Compliance**: HIPAA de-identification, confidentiality notices

## Integration

This skill integrates with:
- **scientific-writing**: Citation management, statistical reporting
- **clinical-reports**: Medical terminology, HIPAA compliance
- **scientific-schematics**: TikZ flowcharts for decision algorithms

## Example Usage

### Individual Treatment Plan
```
> Create a treatment plan for a 55-year-old patient with newly diagnosed type 2 diabetes and hypertension
```

### Patient Cohort Analysis
```
> Analyze a cohort of 45 NSCLC patients stratified by PD-L1 expression (<1%, 1-49%, ≥50%) with outcomes including ORR, PFS, and OS

> Generate cohort analysis for 30 GBM patients classified into mesenchymal-immune-active and proneural molecular subtypes
```

### Treatment Recommendation Report
```
> Create treatment recommendations for HER2-positive metastatic breast cancer including biomarker-guided therapy selection

> Generate evidence-based treatment algorithm for heart failure management based on NYHA class and ejection fraction
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

1. **De-identification**: Remove all 18 HIPAA identifiers before document generation
2. **Evidence Citations**: Include references for all clinical recommendations
3. **Statistical Rigor**: Report confidence intervals, not just p-values
4. **Biomarker Clarity**: Specify assay methods and cut-points
5. **Clinical Actionability**: Link biomarkers to specific therapies
6. **Grading Transparency**: Clearly state evidence levels and recommendation strength
7. **Cohort Details**: Report patient selection criteria and exclusions
8. **Outcome Definitions**: Use standard criteria (RECIST, CTCAE, etc.)

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
- `cohort_analysis_template.tex` - Patient group analysis
- `treatment_recommendation_template.tex` - Evidence-based guidelines
- `clinical_pathway_template.tex` - Decision algorithm flowcharts
- `biomarker_report_template.tex` - Genomic profile reports

## Scripts

See the `scripts/` directory for analysis tools:
- `generate_survival_analysis.py` - Kaplan-Meier curve generation
- `create_cohort_tables.py` - Demographics and outcomes tables
- `build_decision_tree.py` - Automated flowchart generation
- `biomarker_classifier.py` - Patient stratification algorithms
- `validate_cds_document.py` - Quality and compliance checks

