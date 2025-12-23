"""
Example: Generate a Scientific PDF Report with Oligon Brand Styling

Run with: uv run examples/basic_report.py
"""

import sys
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.oligon_reports import ReportGenerator


def main():
    # Create report
    report = ReportGenerator(
        title="Compound X Efficacy Study",
        subtitle="Preliminary Results - Phase 1",
        author="Oligon Research Team",
    )

    # Executive Summary with metrics and key findings
    report.add_executive_summary(
        text=(
            "This report summarizes the preliminary findings from our Phase 1 efficacy "
            "study of Compound X. Initial results demonstrate promising therapeutic potential "
            "with favorable safety profiles across all tested dose levels. The study enrolled "
            "48 participants over a 12-week period, with primary endpoints achieved in the "
            "high-dose cohort."
        ),
        metrics=[
            ("48", "Participants"),
            ("92%", "Completion"),
            ("3", "Dose Levels"),
            ("12 wk", "Duration"),
        ],
        key_findings=[
            "Dose-dependent response observed",
            "No serious adverse events",
            "Primary endpoint met in high-dose group",
        ],
    )

    # Project Timeline
    report.add_section("Study Timeline", level=1)
    report.add_timeline([
        {"label": "Protocol", "date": "Jan 2024", "completed": True},
        {"label": "Enrollment", "date": "Mar 2024", "completed": True},
        {"label": "Treatment", "date": "Jun 2024", "completed": True},
        {"label": "Analysis", "date": "Sep 2024", "current": True},
        {"label": "Final Report", "date": "Dec 2024", "completed": False},
    ])

    # Background section
    report.add_section(
        "Background",
        content=(
            "Compound X is a novel small molecule inhibitor targeting the ABC pathway, "
            "which has been implicated in multiple disease states. Preclinical studies "
            "demonstrated significant efficacy in animal models with IC50 values in the "
            "nanomolar range. This Phase 1 study was designed to evaluate safety, "
            "tolerability, and preliminary efficacy in human subjects."
        ),
    )

    # Methods section
    report.add_section("Methods", level=1)

    report.add_section("Study Design", level=2)
    report.add_paragraph(
        "This was a randomized, double-blind, placebo-controlled study conducted at "
        "three clinical sites. Participants were randomized 3:1 to receive Compound X "
        "or placebo for 12 weeks."
    )

    report.add_section("Dose Escalation", level=2)
    report.add_table(
        data=[
            ["Cohort", "Dose", "N", "Duration"],
            ["Low", "10 mg QD", "12", "12 weeks"],
            ["Medium", "25 mg QD", "12", "12 weeks"],
            ["High", "50 mg QD", "12", "12 weeks"],
            ["Placebo", "—", "12", "12 weeks"],
        ],
    )

    # Results section
    report.add_section("Results", level=1)

    report.add_section("Primary Endpoint", level=2)
    report.add_paragraph(
        "The primary endpoint of 50% reduction in disease biomarker was achieved in "
        "75% of participants in the high-dose group compared to 17% in the placebo "
        "group (p < 0.001). Medium and low dose groups showed intermediate responses."
    )

    # Figure placeholder
    report.add_figure_placeholder(
        caption="Dose-response relationship for primary biomarker reduction at Week 12.",
        figure_id="1",
    )

    report.add_section("Safety", level=2)
    report.add_paragraph(
        "Compound X was generally well tolerated across all dose levels. The most "
        "common adverse events were mild headache (15%) and nausea (10%), which "
        "resolved without intervention."
    )

    # Warning callout
    report.add_callout(
        text=(
            "Two participants in the high-dose group experienced transient elevations "
            "in liver enzymes (< 2x ULN) that normalized upon continued treatment. "
            "Enhanced monitoring is recommended for future studies."
        ),
        title="Safety Note",
        box_type="warning",
    )

    # Discussion
    report.add_section(
        "Discussion",
        content=(
            "These preliminary results support the continued development of Compound X. "
            "The observed dose-response relationship and favorable safety profile provide "
            "a strong foundation for Phase 2 studies. The efficacy signal in the high-dose "
            "group exceeded pre-specified thresholds, suggesting potential for clinically "
            "meaningful benefit."
        ),
    )

    # Next Steps
    report.add_section("Next Steps", level=1)
    report.add_callout(
        text=(
            "Phase 2 study design in progress • Target enrollment: 200 participants • "
            "Primary endpoint: Clinical response at Week 24 • Anticipated start: Q1 2025"
        ),
        title="Upcoming Milestones",
        box_type="success",
    )

    # Build and save
    output_path = "example_report.pdf"
    report.build(output_path)
    print(f"Report generated: {output_path}")


if __name__ == "__main__":
    main()
