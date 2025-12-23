"""
Generate Three Distinct Pareto Analysis PDF Reports

Creates professional, modern PDF reports with Oligon brand styling:
1. Executive Dashboard - Visual metrics and key findings
2. Technical Deep-Dive - Full methodology and detailed tables
3. Decision Support Brief - Actionable recommendations

Run with: uv run examples/pareto_reports.py
"""

import sys
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from reportlab.lib.units import inch

from src.oligon_reports import ReportGenerator
from src.oligon_reports.brand_colors import BRAND_COLORS
from src.oligon_reports.components import (
    MetricCardRow,
)

# =============================================================================
# REPORT 1: EXECUTIVE DASHBOARD
# =============================================================================

def create_executive_dashboard():
    """
    Executive Dashboard Report

    A visually-driven report emphasizing metrics, status indicators,
    and key findings. Designed for rapid scanning by decision-makers.
    """
    report = ReportGenerator(
        title="Pareto Frontier Analysis",
        subtitle="STAT3 siRNA Candidate Optimization Dashboard",
        author="Computational Biology Team",
    )

    # --- Executive Summary with Visual Metrics ---
    report.add_executive_summary(
        text=(
            "Multi-objective Pareto analysis identified 37 non-dominated candidates from 2,256 total "
            "siRNA candidates targeting STAT3 (NM_139276). The v4 composite ranking shows poor alignment "
            "with the Pareto frontier, indicating potential missed opportunities in candidate selection."
        ),
        metrics=[
            ("37", "Frontier Size"),
            ("29.7%", "v4 Overlap"),
            ("26", "Buried Candidates"),
            ("0", "Dominated"),
        ],
        key_findings=[
            "Poor v4/Pareto agreement suggests hidden value candidates",
            "26 Pareto-optimal candidates buried outside v4 top-20",
            "BLAST specificity dominates v4 scoring (78% reduction)",
        ]
    )

    report.add_spacer(0.2 * inch)

    # --- Agreement Status Panel ---
    report.add_callout(
        text=(
            "The v4 composite ranking diverges substantially from the Pareto frontier with only 29.7% overlap. "
            "This indicates the weighted composite may be over-emphasizing or under-emphasizing certain objectives. "
            "Manual review of buried frontier candidates is strongly recommended."
        ),
        title="STATUS: POOR AGREEMENT",
        box_type="warning"
    )

    # --- Key Metrics Table ---
    report.add_section("Analysis Overview", level=1)

    overview_data = [
        ["Metric", "Value", "Interpretation"],
        ["Gene Target", "STAT3", "Signal Transducer and Activator of Transcription 3"],
        ["Transcript", "NM_139276", "Human reference sequence"],
        ["Total Candidates", "2,256", "Full candidate pool analyzed"],
        ["Pareto Frontier", "37 candidates", "Non-dominated optimal trade-offs"],
        ["v4 Top-20 Overlap", "11/37 (29.7%)", "Concordance between methods"],
        ["Buried Frontier", "26 candidates", "Pareto-optimal but low v4 rank"],
        ["Dominated in Top-20", "0 candidates", "v4 picks beaten on all objectives"],
    ]
    report.add_table(overview_data, col_widths=[1.8*inch, 1.5*inch, 3.2*inch])

    # --- Visual Objectives Summary ---
    report.add_section("Optimization Objectives", level=1)
    report.add_paragraph(
        "The Pareto analysis evaluates candidates across four independent objectives that capture "
        "non-redundant aspects of siRNA quality:"
    )

    objectives_data = [
        ["#", "Objective", "Column", "Goal", "Description"],
        ["1", "Efficacy", "v4_adjusted_efficacy", "Maximize", "Intrinsic knockdown potential (ML + design rules)"],
        ["2", "BLAST Specificity", "v4_blast_specificity", "Maximize", "Transcriptome-wide off-target freedom"],
        ["3", "Seed Specificity", "v4_seed_specificity", "Maximize", "Seed region cleanliness (POTS, Ui-Tei Tm)"],
        ["4", "Ortholog Conservation", "v4_ortholog", "Maximize", "Human-mouse conservation (0.4/0.7/1.0)"],
    ]
    report.add_table(objectives_data, col_widths=[0.3*inch, 1.3*inch, 1.5*inch, 0.8*inch, 2.6*inch])

    report.add_page_break()

    # --- Consensus Candidates (High Confidence) ---
    report.add_section("Consensus Candidates", level=1)
    report.add_callout(
        text=(
            "These 18 candidates are validated by both ranking methods - they appear in both the v4 Top-20 "
            "AND the Pareto frontier. These represent the safest choices for experimental validation."
        ),
        title="Highest Confidence Selections",
        box_type="success"
    )

    consensus_data = [
        ["Position", "v4 Rank", "Efficacy", "BLAST", "Seed", "Ortholog", "v4 Score"],
        ["829", "1", "94.6", "1.000", "0.500", "0.7", "28.35"],
        ["2144", "1", "80.3", "0.449", "0.500", "1.0", "13.73"],
        ["2159", "2", "82.8", "0.219", "0.855", "1.0", "11.57"],
        ["677", "3", "92.7", "0.340", "0.855", "0.7", "16.39"],
        ["2161", "3", "84.4", "0.141", "1.000", "1.0", "10.33"],
        ["1339", "4", "89.3", "0.340", "0.500", "1.0", "13.18"],
        ["2181", "4", "95.8", "0.219", "0.500", "1.0", "8.68"],
        ["676", "5", "67.1", "0.340", "0.900", "0.7", "12.48"],
        ["2162", "5", "88.0", "0.113", "1.000", "1.0", "8.65"],
        ["827", "7", "97.5", "0.449", "0.500", "0.7", "11.88"],
        ["1730", "8", "73.0", "0.267", "0.900", "0.7", "10.68"],
        ["212", "11", "84.0", "0.219", "1.000", "0.7", "9.27"],
        ["1550", "12", "88.0", "0.340", "1.000", "0.4", "9.10"],
        ["1411", "13", "89.3", "0.415", "0.855", "0.4", "8.60"],
        ["2143", "15", "96.5", "0.141", "0.500", "1.0", "4.80"],
        ["2036", "17", "94.1", "0.091", "1.000", "0.7", "4.71"],
        ["1009", "17", "63.7", "0.644", "0.650", "0.4", "7.83"],
        ["674", "20", "87.4", "0.141", "1.000", "0.7", "7.50"],
    ]
    report.add_table(consensus_data, col_widths=[0.7*inch, 0.7*inch, 0.8*inch, 0.7*inch, 0.6*inch, 0.8*inch, 0.8*inch])

    report.add_page_break()

    # --- Weight Sensitivity Visualization ---
    report.add_section("Component Impact Analysis", level=1)
    report.add_paragraph(
        "The v4 formula uses multiplicative combination where each component acts as a gate. "
        "Analysis reveals significant imbalance in component influence:"
    )

    impact_data = [
        ["Component", "Median Value", "Reduction from 100%", "Impact Level"],
        ["Efficacy", "84.8", "15.2%", "Low"],
        ["BLAST Specificity", "0.2187", "78.1%", "HIGH"],
        ["Seed Specificity", "0.9000", "10.0%", "Low"],
        ["Ortholog Conservation", "1.0", "0.0%", "Low"],
    ]
    report.add_table(impact_data, col_widths=[1.8*inch, 1.3*inch, 1.5*inch, 1.3*inch])

    report.add_callout(
        text=(
            "BLAST Dominance Alert: The 78% reduction from BLAST specificity dominates the v4 ranking. "
            "Candidates with BLAST < 0.15 are heavily penalized regardless of excellence in other objectives. "
            "This may exclude high-efficacy, dual-species candidates that could be valuable."
        ),
        title="Weight Calibration Warning",
        box_type="warning"
    )

    # --- Action Items ---
    report.add_section("Recommended Actions", level=1)

    report.add_callout(
        text=(
            "1. Review 26 buried frontier candidates for hidden value opportunities. "
            "2. Re-evaluate v4 weight calibration given BLAST dominance finding. "
            "3. Consider Pareto rank as complementary selection criterion for validation panels."
        ),
        title="Next Steps",
        box_type="info"
    )

    # Build the report
    report.build("pareto_executive_dashboard.pdf")
    print("Generated: pareto_executive_dashboard.pdf")


# =============================================================================
# REPORT 2: TECHNICAL DEEP-DIVE
# =============================================================================

def create_technical_analysis():
    """
    Technical Deep-Dive Report

    Comprehensive analysis with full methodology, algorithm details,
    all data tables, and pattern analysis. For technical audiences.
    """
    report = ReportGenerator(
        title="Pareto Frontier Analysis",
        subtitle="Technical Report: STAT3 siRNA Multi-Objective Optimization",
        author="Computational Biology - Technical Documentation",
    )

    # --- Technical Overview ---
    report.add_section("Introduction", level=1)
    report.add_paragraph(
        "This technical report presents a comprehensive Pareto frontier analysis of 2,256 siRNA "
        "candidates targeting human STAT3 (transcript NM_139276). The analysis compares multi-objective "
        "Pareto optimization with the v4 composite scoring system to identify agreement patterns "
        "and potential optimization opportunities."
    )

    analysis_params = [
        ["Parameter", "Value"],
        ["Gene", "STAT3"],
        ["Transcript", "NM_139276"],
        ["Species", "Human"],
        ["Total Candidates", "2,256"],
        ["Analysis Date", "2025-12-11T13:16:34.195830"],
        ["Top-N for Comparison", "20"],
    ]
    report.add_table(analysis_params, col_widths=[2.5*inch, 4*inch])

    # --- Methodology Section ---
    report.add_section("Methodology", level=1)

    report.add_section("The Composite Score Problem", level=2)
    report.add_paragraph(
        "Traditional composite scores combine multiple objectives into a single number using fixed weights. "
        "The general form is: S_composite = w1*Efficacy + w2*BLAST + w3*Seed + w4*Ortholog. "
        "This approach has fundamental limitations:"
    )
    report.add_paragraph(
        "Hidden trade-offs: A candidate with excellent efficacy but poor specificity might score identically "
        "to one with moderate values across all metrics. Weight sensitivity: Different weight choices produce "
        "different rankings, making the 'best' candidate subjective. Lost information: The single score "
        "obscures which objectives each candidate excels at."
    )

    report.add_section("Pareto Dominance Definition", level=2)
    report.add_paragraph(
        "Pareto analysis provides a weight-free alternative by identifying mathematically optimal trade-offs. "
        "Candidate A dominates Candidate B if and only if: (1) A is at least as good as B on ALL objectives, "
        "AND (2) A is strictly better than B on AT LEAST ONE objective. The Pareto Frontier (Rank 1) contains "
        "all candidates not dominated by any other candidate - these represent optimal trade-offs where "
        "improvement on any objective requires sacrificing another."
    )

    report.add_section("Algorithm Specification", level=2)
    report.add_paragraph(
        "The Pareto ranking algorithm proceeds as follows: (1) Dominance Check: For each pair (A, B), "
        "determine if A dominates B by comparing all objective values. (2) Frontier Identification: "
        "Rank 1 consists of all candidates dominated by zero others. (3) Iterative Ranking: Remove Rank 1 "
        "candidates, identify new frontier as Rank 2, repeat until all candidates ranked."
    )

    complexity_data = [
        ["Metric", "Value", "Notes"],
        ["Time Complexity", "O(n² × d × k)", "n=candidates, d=objectives, k=ranks"],
        ["Candidates (n)", "2,256", "Full candidate pool"],
        ["Objectives (d)", "4", "Efficacy, BLAST, Seed, Ortholog"],
        ["Total Comparisons", "~20.4M", "Computed pairwise dominance checks"],
    ]
    report.add_table(complexity_data, col_widths=[1.8*inch, 1.5*inch, 3.2*inch])

    report.add_page_break()

    # --- Objectives Detail ---
    report.add_section("Objective Specifications", level=1)
    report.add_paragraph(
        "The analysis uses four objectives capturing independent, non-redundant aspects of siRNA quality. "
        "All objectives are maximization targets where higher values indicate better performance."
    )

    obj_detail = [
        ["Objective", "Column", "Range", "Description"],
        ["Efficacy", "v4_adjusted_efficacy", "0-100+", "Intrinsic knockdown potential from ML model combined with design rules"],
        ["BLAST Specificity", "v4_blast_specificity", "0.0-1.0", "Freedom from transcriptome-wide off-targets (0=many hits, 1=none)"],
        ["Seed Specificity", "v4_seed_specificity", "0.0-1.0", "Seed region cleanliness: POTS score, Ui-Tei Tm (0=risky, 1=clean)"],
        ["Ortholog Conservation", "v4_ortholog", "0.4/0.7/1.0", "Human-mouse conservation for cross-species utility"],
    ]
    report.add_table(obj_detail, col_widths=[1.3*inch, 1.5*inch, 0.8*inch, 2.9*inch])

    report.add_paragraph(
        "Objective independence rationale: Efficacy measures potency (how well the siRNA silences target). "
        "BLAST Specificity measures genome-wide off-target risk (safety). Seed Specificity measures "
        "seed-mediated off-target risk (complementary safety metric). Ortholog Conservation measures "
        "cross-species utility (translational value). A candidate must balance ALL objectives - "
        "excellence in one cannot compensate for failure in another."
    )

    # --- Full Frontier Composition ---
    report.add_section("Complete Pareto Frontier", level=1)
    report.add_paragraph(
        "The Pareto frontier contains 37 candidates representing optimal trade-offs across all four objectives. "
        "Each frontier candidate offers a unique balance - no other candidate in the pool beats it on all metrics."
    )

    frontier_data = [
        ["Position", "v4 Rank", "Efficacy", "BLAST", "Seed", "Ortholog", "v4 Tier"],
        ["829", "1", "94.6", "1.000", "0.500", "0.7", "Excellent"],
        ["2144", "1", "80.3", "0.449", "0.500", "1.0", "Excellent"],
        ["2159", "2", "82.8", "0.219", "0.855", "1.0", "Excellent"],
        ["677", "3", "92.7", "0.340", "0.855", "0.7", "Excellent"],
        ["2161", "3", "84.4", "0.141", "1.000", "1.0", "Excellent"],
        ["1339", "4", "89.3", "0.340", "0.500", "1.0", "Excellent"],
        ["2181", "4", "95.8", "0.219", "0.500", "1.0", "Excellent"],
        ["676", "5", "67.1", "0.340", "0.900", "0.7", "Excellent"],
        ["2162", "5", "88.0", "0.113", "1.000", "1.0", "Excellent"],
        ["827", "7", "97.5", "0.449", "0.500", "0.7", "Excellent"],
        ["1730", "8", "73.0", "0.267", "0.900", "0.7", "Excellent"],
        ["212", "11", "84.0", "0.219", "1.000", "0.7", "Excellent"],
        ["1550", "12", "88.0", "0.340", "1.000", "0.4", "Excellent"],
        ["1411", "13", "89.3", "0.415", "0.855", "0.4", "Excellent"],
        ["2143", "15", "96.5", "0.141", "0.500", "1.0", "Good"],
    ]
    report.add_table(frontier_data, col_widths=[0.7*inch, 0.7*inch, 0.8*inch, 0.7*inch, 0.6*inch, 0.8*inch, 0.9*inch])

    report.add_page_break()

    # --- Buried Frontier Analysis ---
    report.add_section("Buried Frontier Candidates", level=1)
    report.add_paragraph(
        "26 candidates are Pareto-optimal (not dominated by any other candidate) but ranked outside the v4 top-20. "
        "These represent potentially valuable candidates that the weighted composite under-values."
    )

    buried_data = [
        ["Position", "v4 Rank", "Efficacy", "BLAST", "Seed", "Ortholog", "Notable Strength"],
        ["637", "21", "87.7", "0.154", "0.900", "0.7", "High Seed, Good Ortholog"],
        ["1563", "22", "88.9", "0.449", "0.607", "0.4", "Balanced Profile"],
        ["787", "24", "89.5", "0.289", "1.000", "0.4", "Perfect Seed"],
        ["625", "27", "93.3", "0.340", "0.650", "0.4", "Balanced Profile"],
        ["1954", "46", "91.9", "0.091", "0.742", "1.0", "Full Ortholog Conservation"],
        ["1874", "55", "93.8", "0.141", "1.000", "0.4", "Perfect Seed, High Efficacy"],
        ["1346", "57", "100.4", "0.091", "0.568", "1.0", "Exceptional Efficacy + Ortholog"],
        ["1955", "59", "94.7", "0.091", "0.598", "1.0", "High Efficacy + Full Ortholog"],
        ["1625", "61", "92.8", "0.091", "0.629", "1.0", "Full Ortholog Conservation"],
        ["1069", "78", "101.9", "0.091", "0.500", "1.0", "Maximum Efficacy + Full Ortholog"],
    ]
    report.add_table(buried_data, col_widths=[0.6*inch, 0.6*inch, 0.7*inch, 0.6*inch, 0.6*inch, 0.7*inch, 2.0*inch])

    report.add_section("Pattern Analysis", level=2)
    pattern_data = [
        ["Metric", "Buried Frontier", "v4 Top-20", "Delta"],
        ["Mean Efficacy", "95.6", "83.5", "+12.1"],
        ["Mean BLAST", "0.1488", "0.2636", "-0.1147"],
    ]
    report.add_table(pattern_data, col_widths=[1.8*inch, 1.5*inch, 1.5*inch, 1.2*inch])

    report.add_paragraph(
        "Key observation: Buried frontier candidates show significantly higher mean efficacy (+12.1) but "
        "lower BLAST specificity (-0.1147). This confirms that the v4 composite heavily penalizes low BLAST "
        "scores even when other objectives are exceptional."
    )

    report.add_section("Ortholog Distribution in Buried Frontier", level=2)
    ortho_dist = [
        ["Ortholog Value", "Interpretation", "Count", "Percentage"],
        ["1.0", "Full dual-species (human + mouse)", "6", "32%"],
        ["0.7", "Partial conservation", "5", "26%"],
        ["0.4", "Human-only", "8", "42%"],
    ]
    report.add_table(ortho_dist, col_widths=[1.2*inch, 2.5*inch, 0.8*inch, 1*inch])

    report.add_callout(
        text=(
            "32% of buried candidates have full ortholog conservation (1.0). These candidates are particularly "
            "valuable for translational research requiring human-mouse dual-species experiments. Their low "
            "v4 ranking may represent systematic under-valuation of cross-species utility."
        ),
        title="Translational Research Implication",
        box_type="info"
    )

    report.add_page_break()

    # --- Dominated Analysis ---
    report.add_section("Dominated Candidates in v4 Top-20", level=1)
    report.add_paragraph(
        "Dominated candidates are those where another candidate beats them on ALL four objectives simultaneously. "
        "There is no scenario where a dominated candidate would be preferred - the dominating alternative is "
        "strictly superior. The following v4 top-20 picks are dominated:"
    )

    dominated_data = [
        ["Position", "v4 Rank", "Efficacy", "BLAST", "Seed", "Ortholog", "Dominated By"],
        ["828", "2", "91.3", "0.698", "0.500", "0.7", "Position 117"],
        ["1619", "6", "88.7", "0.340", "0.500", "1.0", "Position 117"],
        ["2179", "6", "82.6", "0.219", "0.500", "1.0", "Position 117"],
        ["2160", "7", "65.4", "0.141", "1.000", "1.0", "Position 117"],
        ["2132", "8", "76.3", "0.141", "1.000", "1.0", "Position 117"],
        ["77", "9", "83.4", "0.340", "0.585", "0.7", "Position 117"],
        ["2134", "9", "82.4", "0.129", "0.950", "1.0", "Position 117"],
        ["626", "10", "88.0", "0.340", "0.950", "0.4", "Position 117"],
        ["2133", "10", "74.3", "0.113", "1.000", "1.0", "Position 117"],
        ["2173", "11", "83.8", "0.091", "1.000", "1.0", "Position 117"],
    ]
    report.add_table(dominated_data, col_widths=[0.7*inch, 0.7*inch, 0.7*inch, 0.7*inch, 0.6*inch, 0.7*inch, 1.2*inch])

    report.add_callout(
        text=(
            "These candidates rank highly only due to v4's specific weight choices. From a Pareto perspective, "
            "they should be replaced with their dominating alternatives (Position 117 in all cases above) "
            "which offer superior performance across all measured objectives."
        ),
        title="Recommendation",
        box_type="warning"
    )

    # --- Weight Sensitivity ---
    report.add_section("v4 Weight Sensitivity Analysis", level=1)
    report.add_paragraph(
        "The v4 formula uses multiplicative combination where each component acts as a gate: "
        "Score = Efficacy * BLAST * Seed * Ortholog * Access / 115 * 100. "
        "This structure means low values in any component can dramatically reduce the final score."
    )

    weight_impact = [
        ["Component", "Median Value", "Reduction from 100%", "Impact Assessment"],
        ["Efficacy", "84.8", "15.2%", "Low - Most candidates maintain good efficacy"],
        ["BLAST Specificity", "0.2187", "78.1%", "HIGH - Dominant factor in score reduction"],
        ["Seed Specificity", "0.9000", "10.0%", "Low - Generally high across candidates"],
        ["Ortholog Conservation", "1.0", "0.0%", "Low - Modal value at maximum"],
    ]
    report.add_table(weight_impact, col_widths=[1.5*inch, 1.1*inch, 1.3*inch, 2.1*inch])

    report.add_callout(
        text=(
            "Critical Finding: The 78% reduction from BLAST specificity dominates the v4 ranking algorithm. "
            "Candidates with BLAST < 0.15 are heavily penalized regardless of exceptional performance on "
            "other objectives. This creates a systematic bias that may exclude high-value candidates "
            "for applications where efficacy or cross-species conservation is prioritized over maximum specificity."
        ),
        title="BLAST Dominance Effect",
        box_type="warning"
    )

    # --- Technical Details ---
    report.add_section("Data Sources and Reproducibility", level=1)

    sources_data = [
        ["Item", "Value"],
        ["Input File", "siRNA_candidates/STAT3/human/scored/STAT3.human.NM_139276.3.CDS.scored.csv"],
        ["Objective Columns", "v4_adjusted_efficacy, v4_blast_specificity, v4_seed_specificity, v4_ortholog"],
        ["Top-N Comparison", "20"],
        ["Pipeline Version", "1.0"],
        ["Content Hash", "4ee5c4210717ab92"],
        ["Input Hash", "d57c0c4df00ad7c5"],
    ]
    report.add_table(sources_data, col_widths=[1.8*inch, 4.7*inch])

    report.build("pareto_technical_analysis.pdf")
    print("Generated: pareto_technical_analysis.pdf")


# =============================================================================
# REPORT 3: DECISION SUPPORT BRIEF
# =============================================================================

def create_decision_brief():
    """
    Decision Support Brief

    Action-oriented report with use-case specific guidance,
    trade-off archetypes, and clear recommendations.
    """
    report = ReportGenerator(
        title="siRNA Selection Guide",
        subtitle="Decision Support: STAT3 Pareto-Optimal Candidates",
        author="Translational Research Advisory",
    )

    # --- Decision Context ---
    report.add_section("Selection Context", level=1)

    report.add_callout(
        text=(
            "This guide provides actionable recommendations for STAT3 siRNA selection based on "
            "Pareto frontier analysis. Use this document to identify optimal candidates for your "
            "specific experimental requirements and risk tolerance."
        ),
        title="Purpose",
        box_type="info"
    )

    context_metrics = [
        ("2,256", "Candidates Analyzed"),
        ("37", "Pareto-Optimal"),
        ("18", "Consensus Picks"),
        ("26", "Hidden Value"),
    ]
    report.elements.append(MetricCardRow(
        context_metrics,
        accent_colors=[
            BRAND_COLORS.DARK_GRAY,
            BRAND_COLORS.BRAND_BLUE,
            BRAND_COLORS.MEDIUM_BLUE,
            BRAND_COLORS.CONTRAST_ORANGE,
        ]
    ))
    report.add_spacer(0.3 * inch)

    # --- Agreement Assessment ---
    report.add_section("v4 vs Pareto Agreement", level=1)
    report.add_paragraph(
        "Understanding the alignment between the v4 composite score and Pareto frontier helps "
        "determine how much to trust each ranking method for your selection decisions."
    )

    agreement_guide = [
        ["Agreement Level", "Overlap", "Recommended Approach"],
        ["Good (>60%)", "Trust v4", "Use v4 ranking as primary; composite weights are well-calibrated"],
        ["Moderate (40-60%)", "Hybrid", "Use v4 as primary, review buried frontier for hidden gems"],
        ["Poor (<40%)", "Caution", "Do not rely solely on v4; use Pareto as complementary criterion"],
    ]
    report.add_table(agreement_guide, col_widths=[1.3*inch, 1.2*inch, 4*inch])

    report.add_callout(
        text=(
            "Current Status: 29.7% overlap indicates POOR AGREEMENT. The v4 composite may be "
            "over-weighting BLAST specificity at the expense of efficacy and cross-species conservation. "
            "Review buried frontier candidates carefully before finalizing selections."
        ),
        title="This Analysis: Poor Agreement",
        box_type="warning"
    )

    report.add_page_break()

    # --- Trade-off Archetypes ---
    report.add_section("Candidate Archetypes", level=1)
    report.add_paragraph(
        "Pareto frontier candidates cluster into distinct archetypes based on their trade-off profiles. "
        "Identify the archetype that best matches your experimental priorities:"
    )

    archetypes = [
        ["Archetype", "Efficacy", "BLAST", "Seed", "Ortholog", "Best Use Case"],
        ["Potency Champion", "HIGH", "Med", "Med", "Med", "Maximum knockdown, moderate safety margin"],
        ["Safety First", "Med", "HIGH", "HIGH", "Med", "Clinical applications, therapeutic development"],
        ["Balanced Profile", "Med", "Med", "Med", "Med", "General purpose, initial screening"],
        ["Translational", "Med", "Med", "Med", "HIGH", "Human-mouse studies, in vivo validation"],
    ]
    report.add_table(archetypes, col_widths=[1.2*inch, 0.7*inch, 0.6*inch, 0.6*inch, 0.8*inch, 2.6*inch])

    # --- Use-Case Specific Recommendations ---
    report.add_section("Use-Case Specific Guidance", level=1)

    report.add_section("For Dual-Species Experiments (Human + Mouse)", level=2)
    report.add_paragraph(
        "If your experimental plan includes mouse models for in vivo validation, prioritize candidates "
        "with high ortholog conservation. The following buried frontier candidates with ortholog >= 0.7 "
        "may be undervalued by the v4 composite:"
    )

    dual_species = [
        ["Position", "Efficacy", "BLAST", "Seed", "Ortholog", "Key Advantage"],
        ["930", "102.9", "Low", "0.500", "0.7", "Exceptional efficacy + mouse compatible"],
        ["1069", "101.9", "Low", "0.500", "1.0", "Maximum efficacy + full conservation"],
        ["1346", "100.4", "Low", "0.568", "1.0", "High efficacy + full conservation"],
        ["797", "98.9", "Low", "0.475", "0.7", "Strong efficacy + mouse compatible"],
        ["1685", "97.7", "Low", "0.500", "0.7", "Good efficacy + mouse compatible"],
    ]
    report.add_table(dual_species, col_widths=[0.8*inch, 0.8*inch, 0.6*inch, 0.6*inch, 0.8*inch, 2.4*inch])

    report.add_callout(
        text=(
            "These candidates trade BLAST specificity for efficacy and cross-species utility. "
            "Accept higher off-target potential only if your application can tolerate it and "
            "validates with appropriate controls."
        ),
        title="Trade-off Advisory",
        box_type="neutral"
    )

    report.add_section("For Human-Only Experiments (Maximum Specificity)", level=2)
    report.add_paragraph(
        "For clinical or therapeutic applications where specificity is paramount, prioritize "
        "consensus candidates with high BLAST scores:"
    )

    human_only = [
        ["Position", "BLAST", "Efficacy", "Seed", "Ortholog", "Notes"],
        ["1009", "0.644", "63.7", "0.650", "0.4", "Best BLAST specificity in consensus"],
        ["1411", "0.415", "89.3", "0.855", "0.4", "Good balance of specificity + efficacy"],
        ["1550", "0.340", "88.0", "1.000", "0.4", "High efficacy + perfect seed"],
        ["829", "1.000", "94.6", "0.500", "0.7", "Perfect BLAST + high efficacy (rare)"],
    ]
    report.add_table(human_only, col_widths=[0.8*inch, 0.7*inch, 0.8*inch, 0.6*inch, 0.8*inch, 2.6*inch])

    report.add_page_break()

    report.add_section("For Balanced Panel Selection", level=2)
    report.add_paragraph(
        "To maximize experimental robustness and reduce risk, select a diverse panel covering "
        "multiple trade-off profiles. Recommended strategy: 2-3 consensus candidates + 2-3 buried "
        "frontier candidates."
    )

    report.add_callout(
        text=(
            "Suggested Panel (6 candidates): "
            "Consensus: Pos 829 (high BLAST), Pos 677 (balanced), Pos 2161 (high seed). "
            "Buried Frontier: Pos 1346 (high efficacy + ortholog), Pos 787 (perfect seed), "
            "Pos 1069 (maximum efficacy)."
        ),
        title="Sample Balanced Panel",
        box_type="success"
    )

    # --- Risk Assessment ---
    report.add_section("Selection Risk Assessment", level=1)

    risk_matrix = [
        ["Selection Strategy", "Efficacy Risk", "Specificity Risk", "Translation Risk", "Overall"],
        ["v4 Top-20 Only", "Medium", "Low", "High", "Medium-High"],
        ["Consensus Only", "Low", "Low", "Medium", "Low"],
        ["Buried Frontier Only", "Low", "High", "Low", "Medium"],
        ["Balanced Panel", "Low", "Medium", "Low", "LOW"],
    ]
    report.add_table(risk_matrix, col_widths=[1.5*inch, 1*inch, 1.1*inch, 1.1*inch, 0.9*inch])

    report.add_paragraph(
        "Risk definitions: Efficacy Risk = chance of poor knockdown. Specificity Risk = chance of "
        "off-target effects. Translation Risk = chance of species-specific results that don't "
        "translate to in vivo models."
    )

    # --- Action Checklist ---
    report.add_section("Decision Checklist", level=1)

    checklist = [
        ["Step", "Action", "Status"],
        ["1", "Define experimental context (human-only vs dual-species)", "[ ]"],
        ["2", "Identify acceptable trade-off profile (archetype selection)", "[ ]"],
        ["3", "Review consensus candidates matching your profile", "[ ]"],
        ["4", "Review buried frontier candidates for hidden value", "[ ]"],
        ["5", "Compose diverse panel (2-3 profiles represented)", "[ ]"],
        ["6", "Validate selections with independent assays", "[ ]"],
        ["7", "Document selection rationale for reproducibility", "[ ]"],
    ]
    report.add_table(checklist, col_widths=[0.5*inch, 4.5*inch, 0.8*inch])

    # --- Final Recommendation ---
    report.add_callout(
        text=(
            "Given the poor v4/Pareto alignment (29.7%), do not rely solely on v4 ranking. "
            "The consensus candidates (18 total) represent the safest starting point. "
            "For maximum experimental coverage, augment with 2-3 buried frontier candidates "
            "selected based on your specific experimental requirements."
        ),
        title="Summary Recommendation",
        box_type="info"
    )

    report.build("pareto_decision_brief.pdf")
    print("Generated: pareto_decision_brief.pdf")


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("Generating Pareto Analysis PDF Reports...")
    print("-" * 50)

    create_executive_dashboard()
    create_technical_analysis()
    create_decision_brief()

    print("-" * 50)
    print("All reports generated successfully!")
    print("\nFiles created:")
    print("  1. pareto_executive_dashboard.pdf")
    print("  2. pareto_technical_analysis.pdf")
    print("  3. pareto_decision_brief.pdf")
