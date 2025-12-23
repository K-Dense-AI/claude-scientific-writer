"""Oligon Reports - Professional PDF report generation with Oligon brand standards."""

from .brand_colors import BRAND_COLORS, ColorCycles
from .components import CalloutBox, MetricCard, SectionDivider, Timeline
from .report_generator import ReportGenerator

__version__ = "0.1.0"
__all__ = [
    "BRAND_COLORS",
    "ColorCycles",
    "ReportGenerator",
    "MetricCard",
    "CalloutBox",
    "Timeline",
    "SectionDivider",
]
