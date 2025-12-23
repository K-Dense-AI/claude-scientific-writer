"""
Reusable PDF Report Components

Unique design elements for professional scientific reports:
- MetricCard: Highlighted key numbers/statistics
- CalloutBox: Critical findings or alerts
- Timeline: Visual milestone progression
- SectionDivider: Brand-colored section separators
"""

from reportlab.lib.units import inch
from reportlab.platypus import Flowable

from .brand_colors import BRAND_COLORS, Typography


class MetricCard(Flowable):
    """
    A highlighted metric card for displaying key numbers.

    Creates a rounded box with brand accent color containing
    a large number and descriptive label.
    """

    def __init__(
        self,
        value: str,
        label: str,
        width: float = 1.5 * inch,
        height: float = 0.9 * inch,
        accent_color=None,
    ):
        super().__init__()
        self.value = value
        self.label = label
        self.box_width = width
        self.box_height = height
        self.accent_color = accent_color or BRAND_COLORS.BRAND_BLUE
        self.width = width
        self.height = height

    def draw(self):
        canvas = self.canv

        # Draw rounded rectangle background
        canvas.setFillColor(self.accent_color)
        canvas.roundRect(
            0,
            0,
            self.box_width,
            self.box_height,
            radius=6,
            fill=1,
            stroke=0,
        )

        # Draw value (large, white, centered)
        canvas.setFillColor(BRAND_COLORS.WHITE)
        canvas.setFont(Typography.BOLD_FONT, 22)
        value_y = self.box_height * 0.55
        canvas.drawCentredString(self.box_width / 2, value_y, self.value)

        # Draw label (smaller, white, centered)
        canvas.setFont(Typography.PRIMARY_FONT, 9)
        label_y = self.box_height * 0.2
        canvas.drawCentredString(self.box_width / 2, label_y, self.label)


class MetricCardRow(Flowable):
    """A row of metric cards with automatic spacing."""

    def __init__(self, metrics: list[tuple[str, str]], accent_colors: list = None):
        """
        Args:
            metrics: List of (value, label) tuples
            accent_colors: Optional list of colors for each card
        """
        super().__init__()
        self.metrics = metrics
        self.accent_colors = accent_colors or [BRAND_COLORS.BRAND_BLUE] * len(metrics)
        self.card_width = 1.5 * inch
        self.card_height = 0.9 * inch
        self.spacing = 0.25 * inch
        self.width = len(metrics) * self.card_width + (len(metrics) - 1) * self.spacing
        self.height = self.card_height

    def draw(self):
        x_offset = 0
        for i, (value, label) in enumerate(self.metrics):
            if i < len(self.accent_colors):
                color = self.accent_colors[i]
            else:
                color = BRAND_COLORS.BRAND_BLUE
            card = MetricCard(value, label, self.card_width, self.card_height, color)
            card.canv = self.canv
            self.canv.saveState()
            self.canv.translate(x_offset, 0)
            card.draw()
            self.canv.restoreState()
            x_offset += self.card_width + self.spacing


class CalloutBox(Flowable):
    """
    A callout box for highlighting critical findings or alerts.

    Features a colored left border and subtle background.
    """

    def __init__(
        self,
        text: str,
        title: str = None,
        width: float = 5.5 * inch,
        box_type: str = "info",
    ):
        """
        Args:
            text: Main callout text
            title: Optional title for the callout
            width: Box width
            box_type: 'info' (brand blue), 'warning' (orange), 'neutral' (gray)
        """
        super().__init__()
        self.text = text
        self.title = title
        self.box_width = width
        self.box_type = box_type
        self.width = width

        # Set colors based on type
        color_map = {
            "info": BRAND_COLORS.BRAND_BLUE,
            "warning": BRAND_COLORS.CONTRAST_ORANGE,
            "neutral": BRAND_COLORS.DARK_TEAL,
            "success": BRAND_COLORS.MEDIUM_BLUE,
        }
        self.accent_color = color_map.get(box_type, BRAND_COLORS.BRAND_BLUE)

        # Calculate height based on text
        self._calculate_height()

    def _calculate_height(self):
        """Estimate box height based on text length."""
        # Rough estimate: 15 chars per line, 14pt line height
        text_width = self.box_width - 0.5 * inch
        chars_per_line = int(text_width / 6)  # ~6 points per char at 10pt
        num_lines = max(1, len(self.text) // chars_per_line + 1)
        title_height = 18 if self.title else 0
        self.height = num_lines * 14 + title_height + 24  # padding

    def draw(self):
        canvas = self.canv

        # Draw background
        canvas.setFillColor(BRAND_COLORS.GRIDLINE)
        canvas.rect(0, 0, self.box_width, self.height, fill=1, stroke=0)

        # Draw left accent bar
        bar_width = 4
        canvas.setFillColor(self.accent_color)
        canvas.rect(0, 0, bar_width, self.height, fill=1, stroke=0)

        # Draw title if present
        y_pos = self.height - 16
        if self.title:
            canvas.setFillColor(self.accent_color)
            canvas.setFont(Typography.BOLD_FONT, 11)
            canvas.drawString(bar_width + 12, y_pos, self.title)
            y_pos -= 16

        # Draw text
        canvas.setFillColor(BRAND_COLORS.DARK_GRAY)
        canvas.setFont(Typography.PRIMARY_FONT, 10)

        # Simple text wrapping
        words = self.text.split()
        line = ""
        x_start = bar_width + 12
        max_width = self.box_width - x_start - 12

        for word in words:
            test_line = f"{line} {word}".strip()
            if canvas.stringWidth(test_line, Typography.PRIMARY_FONT, 10) < max_width:
                line = test_line
            else:
                canvas.drawString(x_start, y_pos, line)
                y_pos -= 14
                line = word
        if line:
            canvas.drawString(x_start, y_pos, line)


class Timeline(Flowable):
    """
    A horizontal timeline showing project milestones.

    Creates a visual progression with labeled milestones.
    """

    def __init__(
        self,
        milestones: list[dict],
        width: float = 6 * inch,
        height: float = 1.2 * inch,
    ):
        """
        Args:
            milestones: List of dicts with 'label', 'date', and optional 'completed' bool
            width: Timeline width
            height: Timeline height
        """
        super().__init__()
        self.milestones = milestones
        self.timeline_width = width
        self.timeline_height = height
        self.width = width
        self.height = height

    def draw(self):
        canvas = self.canv
        n = len(self.milestones)
        if n == 0:
            return

        # Timeline bar position
        bar_y = self.timeline_height * 0.5
        bar_height = 4

        # Draw background bar (full timeline)
        canvas.setFillColor(BRAND_COLORS.GRIDLINE)
        canvas.roundRect(
            0, bar_y - bar_height / 2,
            self.timeline_width, bar_height,
            radius=2, fill=1, stroke=0
        )

        # Calculate milestone positions
        padding = 0.5 * inch
        usable_width = self.timeline_width - 2 * padding
        spacing = usable_width / (n - 1) if n > 1 else 0

        for i, milestone in enumerate(self.milestones):
            x = padding + i * spacing
            completed = milestone.get("completed", False)
            is_current = milestone.get("current", False)

            # Draw progress bar up to completed milestones
            if completed and i > 0:
                prev_x = padding + (i - 1) * spacing
                canvas.setFillColor(BRAND_COLORS.BRAND_BLUE)
                canvas.roundRect(
                    prev_x, bar_y - bar_height / 2,
                    spacing, bar_height,
                    radius=2, fill=1, stroke=0
                )

            # Draw milestone marker
            marker_radius = 8 if is_current else 6
            if completed:
                canvas.setFillColor(BRAND_COLORS.BRAND_BLUE)
            elif is_current:
                canvas.setFillColor(BRAND_COLORS.CONTRAST_ORANGE)
            else:
                canvas.setFillColor(BRAND_COLORS.MUTED_GRAY)

            canvas.circle(x, bar_y, marker_radius, fill=1, stroke=0)

            # Inner circle for current milestone
            if is_current:
                canvas.setFillColor(BRAND_COLORS.WHITE)
                canvas.circle(x, bar_y, marker_radius - 3, fill=1, stroke=0)

            # Draw label above
            canvas.setFillColor(BRAND_COLORS.DARK_GRAY)
            font = Typography.BOLD_FONT if (completed or is_current) else Typography.PRIMARY_FONT
            canvas.setFont(font, 8)
            label = milestone.get("label", "")
            canvas.drawCentredString(x, bar_y + 18, label)

            # Draw date below
            canvas.setFillColor(BRAND_COLORS.MEDIUM_GRAY)
            canvas.setFont(Typography.PRIMARY_FONT, 7)
            date = milestone.get("date", "")
            canvas.drawCentredString(x, bar_y - 22, date)


class SectionDivider(Flowable):
    """
    A branded section divider with optional title.
    """

    def __init__(
        self,
        title: str = None,
        width: float = 6.5 * inch,
        style: str = "line",
    ):
        """
        Args:
            title: Optional section title
            width: Divider width
            style: 'line', 'gradient', or 'dots'
        """
        super().__init__()
        self.title = title
        self.divider_width = width
        self.style = style
        self.width = width
        self.height = 30 if title else 12

    def draw(self):
        canvas = self.canv

        if self.style == "line":
            # Simple line with brand accent
            y = self.height / 2
            canvas.setStrokeColor(BRAND_COLORS.BRAND_BLUE)
            canvas.setLineWidth(2)
            canvas.line(0, y, self.divider_width * 0.15, y)

            if self.title:
                canvas.setFillColor(BRAND_COLORS.DARK_GRAY)
                canvas.setFont(Typography.BOLD_FONT, 12)
                canvas.drawString(self.divider_width * 0.15 + 10, y - 4, self.title)

        elif self.style == "gradient":
            # Gradient fade line
            y = self.height / 2
            steps = 20
            step_width = self.divider_width / steps
            for i in range(steps):
                alpha = 1 - (i / steps)
                canvas.setStrokeColor(BRAND_COLORS.BRAND_BLUE)
                canvas.setLineWidth(2)
                canvas.setStrokeAlpha(alpha)
                canvas.line(i * step_width, y, (i + 1) * step_width, y)
            canvas.setStrokeAlpha(1)  # Reset

        elif self.style == "dots":
            # Dotted pattern
            y = self.height / 2
            dot_spacing = 8
            num_dots = int(self.divider_width * 0.3 / dot_spacing)
            canvas.setFillColor(BRAND_COLORS.BRAND_BLUE)
            for i in range(num_dots):
                canvas.circle(i * dot_spacing + 2, y, 2, fill=1, stroke=0)

            if self.title:
                canvas.setFillColor(BRAND_COLORS.DARK_GRAY)
                canvas.setFont(Typography.BOLD_FONT, 12)
                canvas.drawString(num_dots * dot_spacing + 15, y - 4, self.title)


class FigurePlaceholder(Flowable):
    """
    A placeholder for figures with brand-styled border and caption area.
    """

    def __init__(
        self,
        width: float = 5 * inch,
        height: float = 3 * inch,
        caption: str = None,
        figure_id: str = None,
    ):
        super().__init__()
        self.fig_width = width
        self.fig_height = height
        self.caption = caption
        self.figure_id = figure_id
        self.width = width
        caption_height = 20 if caption else 0
        self.height = height + caption_height

    def draw(self):
        canvas = self.canv

        # Draw placeholder box
        canvas.setStrokeColor(BRAND_COLORS.LIGHT_GRAY)
        canvas.setLineWidth(1)
        canvas.setDash([4, 4])
        caption_offset = 20 if self.caption else 0
        canvas.rect(0, caption_offset, self.fig_width, self.fig_height, fill=0, stroke=1)
        canvas.setDash([])

        # Draw "Figure" text in center
        canvas.setFillColor(BRAND_COLORS.MUTED_GRAY)
        canvas.setFont(Typography.PRIMARY_FONT, 12)
        label = f"Figure {self.figure_id}" if self.figure_id else "Figure"
        canvas.drawCentredString(
            self.fig_width / 2,
            caption_offset + self.fig_height / 2,
            label
        )

        # Draw caption below
        if self.caption:
            canvas.setFillColor(BRAND_COLORS.DARK_GRAY)
            canvas.setFont(Typography.PRIMARY_FONT, 9)
            if self.figure_id:
                caption_text = f"Figure {self.figure_id}. {self.caption}"
            else:
                caption_text = self.caption
            canvas.drawString(0, 4, caption_text)
