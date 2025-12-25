# Scientific Brand Visual Identity & Figure Standards

**Version 4.0**

This document outlines the strict visual identity for **figures, charts, diagrams, and presentation slides** for scientific communication (manuscripts, grants, and conferences).

These rules prioritize scientific clarity, professional publication standards (e.g., *Nature, Science, Cell*), accessibility, and brand consistency. The core principle: **Neutrals are for default data structure; Brand Colors are for highlights and accents; Complementary colors are for scientific contrast.**

**Always follow the approved color palette, layout rules, and typography standards below.** These rules apply to **all visuals**, including when generating **plotting code** (Matplotlib, ggplot2, Plotly, etc.).

---
# Section 0: Logo & Brand Mark

> **Insert this section at the beginning of BRAND_COLORS_v4.md, before "## 1. Color Palettes"**

---

## 0. Logo & Brand Mark

The Oligon logo uses a stylized "O" with an orbital dot, representing precision targeting — central to the SeekR platform's mechanism. The icon integrates into the wordmark, where it serves as the "O" in "Oligon."

### Logo Variants

| Variant | Use Case | Dimensions |
|---------|----------|------------|
| Full Logo | Headers, presentations, documents | 622 × 263 viewBox |
| Icon Only | Favicons, app icons, small spaces | 500 × 375 viewBox |

### Color Versions

| Version | HEX | Background |
|---------|-----|------------|
| Brand Blue | `#2DB2E8` | White or light backgrounds |
| White | `#FFFFFF` | Dark backgrounds, photos |

> **Historical note:** Original logo files used `#00A3DA`. The SVGs below use the canonical brand blue `#2DB2E8` for consistency with the scientific figure palette.

### Usage Rules

1. **Publication figures:** Do NOT include logos — journals prohibit branding
2. **Presentations & posters:** Logo in header/footer only, not on data panels
3. **Grants:** Title page or header; never on figures
4. **Clear space:** Minimum margin equal to the height of the orbital dot
5. **Minimum size:** Full logo ≥80px width; Icon ≥16px

### Do Not

- Stretch, rotate, or distort
- Add shadows, gradients, or outlines
- Place Brand Blue on dark backgrounds
- Place White on light backgrounds
- Use the legacy color `#00A3DA`

---

### SVG Source: Full Logo — Brand Blue (`#2DB2E8`)

Use on white/light backgrounds.

```xml
<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0" y="0" width="622" height="263" viewBox="0, 0, 622, 263">
  <defs>
    <clipPath id="Clip_1">
      <path d="M0.06,0.598 L621.105,0.598 L621.105,262.94 L0.06,262.94 z"/>
    </clipPath>
    <clipPath id="Clip_2">
      <path d="M0.06,0.598 L621.105,0.598 L621.105,262.94 L0.06,262.94 z"/>
    </clipPath>
  </defs>
  <g id="Layer_1">
    <path d="M180.725,47.431 L196.105,47.431 L196.105,208.03 L180.725,208.03 z" fill="#2DB2E8"/>
    <g clip-path="url(#Clip_1)">
      <path d="M226.182,103.524 L241.565,103.524 L241.565,208.03 L226.182,208.03 z" fill="#2DB2E8"/>
      <path d="M357.375,174.778 L357.375,133.161 C348.327,119.816 334.528,113.475 320.05,113.475 C297.202,113.475 280.926,131.578 280.926,154.419 C280.926,175.455 297.202,194.455 320.05,194.455 C334.528,194.455 348.327,188.125 357.375,174.778 z M372.754,211.423 C372.754,242.867 351.72,263 320.729,263 C293.359,263 272.778,246.937 269.156,224.09 L284.988,224.09 C288.163,238.787 301.729,248.75 320.729,248.75 C342.445,248.75 357.152,234.5 357.152,211.423 L357.375,211.423 L357.375,193.098 C347.421,202.374 333.851,208.03 318.019,208.03 C288.163,208.03 265.314,183.601 265.314,154.419 C265.314,123.427 288.163,99.905 318.019,99.905 C333.851,99.905 347.421,105.562 357.375,114.834 L357.375,103.524 L372.754,103.524 L372.754,211.423" fill="#2DB2E8"/>
    </g>
    <path d="M488.11,155.781 C488.11,133.386 470.921,115.061 448.076,115.061 C425.228,115.061 408.037,133.386 408.037,155.781 C408.037,178.848 425.228,197.394 448.076,197.394 C470.921,197.394 488.11,178.848 488.11,155.781 z M503.489,155.781 C503.489,187.214 479.291,211.423 448.076,211.423 C416.631,211.423 392.424,187.214 392.424,155.781 C392.424,124.792 416.631,100.801 448.076,100.801 C479.291,100.801 503.489,124.792 503.489,155.781" fill="#2DB2E8"/>
    <g clip-path="url(#Clip_2)">
      <path d="M621.105,147.862 L621.105,208.03 L605.725,208.03 L605.725,148.532 C605.725,126.827 592.834,114.385 573.832,114.385 C560.484,114.385 546.921,121.396 537.868,133.841 L537.868,208.03 L522.489,208.03 L522.489,103.524 L537.868,103.524 L537.868,115.967 C547.588,106.004 561.162,100.131 576.543,100.131 C602.783,100.131 621.105,118.456 621.105,147.862" fill="#2DB2E8"/>
      <path d="M233.87,72.65 C225.963,72.65 219.539,66.221 219.539,58.315 C219.539,50.411 225.963,43.979 233.87,43.979 C241.777,43.979 248.209,50.411 248.209,58.315 C248.209,66.221 241.777,72.65 233.87,72.65 z M147.215,129.255 C147.215,165.826 118.515,195.915 81.705,195.915 C45.132,195.915 16.43,165.826 16.43,129.255 C16.43,92.688 45.132,62.602 81.705,62.602 C118.515,62.602 147.215,92.688 147.215,129.255 z M233.87,32.299 C230.061,32.299 226.441,33.128 223.178,34.607 C205.71,13.211 179.4,0.598 151.62,0.598 C118.074,0.598 87.076,19.248 70.96,48.064 C30.819,53.408 -0,87.62 -0,129.255 C-0,174.628 36.572,211.195 81.937,211.195 C127.308,211.195 163.879,174.628 163.879,129.255 C163.879,85.222 129.417,49.475 85.902,47.419 C100.656,26.244 125.207,12.882 151.62,12.882 C175.62,12.882 198.352,23.743 213.494,42.176 C209.971,46.611 207.857,52.221 207.857,58.315 C207.857,72.664 219.532,84.325 233.87,84.325 C248.221,84.325 259.893,72.664 259.893,58.315 C259.893,43.971 248.221,32.299 233.87,32.299" fill="#2DB2E8"/>
    </g>
  </g>
</svg>
```

---

### SVG Source: Icon Only — Brand Blue (`#2DB2E8`)

Use for favicons, small contexts on light backgrounds.

```xml
<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0" y="0" width="500" height="375" viewBox="0, 0, 500, 375">
  <g id="Layer_1">
    <path d="M436.683,132.783 C423.099,132.783 412.063,121.738 412.063,108.156 C412.063,94.577 423.099,83.527 436.683,83.527 C450.267,83.527 461.317,94.577 461.317,108.156 C461.317,121.738 450.267,132.783 436.683,132.783 z M287.813,230.028 C287.813,292.856 238.507,344.548 175.269,344.548 C112.437,344.548 63.128,292.856 63.128,230.028 C63.128,167.208 112.437,115.521 175.269,115.521 C238.507,115.521 287.813,167.208 287.813,230.028 z M436.683,63.461 C430.139,63.461 423.92,64.885 418.314,67.426 C388.305,30.669 343.105,9 295.38,9 C237.749,9 184.496,41.04 156.809,90.545 C87.848,99.726 34.902,158.501 34.902,230.028 C34.902,307.978 97.732,370.798 175.667,370.798 C253.613,370.798 316.441,307.978 316.441,230.028 C316.441,154.381 257.236,92.969 182.479,89.437 C207.826,53.059 250.004,30.103 295.38,30.103 C336.611,30.103 375.664,48.762 401.678,80.43 C395.625,88.049 391.993,97.687 391.993,108.156 C391.993,132.807 412.051,152.84 436.683,152.84 C461.337,152.84 481.39,132.807 481.39,108.156 C481.39,83.513 461.337,63.461 436.683,63.461" fill="#2DB2E8" id="Layer_1"/>
  </g>
</svg>
```

---

### SVG Source: Full Logo — White (`#FFFFFF`)

Use on dark backgrounds (website, dark slides, photo overlays).

```xml
<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0" y="0" width="622" height="263" viewBox="0, 0, 622, 263">
  <defs>
    <clipPath id="Clip_1">
      <path d="M0.06,0.598 L621.105,0.598 L621.105,262.94 L0.06,262.94 z"/>
    </clipPath>
    <clipPath id="Clip_2">
      <path d="M0.06,0.598 L621.105,0.598 L621.105,262.94 L0.06,262.94 z"/>
    </clipPath>
  </defs>
  <g id="Layer_1">
    <path d="M180.725,47.431 L196.105,47.431 L196.105,208.03 L180.725,208.03 z" fill="#FFFFFF"/>
    <g clip-path="url(#Clip_1)">
      <path d="M226.182,103.524 L241.565,103.524 L241.565,208.03 L226.182,208.03 z" fill="#FFFFFF"/>
      <path d="M357.375,174.778 L357.375,133.161 C348.327,119.816 334.528,113.475 320.05,113.475 C297.202,113.475 280.926,131.578 280.926,154.419 C280.926,175.455 297.202,194.455 320.05,194.455 C334.528,194.455 348.327,188.125 357.375,174.778 z M372.754,211.423 C372.754,242.867 351.72,263 320.729,263 C293.359,263 272.778,246.937 269.156,224.09 L284.988,224.09 C288.163,238.787 301.729,248.75 320.729,248.75 C342.445,248.75 357.152,234.5 357.152,211.423 L357.375,211.423 L357.375,193.098 C347.421,202.374 333.851,208.03 318.019,208.03 C288.163,208.03 265.314,183.601 265.314,154.419 C265.314,123.427 288.163,99.905 318.019,99.905 C333.851,99.905 347.421,105.562 357.375,114.834 L357.375,103.524 L372.754,103.524 L372.754,211.423" fill="#FFFFFF"/>
    </g>
    <path d="M488.11,155.781 C488.11,133.386 470.921,115.061 448.076,115.061 C425.228,115.061 408.037,133.386 408.037,155.781 C408.037,178.848 425.228,197.394 448.076,197.394 C470.921,197.394 488.11,178.848 488.11,155.781 z M503.489,155.781 C503.489,187.214 479.291,211.423 448.076,211.423 C416.631,211.423 392.424,187.214 392.424,155.781 C392.424,124.792 416.631,100.801 448.076,100.801 C479.291,100.801 503.489,124.792 503.489,155.781" fill="#FFFFFF"/>
    <g clip-path="url(#Clip_2)">
      <path d="M621.105,147.862 L621.105,208.03 L605.725,208.03 L605.725,148.532 C605.725,126.827 592.834,114.385 573.832,114.385 C560.484,114.385 546.921,121.396 537.868,133.841 L537.868,208.03 L522.489,208.03 L522.489,103.524 L537.868,103.524 L537.868,115.967 C547.588,106.004 561.162,100.131 576.543,100.131 C602.783,100.131 621.105,118.456 621.105,147.862" fill="#FFFFFF"/>
      <path d="M233.87,72.65 C225.963,72.65 219.539,66.221 219.539,58.315 C219.539,50.411 225.963,43.979 233.87,43.979 C241.777,43.979 248.209,50.411 248.209,58.315 C248.209,66.221 241.777,72.65 233.87,72.65 z M147.215,129.255 C147.215,165.826 118.515,195.915 81.705,195.915 C45.132,195.915 16.43,165.826 16.43,129.255 C16.43,92.688 45.132,62.602 81.705,62.602 C118.515,62.602 147.215,92.688 147.215,129.255 z M233.87,32.299 C230.061,32.299 226.441,33.128 223.178,34.607 C205.71,13.211 179.4,0.598 151.62,0.598 C118.074,0.598 87.076,19.248 70.96,48.064 C30.819,53.408 -0,87.62 -0,129.255 C-0,174.628 36.572,211.195 81.937,211.195 C127.308,211.195 163.879,174.628 163.879,129.255 C163.879,85.222 129.417,49.475 85.902,47.419 C100.656,26.244 125.207,12.882 151.62,12.882 C175.62,12.882 198.352,23.743 213.494,42.176 C209.971,46.611 207.857,52.221 207.857,58.315 C207.857,72.664 219.532,84.325 233.87,84.325 C248.221,84.325 259.893,72.664 259.893,58.315 C259.893,43.971 248.221,32.299 233.87,32.299" fill="#FFFFFF"/>
    </g>
  </g>
</svg>
```

---

### SVG Source: Icon Only — White (`#FFFFFF`)

Use on dark backgrounds.

```xml
<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0" y="0" width="500" height="375" viewBox="0, 0, 500, 375">
  <g id="Layer_1">
    <path d="M436.683,132.783 C423.099,132.783 412.063,121.738 412.063,108.156 C412.063,94.577 423.099,83.527 436.683,83.527 C450.267,83.527 461.317,94.577 461.317,108.156 C461.317,121.738 450.267,132.783 436.683,132.783 z M287.813,230.028 C287.813,292.856 238.507,344.548 175.269,344.548 C112.437,344.548 63.128,292.856 63.128,230.028 C63.128,167.208 112.437,115.521 175.269,115.521 C238.507,115.521 287.813,167.208 287.813,230.028 z M436.683,63.461 C430.139,63.461 423.92,64.885 418.314,67.426 C388.305,30.669 343.105,9 295.38,9 C237.749,9 184.496,41.04 156.809,90.545 C87.848,99.726 34.902,158.501 34.902,230.028 C34.902,307.978 97.732,370.798 175.667,370.798 C253.613,370.798 316.441,307.978 316.441,230.028 C316.441,154.381 257.236,92.969 182.479,89.437 C207.826,53.059 250.004,30.103 295.38,30.103 C336.611,30.103 375.664,48.762 401.678,80.43 C395.625,88.049 391.993,97.687 391.993,108.156 C391.993,132.807 412.051,152.84 436.683,152.84 C461.337,152.84 481.39,132.807 481.39,108.156 C481.39,83.513 461.337,63.461 436.683,63.461" fill="#FFFFFF" id="Layer_1"/>
  </g>
</svg>
```

---

## Quick Reference

| Logo | Color | HEX | Use On |
|------|-------|-----|--------|
| Full Logo | Brand Blue | `#2DB2E8` | White/light backgrounds |
| Full Logo | White | `#FFFFFF` | Dark backgrounds |
| Icon | Brand Blue | `#2DB2E8` | White/light backgrounds |
| Icon | White | `#FFFFFF` | Dark backgrounds |

---

## 1. Color Palettes (HEX + Role)

### Primary Brand Color (Highlights & Key Accents)

Reserved for the primary data series of interest, the experimental treatment group, or the main focal point of a figure. **Brand Blue should appear in no more than one or two elements per panel in publication figures.**

| Color | HEX | Role |
|-------|-----|------|
| Bright Blue | #2DB2E8 | Hero Color — primary highlight |

### Neutral Data Colors (The Default)

Use these for control groups, baseline data, secondary series, context, or when no specific highlight is needed. **Most data should be neutral; color is earned by importance.**

| Color | HEX | Role |
|-------|-----|------|
| Very Dark Gray | #222222 | Primary default data lines/points |
| Medium Gray | #666666 | Secondary data lines/points |
| Muted Gray | #999999 | Tertiary data (lightest for actual data) |
| Light Gray | #BDBDBD | Annotations, gridlines, de-emphasized points only |

> **Note:** Do not use #BDBDBD for primary data points or lines; it lacks sufficient contrast against white backgrounds, especially in print. Reserve it for gridlines, annotations, non-significant points (e.g., volcano plots), or reference elements only.

### Scientific Contrast Colors (Divergence & Comparison)

Use *only* when strong opposition is needed against the Brand Blue (e.g., "Up-regulated" vs. "Down-regulated," or "Mutant" vs. "Wild-type").

| Color | HEX | Role |
|-------|-----|------|
| Vermilion/Orange | #E8622D | Primary contrast to Brand Blue |
| Dark Warm | #7D250F | Extreme positive in heatmaps |

### Supporting Brand Blues (Limited Use)

Use sparingly and with clear intent. These are **not** interchangeable with the hero blue.

| Color | HEX | Role & When to Use |
|-------|-----|-------------------|
| Medium Blue | #158BBB | Additional categorical series *only* when neutrals + Brand Blue are insufficient. Never use simultaneously with Brand Blue in the same legend without clear semantic distinction. |
| Dark Teal | #0F5D7D | Reserved primarily for heatmap negative extremes. May serve as a rare secondary highlight in line/scatter plots when Brand Blue is already committed. Avoid combining with multiple other blues. |

### Background & Structure Colors

| Element | Color | HEX |
|---------|-------|-----|
| Figure Backgrounds | White ONLY | #FFFFFF |
| Axes, Ticks, Labels, Titles, Legend Text | Black | #000000 |
| Gridlines (if essential) | Thin light gray | #E5E5E5 |

---

## 2. Scenario-Specific Color Cycles

**Do not use default library color cycles.** Select the cycle that matches your scientific context:

### Cycle 1: Control vs. Treatment (Most Common)

Use when comparing an experimental condition against a baseline.

| Order | Color | HEX | Assigned To |
|-------|-------|-----|-------------|
| 1 | Dark Gray | #222222 | Control / Baseline |
| 2 | Brand Blue | #2DB2E8 | Treatment / Experimental |
| 3 | Medium Gray | #666666 | Secondary comparison (if needed) |

```python
CYCLE_TREATMENT_CONTROL = ["#222222", "#2DB2E8", "#666666"]
```

### Cycle 2: Neutrals Only (No Designated Highlight)

Use when all groups are peers and no single condition deserves emphasis.

| Order | Color | HEX | Assigned To |
|-------|-------|-----|-------------|
| 1 | Dark Gray | #222222 | Group A |
| 2 | Medium Gray | #666666 | Group B |
| 3 | Muted Gray | #999999 | Group C |

```python
CYCLE_NEUTRALS_ONLY = ["#222222", "#666666", "#999999"]
```

### Cycle 3: Opposing Effects (Blue vs. Orange)

Use when showing bidirectional changes (up/down, positive/negative, gain/loss).

| Order | Color | HEX | Assigned To |
|-------|-------|-----|-------------|
| 1 | Brand Blue | #2DB2E8 | Direction A (e.g., Down-regulated) |
| 2 | Contrast Orange | #E8622D | Direction B (e.g., Up-regulated) |
| 3 | Dark Gray | #222222 | Neutral / Control / Unchanged |

```python
CYCLE_OPPOSING = ["#2DB2E8", "#E8622D", "#222222"]
```

### Cycle 4: Multiple Categories (≤4 groups, use sparingly)

Use only when you must distinguish 4 categories and cannot restructure the figure.

| Order | Color | HEX | Marker Shape |
|-------|-------|-----|--------------|
| 1 | Dark Gray | #222222 | Circle (o) |
| 2 | Brand Blue | #2DB2E8 | Square (s) |
| 3 | Medium Gray | #666666 | Triangle (^) |
| 4 | Medium Blue | #158BBB | Diamond (D) |

```python
CYCLE_MULTI_CATEGORY = ["#222222", "#2DB2E8", "#666666", "#158BBB"]
```

> **Important:** When using Cycle 4, marker shapes or line styles are **mandatory** for accessibility. If you need more than 4 categories, redesign the figure using faceting or small multiples.

---

## 3. Accessibility & Colorblind Safety

### Core Requirements

1. **All figures must remain interpretable in grayscale.** Test by converting to grayscale before submission.

2. **Do not rely solely on color** to distinguish data series. Combine color with:
   - Line style (solid, dashed, dotted)
   - Marker shape (circle, square, triangle, diamond)
   - Direct labels or annotations

3. **Avoid similar-hue distinctions.** Do not use #2DB2E8 vs. #158BBB as the primary differentiator between two series—they are too similar for colorblind viewers and in grayscale. If both must appear, use shape/style as the primary encoding.

4. **The blue–orange pair is colorblind-safe.** The combination of #2DB2E8 and #E8622D plus neutral grays provides good discrimination for deuteranopia and protanopia (red-green color blindness, ~8% of males).

### Testing Tools

Before finalizing figures, verify discriminability:

- [Coblis Colorblind Simulator](https://www.color-blindness.com/coblis-color-blindness-simulator/)
- [Viz Palette](https://projects.susielu.com/viz-palette)
- Matplotlib: `colorspacious` package
- ImageJ/FIJI: Built-in colorblind simulation

### Contrast Ratios

| Element | Minimum Contrast vs. White |
|---------|---------------------------|
| Text | 4.5:1 |
| Data points/lines | 3:1 |

All approved colors (#222222, #666666, #999999, #2DB2E8, #E8622D) meet these thresholds. #BDBDBD does not meet the 3:1 threshold for data and should only be used for de-emphasized elements.

---

## 4. Global Scientific Principles

1. **White Backgrounds Always:** All figures, charts, and slides must have a pure white background (#FFFFFF).

2. **Black Text & Structure:** For publication figures, all axis lines, ticks, labels, panel titles, and legends must be solid black. (Colored titles are permissible only on slides).

3. **Data-Ink Ratio:** Maximize data visibility. Remove unnecessary borders, heavy fills, and distinct gridlines.

4. **Neutrals First:** Do not use Brand Blue (#2DB2E8) as the default color for *all* series. Most baseline data should be grayscale; Brand Blue highlights the most important comparison or effect. **Brand Blue should appear in no more than one or two elements per panel.**

5. **No Effects:** Avoid gradients, shadows, or 3D elements.

6. **Redundant Encoding:** Never rely on color alone to convey critical information (see Accessibility Standards).

---

## 5. Typography & Text Standards

These specific rules ensure readability at typical journal print sizes (single-column ~89mm or double-column ~183mm).

### Font Family

Use a clean, standard sans-serif font only.

- **Approved Fonts:** Arial, Helvetica, or DejaVu Sans
- **Do Not Use:** Calibri, Times New Roman, or system defaults

### Font Sizes (Print/Manuscript)

| Element | Size |
|---------|------|
| Panel Labels (A, B, C) | 9–10 pt, **bold** |
| Panel Titles/Headings | 8–9 pt |
| Axis Labels | 8 pt |
| Axis Tick Labels | 7–8 pt |
| Legend Text | 7–8 pt |
| Annotations | 7 pt |

### Panel Labels (Multi-Panel Figures)

- **Format:** Uppercase letters (**A**, **B**, **C**)
- **Style:** Bold, black text, 9–10 pt
- **Placement:** Top-left corner of each panel, aligned with the left edge of the y-axis

---

## 6. Output Resolution Standards

| Output Context | Resolution | File Format |
|----------------|------------|-------------|
| Print/Publication | 300 DPI minimum (600 DPI for line art) | TIFF, EPS, PDF |
| Screen/Presentation | 150 DPI | PNG, PDF |
| Web/Preprint | 150 DPI | PNG, SVG |

> **Vector formats (PDF, EPS, SVG) are preferred** for all line-based figures as they scale without quality loss.

---

## 7. Chart & Figure Design Standards

### Structure & Layout ("Despined")

Figures must use an "open" or "despined" layout common in high-impact journals.

- **Axes & Spines:** Only keep the **left** and **bottom** spines. **Remove top and right spines.**
- **Axis Lines:** Thin black lines (0.8 pt weight)
- **Gridlines:** Off by default. If essential for readability, use very thin light gray (#E5E5E5), 0.5 pt weight

### Aspect Ratio

| Chart Type | Recommended Ratio |
|------------|-------------------|
| Time Series / Line Charts | 4:3 (wider than tall) |
| Scatter Plots / Correlations | 1:1 (square) |
| Bar Charts | Context-dependent; avoid excessive width |
| Heatmaps | Determined by data dimensions |

### Legends

- **Placement:** Inside the plotting area in an empty region whenever possible
- **Style:** Minimalist, no surrounding frame (`frameon=False`)
- **Exception:** Use a very thin light gray frame only if legend overlaps data

---

## 8. Color Selection Decision Tree

```
START: How many data series/categories?
│
├─► 1 series (single condition)
│   └─► Use #222222 (Dark Gray) — no highlight needed
│
├─► 2 series
│   │
│   ├─► Treatment vs. Control?
│   │   └─► Cycle 1: #222222 (Control) + #2DB2E8 (Treatment)
│   │
│   └─► Opposing effects (Up vs. Down)?
│       └─► Cycle 3: #2DB2E8 + #E8622D
│
├─► 3 series
│   │
│   ├─► One highlighted condition?
│   │   └─► Cycle 1: #222222, #2DB2E8, #666666
│   │
│   ├─► All conditions equal weight?
│   │   └─► Cycle 2: #222222, #666666, #999999
│   │
│   └─► Two opposing + one neutral?
│       └─► Cycle 3: #2DB2E8, #E8622D, #222222
│
├─► 4 series
│   └─► Cycle 4: #222222, #2DB2E8, #666666, #158BBB
│   └─► MANDATORY: Add marker shapes for accessibility
│
└─► 5+ series
    └─► STOP: Redesign the figure
        • Split into multiple panels
        • Use faceting/small multiples
        • Group categories hierarchically
```

---

## 9. Specific Chart Guidance

### Line & Scatter Plots

- **Line width:** 1.0–1.5 pt for primary data; 0.75 pt for secondary
- **Lines:** Solid for primary data; dashed/dotted for secondary (accessibility redundancy)
- **Markers:** Clean, defined shapes; size 4–6 pt
- **Marker edges:** Avoid heavy outlines unless needed for overlap contrast

### Error Representation Standards

| Error Type | When to Use | Visual Style |
|------------|-------------|--------------|
| **SEM** (Standard Error of Mean) | Estimating precision of the mean | Default for most experimental comparisons |
| **SD** (Standard Deviation) | Showing data spread/variability | When variability itself is of interest |
| **95% CI** (Confidence Interval) | Statistical inference | Preferred for clinical/translational data |

**Visual encoding:**

- **Discrete points (bar charts, dot plots):** Thin error bars (0.75 pt), with or without caps (be consistent)
- **Continuous data (line plots):** Semi-transparent fill bands (20–30% opacity) without borders
- **Always state in figure legend:** "Error bars represent [SEM/SD/95% CI], n = X"

### Bar Charts

- **Use neutrals for most bars**; reserve Brand Blue (#2DB2E8) or Contrast Orange (#E8622D) for the bar(s) you want to emphasize
- Use solid fills based on the appropriate cycle
- **Do not** outline bars with black lines (reduces data-ink ratio)
- Consider dot plots or box plots as alternatives for small n

### Box Plots & Violin Plots

- Box/violin fill: 50% opacity of assigned color
- Median line: solid, same color at full opacity
- Outliers: same color, smaller marker size

### Heatmaps (Divergent Scales)

For data centered around zero (z-scores, log2 fold change):

| Value | Color | HEX |
|-------|-------|-----|
| Extreme Negative | Dark Teal | #0F5D7D |
| Moderate Negative | Bright Blue | #2DB2E8 |
| Zero/Neutral | White | #FFFFFF |
| Moderate Positive | Contrast Orange | #E8622D |
| Extreme Positive | Dark Warm | #7D250F |

**Implementation requirements:**

1. **Use perceptually uniform interpolation** — linear RGB blending creates artifacts
2. **Center the colormap at zero** — do not let automatic scaling shift the neutral point
3. **Consider symmetric limits** — if data ranges -3 to +5, use limits of -5 to +5
4. **Add a colorbar** — always include with tick marks at meaningful intervals

---

## 10. Canonical Plot Templates for Biology

These patterns cover common visualization needs in biological and biomedical research.

### Kaplan-Meier Survival Curves

**Context:** Comparing survival between treatment groups (common in preclinical oncology).

| Element | Color | Style |
|---------|-------|-------|
| Control group | #222222 | Solid line |
| Treatment group | #2DB2E8 | Solid line |
| Additional treatment | #E8622D | Solid line (if opposing effect expected) |
| Confidence bands | Same as line | 20% opacity fill, no border |
| Censored tick marks | #000000 | Short vertical ticks on curve |
| At-risk table | #000000 | Below x-axis, matching group colors for labels |

**Additional guidance:**

- Line width: 1.25–1.5 pt
- Include median survival lines (thin dashed gray) if medians are reached
- P-value and hazard ratio: place in upper right or lower left, 7 pt text
- X-axis: "Time (days)" or appropriate unit; Y-axis: "Survival probability" or "Percent survival"

### Volcano Plots

**Context:** Differential expression analysis showing fold change vs. significance.

| Element | Color | HEX |
|---------|-------|-----|
| Non-significant points | Light Gray | #BDBDBD |
| Significant up-regulated | Contrast Orange | #E8622D |
| Significant down-regulated | Brand Blue | #2DB2E8 |
| Threshold lines | Medium Gray | #666666 (dashed, 0.5 pt) |
| Labeled genes | Black text | #000000 (7 pt, with leader lines if needed) |

**Additional guidance:**

- Point size: 3–4 pt for non-significant, 5–6 pt for significant (optional size encoding)
- Alpha: 0.6–0.8 for non-significant points to reduce overplotting
- X-axis: "log₂(Fold Change)"; Y-axis: "-log₁₀(p-value)" or "-log₁₀(FDR)"
- Symmetric x-axis limits recommended

### Grouped Bar Charts (Treatment Comparisons)

**Context:** Comparing measurements across conditions and groups.

| Element | Color | When |
|---------|-------|------|
| Control bars | #222222 | Default/baseline condition |
| Treatment bars | #2DB2E8 | Experimental condition of interest |
| Secondary treatment | #666666 | Additional comparison (not highlighted) |
| Vehicle/negative control | #999999 | Reference condition |

**Additional guidance:**

- Group bars by biological condition (e.g., cell line), not by treatment
- Use neutrals for most bars; reserve Brand Blue for the key comparison
- Error bars: thin (0.75 pt), same color as bar or black
- Consider replacing with dot plots if n < 10

### Dose-Response Curves

**Context:** IC50/EC50 determination, drug sensitivity assays.

| Element | Color | Style |
|---------|-------|-------|
| Drug A (focus) | #2DB2E8 | Solid line, circle markers |
| Drug B (comparison) | #222222 | Dashed line, square markers |
| Vehicle control | #666666 | Dotted line (if shown as curve) |
| IC50 reference line | #999999 | Thin horizontal dashed line |

**Additional guidance:**

- X-axis: log scale concentration; Y-axis: "% Viability" or "% Response"
- Include 95% CI bands (20% opacity) for fitted curves
- Mark IC50 values with vertical droplines or annotations
- Error bars at each concentration: SEM with n stated

### Flow Cytometry / Population Comparisons

**Context:** Comparing cell populations or marker expression.

| Element | Color | When |
|---------|-------|------|
| Isotype/FMO control | #BDBDBD | Negative control (de-emphasized) |
| Untreated/baseline | #222222 | Reference population |
| Treatment condition | #2DB2E8 | Experimental condition |
| Secondary marker | #E8622D | If showing opposing populations |

**Additional guidance:**

- Histogram overlays: 50% opacity fills, no borders
- Order: controls behind, treatment in front
- Include gate boundaries as thin black lines
- MFI values: annotate directly on plot or in legend

---

## 11. Presentation Slide Rules (Exceptions)

While publication standards are preferred, presentation slides allow slight deviations for visibility.

| Element | Publication Standard | Slide Exception |
|---------|---------------------|-----------------|
| Titles | Black only | May use #0F5D7D or #158BBB |
| Font sizes | 7–9 pt | Scale up 2–3× for readability |
| Accent elements | Minimal | Brand Blue (#2DB2E8) for callouts, icons |
| Body text | Black | Black or #222222 |
| Background | White | White (avoid dark backgrounds) |

---

## 12. Code Implementation

### Matplotlib Complete Setup

```python
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

# =============================================================================
# BRAND COLOR DEFINITIONS
# =============================================================================

BRAND_COLORS = {
    # Primary highlight
    'brand_blue': '#2DB2E8',
    
    # Neutrals (for data)
    'dark_gray': '#222222',
    'medium_gray': '#666666',
    'muted_gray': '#999999',
    'light_gray': '#BDBDBD',  # annotations only
    
    # Contrast
    'contrast_orange': '#E8622D',
    'dark_warm': '#7D250F',
    
    # Supporting blues
    'medium_blue': '#158BBB',
    'dark_teal': '#0F5D7D',
    
    # Structure
    'black': '#000000',
    'white': '#FFFFFF',
    'gridline': '#E5E5E5',
}

# =============================================================================
# SCENARIO-SPECIFIC COLOR CYCLES
# =============================================================================

# Cycle 1: Control vs Treatment (most common)
CYCLE_TREATMENT_CONTROL = ['#222222', '#2DB2E8', '#666666']

# Cycle 2: Neutrals only (no designated highlight)
CYCLE_NEUTRALS_ONLY = ['#222222', '#666666', '#999999']

# Cycle 3: Opposing effects (blue vs orange)
CYCLE_OPPOSING = ['#2DB2E8', '#E8622D', '#222222']

# Cycle 4: Multiple categories (use sparingly, add shapes!)
CYCLE_MULTI_CATEGORY = ['#222222', '#2DB2E8', '#666666', '#158BBB']

# Volcano plot specific
VOLCANO_COLORS = {
    'nonsig': '#BDBDBD',
    'up': '#E8622D',
    'down': '#2DB2E8',
}

# =============================================================================
# RCPARAMS CONFIGURATION
# =============================================================================

def set_brand_style(cycle='treatment_control'):
    """
    Apply brand visual standards to matplotlib.
    
    Parameters
    ----------
    cycle : str
        Which color cycle to use as default:
        - 'treatment_control' (default)
        - 'neutrals_only'
        - 'opposing'
        - 'multi_category'
    """
    
    cycle_map = {
        'treatment_control': CYCLE_TREATMENT_CONTROL,
        'neutrals_only': CYCLE_NEUTRALS_ONLY,
        'opposing': CYCLE_OPPOSING,
        'multi_category': CYCLE_MULTI_CATEGORY,
    }
    
    selected_cycle = cycle_map.get(cycle, CYCLE_TREATMENT_CONTROL)
    
    plt.rcParams.update({
        # Figure
        'figure.facecolor': 'white',
        'figure.edgecolor': 'white',
        'figure.dpi': 150,
        'savefig.dpi': 300,
        'savefig.facecolor': 'white',
        'savefig.edgecolor': 'white',
        'savefig.bbox': 'tight',
        'savefig.pad_inches': 0.1,
        
        # Axes
        'axes.facecolor': 'white',
        'axes.edgecolor': 'black',
        'axes.linewidth': 0.8,
        'axes.grid': False,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.labelcolor': 'black',
        'axes.labelsize': 8,
        'axes.titlesize': 9,
        'axes.titleweight': 'normal',
        'axes.prop_cycle': plt.cycler(color=selected_cycle),
        
        # Ticks
        'xtick.labelsize': 7,
        'ytick.labelsize': 7,
        'xtick.color': 'black',
        'ytick.color': 'black',
        'xtick.direction': 'out',
        'ytick.direction': 'out',
        
        # Grid (off by default)
        'grid.color': '#E5E5E5',
        'grid.linewidth': 0.5,
        'grid.alpha': 1.0,
        
        # Legend
        'legend.fontsize': 7,
        'legend.frameon': False,
        'legend.loc': 'best',
        
        # Font
        'font.family': 'sans-serif',
        'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
        'font.size': 8,
        
        # Lines
        'lines.linewidth': 1.25,
        'lines.markersize': 5,
        
        # Patches (bars, etc.)
        'patch.edgecolor': 'none',
    })

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_divergent_cmap():
    """
    Create a perceptually uniform divergent colormap for heatmaps.
    Centered at white: dark teal (neg) -> brand blue -> white -> orange -> dark warm (pos)
    """
    from matplotlib.colors import LinearSegmentedColormap
    
    colors = [
        BRAND_COLORS['dark_teal'],
        BRAND_COLORS['brand_blue'],
        BRAND_COLORS['white'],
        BRAND_COLORS['contrast_orange'],
        BRAND_COLORS['dark_warm'],
    ]
    
    positions = [0.0, 0.25, 0.5, 0.75, 1.0]
    
    return LinearSegmentedColormap.from_list(
        'brand_divergent', 
        list(zip(positions, colors))
    )


def add_panel_label(ax, label, offset=(-0.12, 1.05)):
    """Add a panel label (A, B, C, etc.) to an axes."""
    ax.text(
        offset[0], offset[1], 
        label,
        transform=ax.transAxes,
        fontsize=10,
        fontweight='bold',
        va='top',
        ha='left',
        color='black'
    )


def add_error_band(ax, x, y, yerr, color, alpha=0.25, label=None):
    """Add a semi-transparent error band around a line."""
    if isinstance(yerr, tuple):
        lower, upper = y - yerr[0], y + yerr[1]
    else:
        lower, upper = y - yerr, y + yerr
    
    ax.fill_between(x, lower, upper, color=color, alpha=alpha, linewidth=0)
    line, = ax.plot(x, y, color=color, label=label)
    return line


def plot_volcano(ax, log2fc, pval, fc_thresh=1.0, p_thresh=0.05, 
                 gene_labels=None, n_labels=10):
    """
    Create a volcano plot with brand colors.
    
    Parameters
    ----------
    ax : matplotlib.axes.Axes
    log2fc : array-like
        Log2 fold change values
    pval : array-like
        P-values (will be -log10 transformed)
    fc_thresh : float
        Fold change threshold (absolute log2)
    p_thresh : float
        P-value threshold
    gene_labels : array-like, optional
        Gene names for labeling
    n_labels : int
        Number of top genes to label
    """
    neg_log_p = -np.log10(pval)
    
    # Classify points
    nonsig = (np.abs(log2fc) < fc_thresh) | (pval >= p_thresh)
    sig_up = (log2fc >= fc_thresh) & (pval < p_thresh)
    sig_down = (log2fc <= -fc_thresh) & (pval < p_thresh)
    
    # Plot
    ax.scatter(log2fc[nonsig], neg_log_p[nonsig], 
               c=VOLCANO_COLORS['nonsig'], s=12, alpha=0.6, label='NS')
    ax.scatter(log2fc[sig_up], neg_log_p[sig_up], 
               c=VOLCANO_COLORS['up'], s=20, alpha=0.8, label='Up')
    ax.scatter(log2fc[sig_down], neg_log_p[sig_down], 
               c=VOLCANO_COLORS['down'], s=20, alpha=0.8, label='Down')
    
    # Threshold lines
    ax.axhline(-np.log10(p_thresh), color='#666666', linestyle='--', linewidth=0.5)
    ax.axvline(-fc_thresh, color='#666666', linestyle='--', linewidth=0.5)
    ax.axvline(fc_thresh, color='#666666', linestyle='--', linewidth=0.5)
    
    ax.set_xlabel('log₂(Fold Change)')
    ax.set_ylabel('-log₁₀(p-value)')
    
    return ax

# =============================================================================
# EXAMPLE: KAPLAN-MEIER STYLE SURVIVAL PLOT
# =============================================================================

def plot_survival_example():
    """Example survival curve following brand standards."""
    set_brand_style('treatment_control')
    
    fig, ax = plt.subplots(figsize=(5, 3.75))
    
    # Simulated survival data
    time_ctrl = np.array([0, 5, 10, 15, 20, 25, 30, 35, 40])
    surv_ctrl = np.array([1.0, 0.95, 0.85, 0.70, 0.55, 0.40, 0.30, 0.22, 0.18])
    
    time_tx = np.array([0, 5, 10, 15, 20, 25, 30, 35, 40])
    surv_tx = np.array([1.0, 0.98, 0.94, 0.88, 0.80, 0.72, 0.65, 0.58, 0.52])
    
    # Plot with confidence bands
    ax.fill_between(time_ctrl, surv_ctrl - 0.08, surv_ctrl + 0.08,
                    color=BRAND_COLORS['dark_gray'], alpha=0.2)
    ax.step(time_ctrl, surv_ctrl, where='post', 
            color=BRAND_COLORS['dark_gray'], linewidth=1.5, label='Control')
    
    ax.fill_between(time_tx, surv_tx - 0.06, surv_tx + 0.06,
                    color=BRAND_COLORS['brand_blue'], alpha=0.2)
    ax.step(time_tx, surv_tx, where='post',
            color=BRAND_COLORS['brand_blue'], linewidth=1.5, label='Treatment')
    
    ax.set_xlabel('Time (days)')
    ax.set_ylabel('Survival probability')
    ax.set_ylim(0, 1.05)
    ax.legend(loc='lower left')
    add_panel_label(ax, 'A')
    
    # Add p-value annotation
    ax.text(0.95, 0.95, 'p = 0.003\nHR = 0.45', transform=ax.transAxes,
            ha='right', va='top', fontsize=7)
    
    plt.tight_layout()
    return fig

if __name__ == "__main__":
    fig = plot_survival_example()
    plt.savefig('survival_example.png', dpi=300)
    plt.show()
```

### ggplot2 Complete Setup (R)

```r
# =============================================================================
# BRAND COLOR DEFINITIONS
# =============================================================================

brand_colors <- list(
  brand_blue = "#2DB2E8",
  dark_gray = "#222222",
  medium_gray = "#666666",
  muted_gray = "#999999",
  light_gray = "#BDBDBD",
  contrast_orange = "#E8622D",
  dark_warm = "#7D250F",
  medium_blue = "#158BBB",
  dark_teal = "#0F5D7D",
  black = "#000000",
  white = "#FFFFFF",
  gridline = "#E5E5E5"
)

# =============================================================================
# SCENARIO-SPECIFIC SCALES
# =============================================================================

# Cycle 1: Treatment vs Control
scale_treatment_control <- c(
  "Control" = "#222222",
  "Treatment" = "#2DB2E8"
)

# Cycle 2: Neutrals only
scale_neutrals <- c("#222222", "#666666", "#999999")

# Cycle 3: Opposing effects
scale_opposing <- c(
  "Down" = "#2DB2E8",
  "Up" = "#E8622D",
  "NS" = "#222222"
)

# Cycle 4: Multiple categories
scale_multi <- c("#222222", "#2DB2E8", "#666666", "#158BBB")

# Volcano plot
scale_volcano <- c(
  "NS" = "#BDBDBD",
  "Up" = "#E8622D",
  "Down" = "#2DB2E8"
)

# =============================================================================
# BRAND THEME
# =============================================================================

theme_brand <- function(base_size = 8, base_family = "Arial") {
  theme_minimal(base_size = base_size, base_family = base_family) %+replace%
    theme(
      plot.background = element_rect(fill = "white", color = NA),
      panel.background = element_rect(fill = "white", color = NA),
      panel.grid.major = element_blank(),
      panel.grid.minor = element_blank(),
      axis.line = element_line(color = "black", linewidth = 0.8 / .pt),
      axis.ticks = element_line(color = "black", linewidth = 0.4 / .pt),
      axis.text = element_text(color = "black", size = 7),
      axis.title = element_text(color = "black", size = 8),
      plot.title = element_text(color = "black", size = 9, hjust = 0),
      legend.background = element_blank(),
      legend.key = element_blank(),
      legend.text = element_text(size = 7),
      legend.title = element_text(size = 8),
      strip.background = element_blank(),
      strip.text = element_text(color = "black", size = 8)
    )
}

# =============================================================================
# DIVERGENT SCALE FOR HEATMAPS
# =============================================================================

scale_fill_brand_divergent <- function(limits = NULL, ...) {
  scale_fill_gradientn(
    colors = c(
      brand_colors$dark_teal,
      brand_colors$brand_blue,
      brand_colors$white,
      brand_colors$contrast_orange,
      brand_colors$dark_warm
    ),
    values = scales::rescale(c(-1, -0.5, 0, 0.5, 1)),
    limits = limits,
    ...
  )
}

# =============================================================================
# EXAMPLE: VOLCANO PLOT
# =============================================================================

library(ggplot2)

# Simulated data
set.seed(42)
volcano_df <- data.frame(
  log2FC = rnorm(1000, 0, 1.5),
  pval = 10^(-runif(1000, 0, 5))
)
volcano_df$category <- with(volcano_df, ifelse(
  abs(log2FC) < 1 | pval > 0.05, "NS",
  ifelse(log2FC > 0, "Up", "Down")
))

ggplot(volcano_df, aes(x = log2FC, y = -log10(pval), color = category)) +
  geom_point(aes(size = category, alpha = category)) +
  scale_color_manual(values = scale_volcano) +
  scale_size_manual(values = c("NS" = 1, "Up" = 2, "Down" = 2)) +
  scale_alpha_manual(values = c("NS" = 0.5, "Up" = 0.8, "Down" = 0.8)) +
  geom_hline(yintercept = -log10(0.05), linetype = "dashed", 
             color = "#666666", linewidth = 0.3) +
  geom_vline(xintercept = c(-1, 1), linetype = "dashed", 
             color = "#666666", linewidth = 0.3) +
  labs(x = expression(log[2](Fold~Change)), 
       y = expression(-log[10](p-value))) +
  theme_brand() +
  theme(legend.position = "none")

ggsave("volcano_example.png", width = 4, height = 4, dpi = 300)
```

---

## 13. Quick Reference Card

### Essential Colors

```
HIGHLIGHT:     #2DB2E8  (Brand Blue)
CONTRAST:      #E8622D  (Orange)
NEUTRAL 1:     #222222  (Dark Gray)
NEUTRAL 2:     #666666  (Medium Gray)
NEUTRAL 3:     #999999  (Muted Gray)
ANNOTATION:    #BDBDBD  (Light Gray - NOT for data)
```

### Cycle Quick Reference

| Scenario | Colors (in order) |
|----------|-------------------|
| Control vs Treatment | #222222, #2DB2E8 |
| Neutrals only | #222222, #666666, #999999 |
| Opposing effects | #2DB2E8, #E8622D, #222222 |
| 4 categories | #222222, #2DB2E8, #666666, #158BBB + shapes |

### Pre-Flight Checklist

Before submitting any figure:

- [ ] White background (#FFFFFF)
- [ ] Black text and axis lines (#000000)
- [ ] Top and right spines removed
- [ ] Correct color cycle selected for scientific context
- [ ] Brand Blue limited to 1–2 elements per panel
- [ ] Colors match brand palette (no library defaults)
- [ ] Redundant encoding present (shapes/styles with color)
- [ ] Tested in grayscale
- [ ] Colorblind simulation checked
- [ ] Error bars labeled in legend (SEM/SD/95% CI, n = ?)
- [ ] Font is Arial/Helvetica, 7–9 pt range
- [ ] Resolution ≥300 DPI for print
- [ ] Panel labels (A, B, C) bold, 9–10 pt, top-left aligned

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | — | Initial release |
| 2.0 | — | Shifted to neutrals-first philosophy |
| 3.0 | — | Added accessibility standards, expanded code templates, error bar guidance, decision tree |
| 4.0 | — | Scenario-specific color cycles, canonical bio-plot templates (K-M, volcano, dose-response, flow), clarified supporting blue roles, grayscale testing requirement, enhanced bar chart guidance |

---

*Document maintained for scientific figure standardization. For questions or proposed amendments, contact the visual standards committee.*
