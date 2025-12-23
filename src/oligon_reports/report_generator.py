"""
PDF Report Generator

Main class for creating professional scientific PDF reports
with Oligon brand styling.
"""

from datetime import datetime
from pathlib import Path
from typing import Any

from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from .brand_colors import BRAND_COLORS, Layout, Typography
from .components import (
    CalloutBox,
    FigurePlaceholder,
    MetricCardRow,
    SectionDivider,
    Timeline,
)


class ReportGenerator:
    """
    Professional PDF report generator with Oligon brand styling.

    Example:
        report = ReportGenerator("Project Report", "Research Team")
        report.add_executive_summary("Key findings...", metrics=[("95%", "Accuracy")])
        report.add_section("Methods", "Description of methods...")
        report.build("output.pdf")
    """

    def __init__(
        self,
        title: str,
        author: str = None,
        subtitle: str = None,
        date: str = None,
    ):
        self.title = title
        self.author = author
        self.subtitle = subtitle
        self.date = date or datetime.now().strftime("%B %d, %Y")

        self.elements: list[Any] = []
        self.styles = self._create_styles()

    def _create_styles(self) -> dict:
        """Create brand-styled paragraph styles."""
        base_styles = getSampleStyleSheet()

        styles = {
            "title": ParagraphStyle(
                "BrandTitle",
                parent=base_styles["Title"],
                fontName=Typography.BOLD_FONT,
                fontSize=Typography.ReportSizes.TITLE,
                textColor=BRAND_COLORS.DARK_GRAY,
                spaceAfter=6,
                alignment=TA_CENTER,
            ),
            "subtitle": ParagraphStyle(
                "BrandSubtitle",
                parent=base_styles["Normal"],
                fontName=Typography.PRIMARY_FONT,
                fontSize=Typography.ReportSizes.SUBTITLE,
                textColor=BRAND_COLORS.MEDIUM_GRAY,
                spaceAfter=12,
                alignment=TA_CENTER,
            ),
            "heading1": ParagraphStyle(
                "BrandH1",
                parent=base_styles["Heading1"],
                fontName=Typography.BOLD_FONT,
                fontSize=Typography.ReportSizes.HEADING1,
                textColor=BRAND_COLORS.DARK_GRAY,
                spaceBefore=24,
                spaceAfter=12,
                borderColor=BRAND_COLORS.BRAND_BLUE,
                borderWidth=0,
                borderPadding=0,
            ),
            "heading2": ParagraphStyle(
                "BrandH2",
                parent=base_styles["Heading2"],
                fontName=Typography.BOLD_FONT,
                fontSize=Typography.ReportSizes.HEADING2,
                textColor=BRAND_COLORS.DARK_GRAY,
                spaceBefore=18,
                spaceAfter=8,
            ),
            "heading3": ParagraphStyle(
                "BrandH3",
                parent=base_styles["Heading3"],
                fontName=Typography.BOLD_FONT,
                fontSize=Typography.ReportSizes.HEADING3,
                textColor=BRAND_COLORS.MEDIUM_GRAY,
                spaceBefore=12,
                spaceAfter=6,
            ),
            "body": ParagraphStyle(
                "BrandBody",
                parent=base_styles["Normal"],
                fontName=Typography.PRIMARY_FONT,
                fontSize=Typography.ReportSizes.BODY,
                textColor=BRAND_COLORS.DARK_GRAY,
                leading=14,
                spaceAfter=8,
                alignment=TA_JUSTIFY,
            ),
            "caption": ParagraphStyle(
                "BrandCaption",
                parent=base_styles["Normal"],
                fontName=Typography.PRIMARY_FONT,
                fontSize=Typography.ReportSizes.CAPTION,
                textColor=BRAND_COLORS.MEDIUM_GRAY,
                spaceAfter=12,
            ),
            "footer": ParagraphStyle(
                "BrandFooter",
                parent=base_styles["Normal"],
                fontName=Typography.PRIMARY_FONT,
                fontSize=8,
                textColor=BRAND_COLORS.MUTED_GRAY,
                alignment=TA_CENTER,
            ),
        }

        return styles

    def _add_cover_page(self):
        """Add a branded cover page."""
        # Top accent bar
        self.elements.append(Spacer(1, 2 * inch))

        # Title
        self.elements.append(Paragraph(self.title, self.styles["title"]))

        # Subtitle
        if self.subtitle:
            self.elements.append(Paragraph(self.subtitle, self.styles["subtitle"]))

        self.elements.append(Spacer(1, 0.5 * inch))

        # Decorative line
        self.elements.append(SectionDivider(style="gradient"))

        self.elements.append(Spacer(1, 1 * inch))

        # Author and date
        if self.author:
            author_style = ParagraphStyle(
                "Author",
                parent=self.styles["body"],
                alignment=TA_CENTER,
                textColor=BRAND_COLORS.MEDIUM_GRAY,
            )
            self.elements.append(Paragraph(self.author, author_style))

        date_style = ParagraphStyle(
            "Date",
            parent=self.styles["body"],
            alignment=TA_CENTER,
            textColor=BRAND_COLORS.MUTED_GRAY,
        )
        self.elements.append(Paragraph(self.date, date_style))

        self.elements.append(PageBreak())

    def add_executive_summary(
        self,
        text: str,
        metrics: list[tuple[str, str]] = None,
        key_findings: list[str] = None,
    ):
        """
        Add an executive summary section with optional metrics and findings.

        Args:
            text: Summary paragraph text
            metrics: List of (value, label) tuples for metric cards
            key_findings: List of key finding strings for callout
        """
        self.elements.append(SectionDivider("Executive Summary", style="line"))
        self.elements.append(Spacer(1, 12))

        # Metric cards
        if metrics:
            card_row = MetricCardRow(metrics)
            self.elements.append(card_row)
            self.elements.append(Spacer(1, 18))

        # Summary text
        self.elements.append(Paragraph(text, self.styles["body"]))
        self.elements.append(Spacer(1, 12))

        # Key findings callout
        if key_findings:
            findings_text = " • ".join(key_findings)
            callout = CalloutBox(
                findings_text,
                title="Key Findings",
                box_type="info",
            )
            self.elements.append(callout)
            self.elements.append(Spacer(1, 12))

    def add_section(
        self,
        title: str,
        content: str = None,
        level: int = 1,
    ):
        """
        Add a content section with heading.

        Args:
            title: Section heading
            content: Paragraph content (optional)
            level: Heading level (1, 2, or 3)
        """
        style_map = {
            1: "heading1",
            2: "heading2",
            3: "heading3",
        }
        heading_style = self.styles.get(style_map.get(level, "heading1"))

        if level == 1:
            self.elements.append(SectionDivider(title, style="line"))
        else:
            self.elements.append(Paragraph(title, heading_style))

        if content:
            self.elements.append(Spacer(1, 6))
            self.elements.append(Paragraph(content, self.styles["body"]))

    def add_paragraph(self, text: str):
        """Add a body paragraph."""
        self.elements.append(Paragraph(text, self.styles["body"]))

    def add_callout(
        self,
        text: str,
        title: str = None,
        box_type: str = "info",
    ):
        """
        Add a callout box.

        Args:
            text: Callout content
            title: Optional callout title
            box_type: 'info', 'warning', 'neutral', or 'success'
        """
        callout = CalloutBox(text, title=title, box_type=box_type)
        self.elements.append(callout)
        self.elements.append(Spacer(1, 12))

    def add_timeline(self, milestones: list[dict]):
        """
        Add a project timeline.

        Args:
            milestones: List of dicts with 'label', 'date', 'completed', 'current' keys
        """
        timeline = Timeline(milestones)
        self.elements.append(Spacer(1, 12))
        self.elements.append(timeline)
        self.elements.append(Spacer(1, 18))

    def add_figure_placeholder(
        self,
        caption: str = None,
        figure_id: str = None,
        width: float = 5 * inch,
        height: float = 3 * inch,
    ):
        """Add a placeholder for a figure."""
        placeholder = FigurePlaceholder(
            width=width,
            height=height,
            caption=caption,
            figure_id=figure_id,
        )
        self.elements.append(placeholder)
        self.elements.append(Spacer(1, 12))

    def add_image(
        self,
        image_path: str,
        width: float = None,
        height: float = None,
        caption: str = None,
    ):
        """
        Add an image to the report.

        Args:
            image_path: Path to image file
            width: Optional width (maintains aspect ratio if height not set)
            height: Optional height
            caption: Optional figure caption
        """
        img = Image(image_path)
        if width:
            img.drawWidth = width
            if not height:
                # Maintain aspect ratio
                aspect = img.imageHeight / img.imageWidth
                img.drawHeight = width * aspect
        if height:
            img.drawHeight = height

        self.elements.append(img)

        if caption:
            self.elements.append(Spacer(1, 4))
            self.elements.append(Paragraph(caption, self.styles["caption"]))

        self.elements.append(Spacer(1, 12))

    def add_table(
        self,
        data: list[list],
        col_widths: list[float] = None,
        header: bool = True,
    ):
        """
        Add a styled table.

        Args:
            data: 2D list of table data (first row is header if header=True)
            col_widths: Optional list of column widths
            header: Whether first row is a header
        """
        table = Table(data, colWidths=col_widths)

        # Brand-styled table
        style_commands = [
            # All cells
            ("FONTNAME", (0, 0), (-1, -1), Typography.PRIMARY_FONT),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("TEXTCOLOR", (0, 0), (-1, -1), BRAND_COLORS.DARK_GRAY),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            # Grid
            ("LINEBELOW", (0, 0), (-1, -1), 0.5, BRAND_COLORS.GRIDLINE),
        ]

        if header:
            style_commands.extend([
                ("FONTNAME", (0, 0), (-1, 0), Typography.BOLD_FONT),
                ("TEXTCOLOR", (0, 0), (-1, 0), BRAND_COLORS.DARK_GRAY),
                ("LINEBELOW", (0, 0), (-1, 0), 1.5, BRAND_COLORS.BRAND_BLUE),
                ("BACKGROUND", (0, 0), (-1, 0), BRAND_COLORS.GRIDLINE),
            ])

        table.setStyle(TableStyle(style_commands))
        self.elements.append(table)
        self.elements.append(Spacer(1, 12))

    def add_spacer(self, height: float = 0.25 * inch):
        """Add vertical space."""
        self.elements.append(Spacer(1, height))

    def add_page_break(self):
        """Add a page break."""
        self.elements.append(PageBreak())

    def _header_footer(self, canvas: canvas.Canvas, doc):
        """Draw header and footer on each page."""
        canvas.saveState()

        # Header - thin brand blue line
        canvas.setStrokeColor(BRAND_COLORS.BRAND_BLUE)
        canvas.setLineWidth(1)
        canvas.line(
            Layout.MARGIN_LEFT,
            letter[1] - Layout.MARGIN_TOP + 20,
            letter[0] - Layout.MARGIN_RIGHT,
            letter[1] - Layout.MARGIN_TOP + 20,
        )

        # Footer - page number
        canvas.setFont(Typography.PRIMARY_FONT, 8)
        canvas.setFillColor(BRAND_COLORS.MUTED_GRAY)
        page_num = canvas.getPageNumber()
        canvas.drawCentredString(
            letter[0] / 2,
            Layout.MARGIN_BOTTOM - 20,
            f"{page_num}",
        )

        # Footer - title on left
        canvas.drawString(
            Layout.MARGIN_LEFT,
            Layout.MARGIN_BOTTOM - 20,
            self.title[:50],  # Truncate long titles
        )

        canvas.restoreState()

    def build(self, output_path: str, include_cover: bool = True):
        """
        Build and save the PDF report.

        Args:
            output_path: Output file path
            include_cover: Whether to include cover page
        """
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            leftMargin=Layout.MARGIN_LEFT,
            rightMargin=Layout.MARGIN_RIGHT,
            topMargin=Layout.MARGIN_TOP,
            bottomMargin=Layout.MARGIN_BOTTOM,
        )

        # Build element list
        final_elements = []

        if include_cover:
            self._add_cover_page()
            final_elements.extend(self.elements)
        else:
            final_elements.extend(self.elements)

        # Build PDF
        doc.build(
            final_elements,
            onFirstPage=self._header_footer,
            onLaterPages=self._header_footer,
        )

        return Path(output_path)
