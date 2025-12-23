"""
Oligon Brand Color Definitions

Color palette and cycles extracted from BRAND_COLORS_v4.md for use in PDF generation.
All colors are defined as HEX strings and can be converted to reportlab colors.
"""

from reportlab.lib.colors import HexColor


class BRAND_COLORS:
    """Oligon brand color palette."""

    # Primary Brand Color (Highlights & Key Accents)
    BRAND_BLUE = HexColor("#2DB2E8")

    # Neutral Data Colors (The Default)
    DARK_GRAY = HexColor("#222222")
    MEDIUM_GRAY = HexColor("#666666")
    MUTED_GRAY = HexColor("#999999")
    LIGHT_GRAY = HexColor("#BDBDBD")  # Annotations only, not for data

    # Scientific Contrast Colors
    CONTRAST_ORANGE = HexColor("#E8622D")
    DARK_WARM = HexColor("#7D250F")

    # Supporting Brand Blues (Limited Use)
    MEDIUM_BLUE = HexColor("#158BBB")
    DARK_TEAL = HexColor("#0F5D7D")

    # Background & Structure
    WHITE = HexColor("#FFFFFF")
    BLACK = HexColor("#000000")
    GRIDLINE = HexColor("#E5E5E5")

    # Hex string versions for compatibility
    HEX = {
        "brand_blue": "#2DB2E8",
        "dark_gray": "#222222",
        "medium_gray": "#666666",
        "muted_gray": "#999999",
        "light_gray": "#BDBDBD",
        "contrast_orange": "#E8622D",
        "dark_warm": "#7D250F",
        "medium_blue": "#158BBB",
        "dark_teal": "#0F5D7D",
        "white": "#FFFFFF",
        "black": "#000000",
        "gridline": "#E5E5E5",
    }


class ColorCycles:
    """Scenario-specific color cycles for scientific figures."""

    # Cycle 1: Control vs Treatment (Most Common)
    TREATMENT_CONTROL = [
        BRAND_COLORS.DARK_GRAY,
        BRAND_COLORS.BRAND_BLUE,
        BRAND_COLORS.MEDIUM_GRAY,
    ]

    # Cycle 2: Neutrals Only (No Designated Highlight)
    NEUTRALS_ONLY = [
        BRAND_COLORS.DARK_GRAY,
        BRAND_COLORS.MEDIUM_GRAY,
        BRAND_COLORS.MUTED_GRAY,
    ]

    # Cycle 3: Opposing Effects (Blue vs Orange)
    OPPOSING = [
        BRAND_COLORS.BRAND_BLUE,
        BRAND_COLORS.CONTRAST_ORANGE,
        BRAND_COLORS.DARK_GRAY,
    ]

    # Cycle 4: Multiple Categories (use sparingly)
    MULTI_CATEGORY = [
        BRAND_COLORS.DARK_GRAY,
        BRAND_COLORS.BRAND_BLUE,
        BRAND_COLORS.MEDIUM_GRAY,
        BRAND_COLORS.MEDIUM_BLUE,
    ]

    # Volcano plot specific
    VOLCANO = {
        "nonsig": BRAND_COLORS.LIGHT_GRAY,
        "up": BRAND_COLORS.CONTRAST_ORANGE,
        "down": BRAND_COLORS.BRAND_BLUE,
    }


# Typography standards
class Typography:
    """Font and size standards from brand guidelines."""

    # Approved font families (in preference order)
    FONT_FAMILY = ["Helvetica", "Arial", "DejaVu Sans"]
    PRIMARY_FONT = "Helvetica"
    BOLD_FONT = "Helvetica-Bold"

    # Font sizes for print/manuscript (in points)
    class Sizes:
        PANEL_LABEL = 10  # Panel labels (A, B, C) - bold
        PANEL_TITLE = 9  # Panel titles/headings
        AXIS_LABEL = 8  # Axis labels
        TICK_LABEL = 7  # Axis tick labels, legend text
        ANNOTATION = 7  # Annotations

    # Font sizes for reports/documents (scaled up for readability)
    class ReportSizes:
        TITLE = 24
        SUBTITLE = 14
        HEADING1 = 18
        HEADING2 = 14
        HEADING3 = 12
        BODY = 10
        CAPTION = 9
        FOOTNOTE = 8


# Page layout standards
class Layout:
    """Page layout and spacing standards."""

    # Margins (in points, 72 points = 1 inch)
    MARGIN_TOP = 72
    MARGIN_BOTTOM = 72
    MARGIN_LEFT = 72
    MARGIN_RIGHT = 72

    # Spacing
    LINE_SPACING = 1.2
    PARAGRAPH_SPACING = 12
    SECTION_SPACING = 24

    # Line weights (in points)
    THIN_LINE = 0.5
    NORMAL_LINE = 0.8
    THICK_LINE = 1.5
