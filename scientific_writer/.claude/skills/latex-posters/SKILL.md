---
name: latex-posters
description: "Create professional research posters in LaTeX using beamerposter, tikzposter, or baposter. Support for conference presentations, academic posters, and scientific communication. Includes layout design, color schemes, multi-column formats, figure integration, and poster-specific best practices for visual communication."
allowed-tools: [Read, Write, Edit, Bash]
---

# LaTeX Research Posters

## Overview

Research posters are a critical medium for scientific communication at conferences, symposia, and academic events. This skill provides comprehensive guidance for creating professional, visually appealing research posters using LaTeX packages. Generate publication-quality posters with proper layout, typography, color schemes, and visual hierarchy.

## When to Use This Skill

This skill should be used when:
- Creating research posters for conferences, symposia, or poster sessions
- Designing academic posters for university events or thesis defenses
- Preparing visual summaries of research for public engagement
- Converting scientific papers into poster format
- Creating template posters for research groups or departments
- Designing posters that comply with specific conference size requirements (A0, A1, 36×48", etc.)
- Building posters with complex multi-column layouts
- Integrating figures, tables, equations, and citations in poster format

## AI-Powered Visual Element Generation

**STANDARD WORKFLOW: Generate ALL major visual elements using AI before creating the LaTeX poster.**

This is the recommended approach for creating visually compelling posters:
1. Plan all visual elements needed (title, intro, methods, results, conclusions)
2. Generate each element using scientific-schematics or Nano Banana Pro
3. Assemble generated images in the LaTeX template
4. Add text content around the visuals

**Target: 60-70% of poster area should be AI-generated visuals, 30-40% text.**

---

### CRITICAL: Poster-Size Font Requirements

**⚠️ ALL text within AI-generated visualizations MUST be poster-readable.**

When generating graphics for posters, you MUST include font size specifications in EVERY prompt. Poster graphics are viewed from 4-6 feet away, so text must be LARGE.

**⚠️ COMMON PROBLEM: Content Overflow and Density**

The #1 issue with AI-generated poster graphics is **TOO MUCH CONTENT**. This causes:
- Text overflow beyond boundaries
- Unreadable small fonts
- Cluttered, overwhelming visuals
- Poor white space usage

**SOLUTION: Generate SIMPLE graphics with MINIMAL content.**

**Required prompt additions for poster graphics:**

```
POSTER FORMAT REQUIREMENTS:
- MAXIMUM 3-5 elements per graphic (NOT 10+)
- MAXIMUM 10-15 words total per graphic
- ALL text must be VERY LARGE and bold (readable from 6 feet away)
- Title text: minimum 72pt equivalent, bold
- Key metrics/numbers: minimum 60pt equivalent, bold  
- Labels and captions: minimum 36pt equivalent
- Use high contrast (dark text on light background or vice versa)
- GENEROUS white space (40-50% of graphic should be empty)
- Large icons and graphics with thick lines
- ONE main message per graphic
```

**Content limits per graphic type:**
| Graphic Type | Max Elements | Max Words | Example |
|--------------|--------------|-----------|---------|
| Flowchart | 4-5 boxes | 15 words | "DATA → PROCESS → MODEL → OUTPUT" |
| Key findings | 3 items | 12 words | "95% Accuracy, 2X Faster, Clinical Ready" |
| Comparison chart | 3-4 bars | 10 words | "Method A: 70%, Method B: 85%, Ours: 95%" |
| Diagram | 3-5 components | 15 words | Simple architecture with labeled parts |

**Example - WRONG (too much content, text too small):**
```bash
# BAD - too complex, too many elements, no size specs
python scripts/generate_schematic.py "Infographic showing machine learning pipeline with data collection, preprocessing, feature extraction, model training, validation, hyperparameter tuning, testing, deployment, monitoring, and feedback loops. Include accuracy metrics, performance graphs, comparison tables, and technical specifications." -o figures/pipeline.png
# Result: Cluttered graphic with tiny unreadable text, overflow issues
```

**Example - CORRECT (simple, poster-appropriate):**
```bash
# GOOD - minimal content, explicit size requirements, generous spacing
python scripts/generate_schematic.py "POSTER FORMAT for A0. SIMPLE flowchart with ONLY 4 boxes: DATA → MODEL → PREDICT → RESULT. Each box label in GIANT bold text (80pt+). Thick arrows between boxes. GENEROUS white space (50% empty). High contrast. Maximum 4 words per box. Readable from 8 feet." -o figures/pipeline.png
# Result: Clean, readable graphic with large text
```

**Example - WRONG (key findings too complex):**
```bash
# BAD - too many items, too much detail
python scripts/generate_schematic.py "Key findings showing 8 metrics: accuracy 95%, precision 92%, recall 94%, F1 0.93, AUC 0.97, training time 2.3 hours, inference 50ms, model size 145MB with comparison to 5 baseline methods" -o figures/findings.png
# Result: Cramped graphic with tiny numbers
```

**Example - CORRECT (key findings simple):**
```bash
# GOOD - only 3 key items, giant numbers
python scripts/generate_schematic.py "POSTER FORMAT for A0. KEY FINDINGS with ONLY 3 large cards. Card 1: '95%' in GIANT text (120pt) with 'ACCURACY' below (48pt). Card 2: '2X' in GIANT text with 'FASTER' below. Card 3: checkmark icon with 'VALIDATED' in large text. 50% white space. High contrast colors. NO other text or details." -o figures/findings.png
# Result: Bold, readable impact statement
```

**Font size reference for poster prompts:**
| Element | Minimum Size | Prompt Keywords |
|---------|--------------|-----------------|
| Main numbers/metrics | 72pt+ | "huge", "very large", "giant", "poster-size" |
| Section titles | 60pt+ | "large bold", "prominent" |
| Labels/captions | 36pt+ | "readable from 6 feet", "clear labels" |
| Body text | 24pt+ | "poster-readable", "large text" |

**Always include in prompts:**
- "POSTER FORMAT" or "for A0 poster" or "readable from 6 feet"
- "VERY LARGE TEXT" or "huge bold fonts"
- Specific text that should appear (so it's baked into the image)
- "minimal text, maximum impact"
- "high contrast" for readability

---

### Step 1: Plan Your Poster Elements

Before creating the LaTeX poster, identify all visual elements needed:

1. **Title Block** - Stylized title with institutional branding (optional - can be LaTeX text)
2. **Introduction Graphic** - Conceptual overview or problem statement visual
3. **Methods Diagram** - Workflow, pipeline, or experimental design
4. **Results Figures** - Data visualizations, charts, key findings (2-4 figures)
5. **Conclusion Graphic** - Summary visual or take-home message
6. **Supplementary Icons** - Icons for sections, QR codes, logos

### Step 2: Generate Each Element

Use the appropriate tool for each element type:

**For Schematics and Diagrams (scientific-schematics):**
```bash
# Create figures directory
mkdir -p figures

# Methods flowchart - SIMPLE, 4 steps only
python scripts/generate_schematic.py "POSTER FORMAT for A0. SIMPLE flowchart with ONLY 4 boxes: DATA → PROCESS → MODEL → RESULTS. Each label in GIANT bold text (80pt+). Thick arrows. 50% white space. NO additional details or sub-steps. Readable from 8 feet." -o figures/methods_flowchart.png

# System architecture - SIMPLE, 4 components only
python scripts/generate_schematic.py "POSTER FORMAT for A0. SIMPLE architecture diagram with ONLY 4 components: INPUT → NETWORK → PROCESSING → OUTPUT. GIANT labels (80pt+). Thick lines. 50% white space. NO layer details. Readable from 8 feet." -o figures/architecture.png

# Conceptual framework - SIMPLE, 3 elements only
python scripts/generate_schematic.py "POSTER FORMAT for A0. SIMPLE diagram with ONLY 3 elements: A → B → C. Each label in GIANT bold text (80pt+). Thick arrows. 50% white space. NO additional text. Readable from 8 feet." -o figures/concept_framework.png

# Experimental design - SIMPLE, 3 groups only
python scripts/generate_schematic.py "POSTER FORMAT for A0. SIMPLE design diagram: CONTROL vs TREATMENT with arrow to OUTCOMES. ONLY 3 boxes total. GIANT labels (80pt+). 50% white space. NO detailed sub-groups. Readable from 8 feet." -o figures/experimental_design.png
```

**For Stylized Blocks and Graphics (Nano Banana Pro):**
```bash
# Title block - SIMPLE
python scripts/generate_schematic.py "POSTER FORMAT for A0. Title block: 'ML FOR DRUG DISCOVERY' in HUGE bold text (120pt+). Dark blue background. ONE subtle icon. NO other text. 40% white space. Readable from 15 feet." -o figures/title_block.png

# Introduction visual - SIMPLE, 3 elements only
python scripts/generate_schematic.py "POSTER FORMAT for A0. SIMPLE problem visual with ONLY 3 icons: drug icon, arrow, target icon. ONE label per icon (80pt+). 50% white space. NO detailed text. Readable from 8 feet." -o figures/intro_visual.png

# Conclusion/summary - ONLY 3 items, GIANT numbers
python scripts/generate_schematic.py "POSTER FORMAT for A0. KEY FINDINGS with EXACTLY 3 cards only. Card 1: '95%' (150pt font) with 'ACCURACY' (60pt). Card 2: '2X' (150pt) with 'FASTER' (60pt). Card 3: checkmark icon with 'READY' (60pt). 50% white space. NO other text. Readable from 10 feet." -o figures/conclusions_graphic.png

# Background visual - SIMPLE, 3 icons only
python scripts/generate_schematic.py "POSTER FORMAT for A0. SIMPLE visual with ONLY 3 large icons in a row: problem icon → challenge icon → impact icon. ONE word label each (80pt+). 50% white space. NO detailed text. Readable from 8 feet." -o figures/background_visual.png
```

**For Data Visualizations - SIMPLE, 3 bars max:**
```bash
# SIMPLE chart with ONLY 3 bars, GIANT labels
python scripts/generate_schematic.py "POSTER FORMAT for A0. SIMPLE bar chart with ONLY 3 bars: BASELINE (70%), EXISTING (85%), OURS (95%). GIANT percentage labels ON the bars (100pt+). NO axis labels, NO legend, NO gridlines. Our bar highlighted in different color. 40% white space. Readable from 8 feet." -o figures/comparison_chart.png
```

### Step 3: Assemble in LaTeX Template

Include all generated figures in your poster template:

**tikzposter example:**
```latex
\documentclass[25pt, a0paper, portrait]{tikzposter}

\begin{document}

\maketitle

\begin{columns}
\column{0.5}

\block{Introduction}{
  \centering
  \includegraphics[width=0.85\linewidth]{figures/intro_visual.png}
  
  \vspace{0.5em}
  Brief context text here (2-3 sentences max).
}

\block{Methods}{
  \centering
  \includegraphics[width=0.9\linewidth]{figures/methods_flowchart.png}
}

\column{0.5}

\block{Results}{
  \begin{minipage}{0.48\linewidth}
    \centering
    \includegraphics[width=\linewidth]{figures/result_1.png}
  \end{minipage}
  \hfill
  \begin{minipage}{0.48\linewidth}
    \centering
    \includegraphics[width=\linewidth]{figures/result_2.png}
  \end{minipage}
  
  \vspace{0.5em}
  Key findings in 3-4 bullet points.
}

\block{Conclusions}{
  \centering
  \includegraphics[width=0.8\linewidth]{figures/conclusions_graphic.png}
}

\end{columns}

\end{document}
```

**baposter example:**
```latex
\headerbox{Methods}{name=methods,column=0,row=0}{
  \centering
  \includegraphics[width=0.95\linewidth]{figures/methods_flowchart.png}
}

\headerbox{Results}{name=results,column=1,row=0}{
  \includegraphics[width=\linewidth]{figures/comparison_chart.png}
  \vspace{0.3em}
  
  Key finding: Our method achieves 92% accuracy.
}
```

### Example: Complete Poster Generation Workflow

**Remember: SIMPLE graphics with MINIMAL content. Each graphic = ONE message.**

```bash
# 1. Create figures directory
mkdir -p figures

# 2. Generate SIMPLE visual elements - MAXIMUM 5 elements per graphic

# Problem statement - ONLY 3 icons
python scripts/generate_schematic.py "POSTER FORMAT for A0. SIMPLE visual with 3 icons only: PATIENT icon → DELAY icon → RISK icon. ONE word label each (80pt+). 50% white space. Readable from 8 feet." -o figures/problem.png

# Methods pipeline - ONLY 4 steps
python scripts/generate_schematic.py "POSTER FORMAT for A0. SIMPLE flowchart with ONLY 4 boxes: IMAGES → PROCESS → MODEL → DIAGNOSIS. GIANT labels (100pt+). Thick arrows. 50% white space. NO sub-steps. Readable from 8 feet." -o figures/methods.png

# Architecture diagram - ONLY 4 components  
python scripts/generate_schematic.py "POSTER FORMAT for A0. SIMPLE architecture with ONLY 4 blocks: INPUT → CNN → DENSE → OUTPUT. GIANT labels (80pt+). Thick lines. 50% white space. NO layer details. Readable from 8 feet." -o figures/architecture.png

# Results - ONLY 3 bars
python scripts/generate_schematic.py "POSTER FORMAT for A0. SIMPLE bar chart with ONLY 3 bars: 82% BASELINE, 88% EXISTING, 95% OURS (highlighted). GIANT percentages ON bars (120pt+). NO axis, NO legend. 40% white space. Readable from 10 feet." -o figures/results.png

# Key findings - ONLY 3 items with GIANT numbers
python scripts/generate_schematic.py "POSTER FORMAT for A0. EXACTLY 3 cards only: '95%' (150pt) 'ACCURACY' (60pt), '2X' (150pt) 'FASTER' (60pt), checkmark 'VALIDATED' (60pt). 50% white space. NO other text. Readable from 10 feet." -o figures/conclusions.png

# 3. Compile LaTeX poster with all figures
pdflatex poster.tex
```

**If graphics still overflow or have small text:**
1. Reduce number of elements further (try 3 instead of 5)
2. Add "EVEN SIMPLER" or "ONLY 3 elements" to prompt
3. Increase font size requirements (try 150pt+ for key numbers)
4. Add "60% white space" instead of 50%

### Visual Element Guidelines

**⚠️ CRITICAL: Each graphic should have ONE main message and MINIMAL content.**

**Content limits - NEVER exceed these:**
- **Maximum 5 boxes/elements** per flowchart
- **Maximum 3-4 bars** per chart  
- **Maximum 3 key findings** per infographic
- **Maximum 15 words** total per graphic
- **50% white space** minimum

**For each poster section, generate SIMPLE visuals with POSTER FORMAT:**

| Section | Max Elements | Example Prompt |
|---------|--------------|----------------|
| **Introduction** | 3-4 icons | "POSTER FORMAT for A0: SIMPLE problem visual with 3 large icons and 3 word labels. 50% white space." |
| **Methods** | 4-5 boxes max | "POSTER FORMAT for A0: SIMPLE flowchart with ONLY 4 steps: A → B → C → D. GIANT labels (80pt+). 50% white space." |
| **Results** | 3-4 bars max | "POSTER FORMAT for A0: SIMPLE bar chart with ONLY 3 bars. GIANT percentages (100pt+). NO legend, direct labels." |
| **Conclusions** | 3 items only | "POSTER FORMAT for A0: ONLY 3 key findings. GIANT numbers (120pt+). One word labels. 50% white space." |

**MANDATORY prompt elements for poster graphics:**
1. **"POSTER FORMAT for A0"** - size indicator
2. **"SIMPLE"** or **"ONLY X elements"** - content limit
3. **"GIANT (80pt+)"** or **"HUGE (100pt+)"** - font sizes
4. **"50% white space"** - prevent crowding
5. **"readable from 6-8 feet"** - viewing distance
6. **Exact text** that should appear (keep minimal!)

**ANTI-PATTERNS TO AVOID:**
- ❌ "Show all the steps in the methodology" → Too many elements
- ❌ "Include accuracy, precision, recall, F1, AUC" → Too many metrics
- ❌ "Comparison of 6 different methods" → Too many comparisons
- ❌ "Detailed architecture with all layers" → Too complex

**CORRECT PATTERNS:**
- ✅ "ONLY 4 main steps" → Limited elements
- ✅ "ONLY the top 3 metrics" → Focused content
- ✅ "Compare ONLY our method vs baseline" → Simple comparison
- ✅ "HIGH-LEVEL architecture with 4 components" → Simplified view

---

## Scientific Schematics Integration

For detailed guidance on creating schematics, refer to the **scientific-schematics** skill documentation.

**Key capabilities:**
- Nano Banana Pro automatically generates, reviews, and refines diagrams
- Creates publication-quality images with proper formatting
- Ensures accessibility (colorblind-friendly, high contrast)
- Supports iterative refinement for complex diagrams

---

## Core Capabilities

### 1. LaTeX Poster Packages

Support for three major LaTeX poster packages, each with distinct advantages. For detailed comparison and package-specific guidance, refer to `references/latex_poster_packages.md`.

**beamerposter**:
- Extension of the Beamer presentation class
- Familiar syntax for Beamer users
- Excellent theme support and customization
- Best for: Traditional academic posters, institutional branding

**tikzposter**:
- Modern, flexible design with TikZ integration
- Built-in color themes and layout templates
- Extensive customization through TikZ commands
- Best for: Colorful, modern designs, custom graphics

**baposter**:
- Box-based layout system
- Automatic spacing and positioning
- Professional-looking default styles
- Best for: Multi-column layouts, consistent spacing

### 2. Poster Layout and Structure

Create effective poster layouts following visual communication principles. For comprehensive layout guidance, refer to `references/poster_layout_design.md`.

**Common Poster Sections**:
- **Header/Title**: Title, authors, affiliations, logos
- **Introduction/Background**: Research context and motivation
- **Methods/Approach**: Methodology and experimental design
- **Results**: Key findings with figures and data visualizations
- **Conclusions**: Main takeaways and implications
- **References**: Key citations (typically abbreviated)
- **Acknowledgments**: Funding, collaborators, institutions

**Layout Strategies**:
- **Column-based layouts**: 2-column, 3-column, or 4-column grids
- **Block-based layouts**: Flexible arrangement of content blocks
- **Z-pattern flow**: Guide readers through content logically
- **Visual hierarchy**: Use size, color, and spacing to emphasize key points

### 3. Design Principles for Research Posters

Apply evidence-based design principles for maximum impact. For detailed design guidance, refer to `references/poster_design_principles.md`.

**Typography**:
- Title: 72-120pt for visibility from distance
- Section headers: 48-72pt
- Body text: 24-36pt minimum for readability from 4-6 feet
- Use sans-serif fonts (Arial, Helvetica, Calibri) for clarity
- Limit to 2-3 font families maximum

**Color and Contrast**:
- Use high-contrast color schemes for readability
- Institutional color palettes for branding
- Color-blind friendly palettes (avoid red-green combinations)
- White space is active space—don't overcrowd

**Visual Elements**:
- High-resolution figures (300 DPI minimum for print)
- Large, clear labels on all figures
- Consistent figure styling throughout
- Strategic use of icons and graphics
- Balance text with visual content (40-50% visual recommended)

**Content Guidelines**:
- **Less is more**: 300-800 words total recommended
- Bullet points over paragraphs for scannability
- Clear, concise messaging
- Self-explanatory figures with minimal text explanation
- QR codes for supplementary materials or online resources

### 4. Standard Poster Sizes

Support for international and conference-specific poster dimensions:

**International Standards**:
- A0 (841 × 1189 mm / 33.1 × 46.8 inches) - Most common European standard
- A1 (594 × 841 mm / 23.4 × 33.1 inches) - Smaller format
- A2 (420 × 594 mm / 16.5 × 23.4 inches) - Compact posters

**North American Standards**:
- 36 × 48 inches (914 × 1219 mm) - Common US conference size
- 42 × 56 inches (1067 × 1422 mm) - Large format
- 48 × 72 inches (1219 × 1829 mm) - Extra large

**Orientation**:
- Portrait (vertical) - Most common, traditional
- Landscape (horizontal) - Better for wide content, timelines

### 5. Package-Specific Templates

Provide ready-to-use templates for each major package. Templates available in `assets/` directory.

**beamerposter Templates**:
- `beamerposter_classic.tex` - Traditional academic style
- `beamerposter_modern.tex` - Clean, minimal design
- `beamerposter_colorful.tex` - Vibrant theme with blocks

**tikzposter Templates**:
- `tikzposter_default.tex` - Standard tikzposter layout
- `tikzposter_rays.tex` - Modern design with ray theme
- `tikzposter_wave.tex` - Professional wave-style theme

**baposter Templates**:
- `baposter_portrait.tex` - Classic portrait layout
- `baposter_landscape.tex` - Landscape multi-column
- `baposter_minimal.tex` - Minimalist design

### 6. Figure and Image Integration

Optimize visual content for poster presentations:

**Best Practices**:
- Use vector graphics (PDF, SVG) when possible for scalability
- Raster images: minimum 300 DPI at final print size
- Consistent image styling (borders, captions, sizes)
- Group related figures together
- Use subfigures for comparisons

**LaTeX Figure Commands**:
```latex
% Include graphics package
\usepackage{graphicx}

% Simple figure
\includegraphics[width=0.8\linewidth]{figure.pdf}

% Figure with caption in tikzposter
\block{Results}{
  \begin{tikzfigure}
    \includegraphics[width=0.9\linewidth]{results.png}
  \end{tikzfigure}
}

% Multiple subfigures
\usepackage{subcaption}
\begin{figure}
  \begin{subfigure}{0.48\linewidth}
    \includegraphics[width=\linewidth]{fig1.pdf}
    \caption{Condition A}
  \end{subfigure}
  \begin{subfigure}{0.48\linewidth}
    \includegraphics[width=\linewidth]{fig2.pdf}
    \caption{Condition B}
  \end{subfigure}
\end{figure}
```

### 7. Color Schemes and Themes

Provide professional color palettes for various contexts:

**Academic Institution Colors**:
- Match university or department branding
- Use official color codes (RGB, CMYK, or LaTeX color definitions)

**Scientific Color Palettes** (color-blind friendly):
- Viridis: Professional gradient from purple to yellow
- ColorBrewer: Research-tested palettes for data visualization
- IBM Color Blind Safe: Accessible corporate palette

**Package-Specific Theme Selection**:

**beamerposter**:
```latex
\usetheme{Berlin}
\usecolortheme{beaver}
```

**tikzposter**:
```latex
\usetheme{Rays}
\usecolorstyle{Denmark}
```

**baposter**:
```latex
\begin{poster}{
  background=plain,
  bgColorOne=white,
  headerColorOne=blue!70,
  textborder=rounded
}
```

### 8. Typography and Text Formatting

Ensure readability and visual appeal:

**Font Selection**:
```latex
% Sans-serif fonts recommended for posters
\usepackage{helvet}      % Helvetica
\usepackage{avant}       % Avant Garde
\usepackage{sfmath}      % Sans-serif math fonts

% Set default to sans-serif
\renewcommand{\familydefault}{\sfdefault}
```

**Text Sizing**:
```latex
% Adjust text sizes for visibility
\setbeamerfont{title}{size=\VeryHuge}
\setbeamerfont{author}{size=\Large}
\setbeamerfont{institute}{size=\normalsize}
```

**Emphasis and Highlighting**:
- Use bold for key terms: `\textbf{important}`
- Color highlights sparingly: `\textcolor{blue}{highlight}`
- Boxes for critical information
- Avoid italics (harder to read from distance)

### 9. QR Codes and Interactive Elements

Enhance poster interactivity for modern conferences:

**QR Code Integration**:
```latex
\usepackage{qrcode}

% Link to paper, code repository, or supplementary materials
\qrcode[height=2cm]{https://github.com/username/project}

% QR code with caption
\begin{center}
  \qrcode[height=3cm]{https://doi.org/10.1234/paper}\\
  \small Scan for full paper
\end{center}
```

**Digital Enhancements**:
- Link to GitHub repositories for code
- Link to video presentations or demos
- Link to interactive web visualizations
- Link to supplementary data or appendices

### 10. Compilation and Output

Generate high-quality PDF output for printing or digital display:

**Compilation Commands**:
```bash
# Basic compilation
pdflatex poster.tex

# With bibliography
pdflatex poster.tex
bibtex poster
pdflatex poster.tex
pdflatex poster.tex

# For beamer-based posters
lualatex poster.tex  # Better font support
xelatex poster.tex   # Unicode and modern fonts
```

**Ensuring Full Page Coverage**:

Posters should use the entire page without excessive margins. Configure packages correctly:

**beamerposter - Full Page Setup**:
```latex
\documentclass[final,t]{beamer}
\usepackage[size=a0,scale=1.4,orientation=portrait]{beamerposter}

% Remove default beamer margins
\setbeamersize{text margin left=0mm, text margin right=0mm}

% Use geometry for precise control
\usepackage[margin=10mm]{geometry}  % 10mm margins all around

% Remove navigation symbols
\setbeamertemplate{navigation symbols}{}

% Remove footline and headline if not needed
\setbeamertemplate{footline}{}
\setbeamertemplate{headline}{}
```

**tikzposter - Full Page Setup**:
```latex
\documentclass[
  25pt,                      % Font scaling
  a0paper,                   % Paper size
  portrait,                  % Orientation
  margin=10mm,               % Outer margins (minimal)
  innermargin=15mm,          % Space inside blocks
  blockverticalspace=15mm,   % Space between blocks
  colspace=15mm,             % Space between columns
  subcolspace=8mm            % Space between subcolumns
]{tikzposter}

% This ensures content fills the page
```

**baposter - Full Page Setup**:
```latex
\documentclass[a0paper,portrait,fontscale=0.285]{baposter}

\begin{poster}{
  grid=false,
  columns=3,
  colspacing=1.5em,          % Space between columns
  eyecatcher=true,
  background=plain,
  bgColorOne=white,
  borderColor=blue!50,
  headerheight=0.12\textheight,  % 12% for header
  textborder=roundedleft,
  headerborder=closed,
  boxheaderheight=2em        % Consistent box header heights
}
% Content here
\end{poster}
```

**Common Issues and Fixes**:

**Problem**: Large white margins around poster
```latex
% Fix for beamerposter
\setbeamersize{text margin left=5mm, text margin right=5mm}

% Fix for tikzposter
\documentclass[..., margin=5mm, innermargin=10mm]{tikzposter}

% Fix for baposter - adjust in document class
\documentclass[a0paper, margin=5mm]{baposter}
```

**Problem**: Content doesn't fill vertical space
```latex
% Use \vfill between sections to distribute space
\block{Introduction}{...}
\vfill
\block{Methods}{...}
\vfill
\block{Results}{...}

% Or manually adjust block spacing
\vspace{1cm}  % Add space between specific blocks
```

**Problem**: Poster extends beyond page boundaries
```latex
% Check total width calculation
% For 3 columns with spacing:
% Total = 3×columnwidth + 2×colspace + 2×margins
% Ensure this equals \paperwidth

% Debug by adding visible page boundary
\usepackage{eso-pic}
\AddToShipoutPictureBG{
  \AtPageLowerLeft{
    \put(0,0){\framebox(\LenToUnit{\paperwidth},\LenToUnit{\paperheight}){}}
  }
}
```

**Print Preparation**:
- Generate PDF/X-1a for professional printing
- Embed all fonts
- Convert colors to CMYK if required
- Check resolution of all images (minimum 300 DPI)
- Add bleed area if required by printer (usually 3-5mm)
- Verify page size matches requirements exactly

**Digital Display**:
- RGB color space for screen display
- Optimize file size for email/web
- Test readability on different screens

### 11. PDF Review and Quality Control

**CRITICAL**: Always review the generated PDF before printing or presenting. Use this systematic checklist:

**Step 1: Page Size Verification**
```bash
# Check PDF dimensions (should match poster size exactly)
pdfinfo poster.pdf | grep "Page size"

# Expected outputs:
# A0: 2384 x 3370 points (841 x 1189 mm)
# 36x48": 2592 x 3456 points
# A1: 1684 x 2384 points (594 x 841 mm)
```

**Step 2: Visual Inspection Checklist**

Open PDF at 100% zoom and check:

**Layout and Spacing**:
- [ ] Content fills entire page (no large white margins)
- [ ] Consistent spacing between columns
- [ ] Consistent spacing between blocks/sections
- [ ] All elements aligned properly (use ruler tool)
- [ ] No overlapping text or figures
- [ ] White space evenly distributed

**Typography**:
- [ ] Title clearly visible and large (72pt+)
- [ ] Section headers readable (48-72pt)
- [ ] Body text readable at 100% zoom (24-36pt minimum)
- [ ] No text cutoff or running off edges
- [ ] Consistent font usage throughout
- [ ] All special characters render correctly (symbols, Greek letters)

**Visual Elements**:
- [ ] All figures display correctly
- [ ] No pixelated or blurry images
- [ ] Figure captions present and readable
- [ ] Colors render as expected (not washed out or too dark)
- [ ] Logos display clearly
- [ ] QR codes visible and scannable

**Content Completeness**:
- [ ] Title and authors complete
- [ ] All sections present (Intro, Methods, Results, Conclusions)
- [ ] References included
- [ ] Contact information visible
- [ ] Acknowledgments (if applicable)
- [ ] No placeholder text remaining (Lorem ipsum, TODO, etc.)

**Technical Quality**:
- [ ] No LaTeX compilation warnings in important areas
- [ ] All citations resolved (no [?] marks)
- [ ] All cross-references working
- [ ] Page boundaries correct (no content cut off)

**Step 3: Reduced-Scale Print Test**

**Essential Pre-Printing Test**:
```bash
# Create reduced-size test print (25% of final size)
# This simulates viewing full poster from ~8-10 feet

# For A0 poster, print on A4 paper (24.7% scale)
# For 36x48" poster, print on letter paper (~25% scale)
```

**Print Test Checklist**:
- [ ] Title readable from 6 feet away
- [ ] Section headers readable from 4 feet away
- [ ] Body text readable from 2 feet away
- [ ] Figures clear and understandable
- [ ] Colors printed accurately
- [ ] No obvious design flaws

**Step 4: Digital Quality Checks**

**Font Embedding Verification**:
```bash
# Check that all fonts are embedded (required for printing)
pdffonts poster.pdf

# All fonts should show "yes" in "emb" column
# If any show "no", recompile with:
pdflatex -dEmbedAllFonts=true poster.tex
```

**Image Resolution Check**:
```bash
# Extract image information
pdfimages -list poster.pdf

# Check that all images are at least 300 DPI
# Formula: DPI = pixels / (inches in poster)
# For A0 width (33.1"): 300 DPI = 9930 pixels minimum
```

**File Size Optimization**:
```bash
# For email/web, compress if needed (>50MB)
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 \
   -dPDFSETTINGS=/printer -dNOPAUSE -dQUIET -dBATCH \
   -sOutputFile=poster_compressed.pdf poster.pdf

# For printing, keep original (no compression)
```

**Step 5: Accessibility Check**

**Color Contrast Verification**:
- [ ] Text-background contrast ratio ≥ 4.5:1 (WCAG AA)
- [ ] Important elements contrast ratio ≥ 7:1 (WCAG AAA)
- Test online: https://webaim.org/resources/contrastchecker/

**Color Blindness Simulation**:
- [ ] View PDF through color blindness simulator
- [ ] Information not lost with red-green simulation
- [ ] Use Coblis (color-blindness.com) or similar tool

**Step 6: Content Proofreading**

**Systematic Review**:
- [ ] Spell-check all text
- [ ] Verify all author names and affiliations
- [ ] Check all numbers and statistics for accuracy
- [ ] Confirm all citations are correct
- [ ] Review figure labels and captions
- [ ] Check for typos in headers and titles

**Peer Review**:
- [ ] Ask colleague to review poster
- [ ] 30-second test: Can they identify main message?
- [ ] 5-minute review: Do they understand conclusions?
- [ ] Note any confusing elements

**Step 7: Technical Validation**

**LaTeX Compilation Log Review**:
```bash
# Check for warnings in .log file
grep -i "warning\|error\|overfull\|underfull" poster.log

# Common issues to fix:
# - Overfull hbox: Text extending beyond margins
# - Underfull hbox: Excessive spacing
# - Missing references: Citations not resolved
# - Missing figures: Image files not found
```

**Fix Common Warnings**:
```latex
% Overfull hbox (text too wide)
\usepackage{microtype}  % Better spacing
\sloppy  % Allow slightly looser spacing
\hyphenation{long-word}  % Manual hyphenation

% Missing fonts
\usepackage[T1]{fontenc}  % Better font encoding

% Image not found
% Ensure paths are correct and files exist
\graphicspath{{./figures/}{./images/}}
```

**Step 8: Final Pre-Print Checklist**

**Before Sending to Printer**:
- [ ] PDF size exactly matches requirements (check with pdfinfo)
- [ ] All fonts embedded (check with pdffonts)
- [ ] Color mode correct (RGB for screen, CMYK for print if required)
- [ ] Bleed area added if required (usually 3-5mm)
- [ ] Crop marks visible if required
- [ ] Test print completed and reviewed
- [ ] File naming clear: [LastName]_[Conference]_Poster.pdf
- [ ] Backup copy saved

**Printing Specifications to Confirm**:
- [ ] Paper type (matte vs. glossy)
- [ ] Printing method (inkjet, large format, fabric)
- [ ] Color profile (provided to printer if required)
- [ ] Delivery deadline and shipping address
- [ ] Tube or flat packaging preference

**Digital Presentation Checklist**:
- [ ] PDF size optimized (<10MB for email)
- [ ] Tested on multiple PDF viewers (Adobe, Preview, etc.)
- [ ] Displays correctly on different screens
- [ ] QR codes tested and functional
- [ ] Alternative formats prepared (PNG for social media)

**Review Script** (Available in `scripts/review_poster.sh`):
```bash
#!/bin/bash
# Automated poster PDF review script

echo "Poster PDF Quality Check"
echo "======================="

# Check file exists
if [ ! -f "$1" ]; then
    echo "Error: File not found"
    exit 1
fi

echo "File: $1"
echo ""

# Check page size
echo "1. Page Dimensions:"
pdfinfo "$1" | grep "Page size"
echo ""

# Check fonts
echo "2. Font Embedding:"
pdffonts "$1" | head -20
echo ""

# Check file size
echo "3. File Size:"
ls -lh "$1" | awk '{print $5}'
echo ""

# Count pages (should be 1 for poster)
echo "4. Page Count:"
pdfinfo "$1" | grep "Pages"
echo ""

echo "Manual checks required:"
echo "- Visual inspection at 100% zoom"
echo "- Reduced-scale print test (25%)"
echo "- Color contrast verification"
echo "- Proofreading for typos"
```

**Common PDF Issues and Solutions**:

| Issue | Cause | Solution |
|-------|-------|----------|
| Large white margins | Incorrect margin settings | Reduce margin in documentclass |
| Content cut off | Exceeds page boundaries | Check total width/height calculations |
| Blurry images | Low resolution (<300 DPI) | Replace with higher resolution images |
| Missing fonts | Fonts not embedded | Compile with -dEmbedAllFonts=true |
| Wrong page size | Incorrect paper size setting | Verify documentclass paper size |
| Colors look wrong | RGB vs CMYK mismatch | Convert color space for print |
| File too large (>50MB) | Uncompressed images | Optimize images or compress PDF |
| QR codes don't work | Too small or low resolution | Minimum 2×2cm, high contrast |

### 11. Common Poster Content Patterns

Effective content organization for different research types:

**Experimental Research Poster**:
1. Title and authors
2. Introduction: Problem and hypothesis
3. Methods: Experimental design (with diagram)
4. Results: Key findings (2-4 main figures)
5. Conclusions: Main takeaways (3-5 bullet points)
6. Future work (optional)
7. References and acknowledgments

**Computational/Modeling Poster**:
1. Title and authors
2. Motivation: Problem statement
3. Approach: Algorithm or model (with flowchart)
4. Implementation: Technical details
5. Results: Performance metrics and comparisons
6. Applications: Use cases
7. Code availability (QR code to GitHub)
8. References

**Review/Survey Poster**:
1. Title and authors
2. Scope: Topic overview
3. Methods: Literature search strategy
4. Key findings: Main themes (organized by category)
5. Trends: Visualizations of publication patterns
6. Gaps: Identified research needs
7. Conclusions: Summary and implications
8. References

### 12. Accessibility and Inclusive Design

Design posters that are accessible to diverse audiences:

**Color Blindness Considerations**:
- Avoid red-green combinations (most common color blindness)
- Use patterns or shapes in addition to color
- Test with color-blindness simulators
- Provide high contrast (WCAG AA standard: 4.5:1 minimum)

**Visual Impairment Accommodations**:
- Large, clear fonts (minimum 24pt body text)
- High contrast text and background
- Clear visual hierarchy
- Avoid complex textures or patterns in backgrounds

**Language and Content**:
- Clear, concise language
- Define acronyms and jargon
- International audience considerations
- Consider multilingual QR code options for global conferences

### 13. Poster Presentation Best Practices

Guidance beyond LaTeX for effective poster sessions:

**Content Strategy**:
- Tell a story, don't just list facts
- Focus on 1-3 main messages
- Use visual abstract or graphical summary
- Leave room for conversation (don't over-explain)

**Physical Presentation Tips**:
- Bring printed handouts or business cards with QR code
- Prepare 30-second, 2-minute, and 5-minute verbal summaries
- Stand to the side, not blocking the poster
- Engage viewers with open-ended questions

**Digital Backups**:
- Save poster as PDF on mobile device
- Prepare digital version for email sharing
- Create social media-friendly image version
- Have backup printed copy or digital display option

## Workflow for Poster Creation

### Stage 1: Planning and Content Development

1. **Determine poster requirements**:
   - Conference size specifications (A0, 36×48", etc.)
   - Orientation (portrait vs. landscape)
   - Submission deadlines and format requirements

2. **Develop content outline**:
   - Identify 1-3 core messages
   - Select key figures (typically 3-6 main visuals)
   - Draft concise text for each section (bullet points preferred)
   - Aim for 300-800 words total

3. **Choose LaTeX package**:
   - beamerposter: If familiar with Beamer, need institutional themes
   - tikzposter: For modern, colorful designs with flexibility
   - baposter: For structured, professional multi-column layouts

### Stage 2: Generate Visual Elements (AI-Powered)

**CRITICAL: Generate SIMPLE figures with MINIMAL content. Each graphic = ONE message.**

**Content limits:**
- Maximum 4-5 elements per graphic
- Maximum 15 words total per graphic
- 50% white space minimum
- GIANT fonts (80pt+ for labels, 120pt+ for key numbers)

1. **Create figures directory**:
   ```bash
   mkdir -p figures
   ```

2. **Generate SIMPLE visual elements**:
   ```bash
   # Introduction - ONLY 3 icons/elements
   python scripts/generate_schematic.py "POSTER FORMAT for A0. SIMPLE visual with ONLY 3 elements: [icon1] [icon2] [icon3]. ONE word labels (80pt+). 50% white space. Readable from 8 feet." -o figures/intro.png
   
   # Methods - ONLY 4 steps maximum
   python scripts/generate_schematic.py "POSTER FORMAT for A0. SIMPLE flowchart with ONLY 4 boxes: STEP1 → STEP2 → STEP3 → STEP4. GIANT labels (100pt+). 50% white space. NO sub-steps." -o figures/methods.png
   
   # Results - ONLY 3 bars/comparisons
   python scripts/generate_schematic.py "POSTER FORMAT for A0. SIMPLE chart with ONLY 3 bars. GIANT percentages ON bars (120pt+). NO axis, NO legend. 50% white space." -o figures/results.png
   
   # Conclusions - EXACTLY 3 items with GIANT numbers
   python scripts/generate_schematic.py "POSTER FORMAT for A0. EXACTLY 3 key findings: '[NUMBER]' (150pt) '[LABEL]' (60pt) for each. 50% white space. NO other text." -o figures/conclusions.png
   ```

3. **Review generated figures - check for overflow:**
   - **View at 25% zoom**: All text still readable?
   - **Count elements**: More than 5? → Regenerate simpler
   - **Check white space**: Less than 40%? → Add "60% white space" to prompt
   - **Font too small?**: Add "EVEN LARGER" or increase pt sizes
   - **Still overflowing?**: Reduce to 3 elements instead of 4-5

### Stage 3: Design and Layout

1. **Select or create template**:
   - Start with provided templates in `assets/`
   - Customize color scheme to match branding
   - Configure page size and orientation

2. **Design layout structure**:
   - Plan column structure (2, 3, or 4 columns)
   - Map content flow (typically left-to-right, top-to-bottom)
   - Allocate space for title (10-15%), content (70-80%), footer (5-10%)

3. **Set typography**:
   - Configure font sizes for different hierarchy levels
   - Ensure minimum 24pt body text
   - Test readability from 4-6 feet distance

### Stage 4: Content Integration

1. **Create poster header**:
   - Title (concise, descriptive, 10-15 words)
   - Authors and affiliations
   - Institution logos (high-resolution)
   - Conference logo if required

2. **Integrate AI-generated figures**:
   - Add all figures from Stage 2 to appropriate sections
   - Use `\includegraphics` with proper sizing
   - Ensure figures dominate each section (visuals first, text second)
   - Center figures within blocks for visual impact

3. **Add minimal supporting text**:
   - Keep text minimal and scannable (300-800 words total)
   - Use bullet points, not paragraphs
   - Write in active voice
   - Text should complement figures, not duplicate them

4. **Add supplementary elements**:
   - QR codes for supplementary materials
   - References (cite key papers only, 5-10 typical)
   - Contact information and acknowledgments

### Stage 5: Refinement and Testing

1. **Review and iterate**:
   - Check for typos and errors
   - Verify all figures are high resolution
   - Ensure consistent formatting
   - Confirm color scheme works well together

2. **Test readability**:
   - Print at 25% scale and read from 2-3 feet (simulates poster from 8-12 feet)
   - Check color on different monitors
   - Verify QR codes function correctly
   - Ask colleague to review

3. **Optimize for printing**:
   - Embed all fonts in PDF
   - Verify image resolution
   - Check PDF size requirements
   - Include bleed area if required

### Stage 6: Compilation and Delivery

1. **Compile final PDF**:
   ```bash
   pdflatex poster.tex
   # Or for better font support:
   lualatex poster.tex
   ```

2. **Verify output quality**:
   - Check all elements are visible and correctly positioned
   - Zoom to 100% and inspect figure quality
   - Verify colors match expectations
   - Confirm PDF opens correctly on different viewers

3. **Prepare for printing**:
   - Export as PDF/X-1a if required
   - Save backup copies
   - Get test print on regular paper first
   - Order professional printing 2-3 days before deadline

4. **Create supplementary materials**:
   - Save PNG/JPG version for social media
   - Create handout version (8.5×11" summary)
   - Prepare digital version for email sharing

## Integration with Other Skills

This skill works effectively with:
- **Scientific Schematics**: CRITICAL - Use for generating all poster diagrams and flowcharts
- **Generate Image / Nano Banana Pro**: For stylized graphics, conceptual illustrations, and summary visuals
- **Scientific Writing**: For developing poster content from papers
- **Literature Review**: For contextualizing research
- **Data Analysis**: For creating result figures and charts

**Recommended workflow**: Always use scientific-schematics and generate-image skills BEFORE creating the LaTeX poster to generate all visual elements.

## Common Pitfalls to Avoid

**AI-Generated Graphics Mistakes (MOST COMMON):**
- ❌ Too many elements in one graphic (10+ items) → Keep to 3-5 max
- ❌ Text too small in AI graphics → Specify "GIANT (100pt+)" or "HUGE (150pt+)"
- ❌ Too much detail in prompts → Use "SIMPLE" and "ONLY X elements"
- ❌ No white space specification → Add "50% white space" to every prompt
- ❌ Complex flowcharts with 8+ steps → Limit to 4-5 steps maximum
- ❌ Comparison charts with 6+ items → Limit to 3 items maximum
- ❌ Key findings with 5+ metrics → Show only top 3

**Fixing Overflow in AI Graphics:**
If your AI-generated graphics are overflowing or have small text:
1. Add "SIMPLER" or "ONLY 3 elements" to prompt
2. Increase font sizes: "150pt+" instead of "80pt+"
3. Add "60% white space" instead of "50%"
4. Remove sub-details: "NO sub-steps", "NO axis labels", "NO legend"
5. Regenerate with fewer elements

**Design Mistakes**:
- ❌ Too much text (over 1000 words)
- ❌ Font sizes too small (under 24pt body text)
- ❌ Low-contrast color combinations
- ❌ Cluttered layout with no white space
- ❌ Inconsistent styling across sections
- ❌ Poor quality or pixelated images

**Content Mistakes**:
- ❌ No clear narrative or message
- ❌ Too many research questions or objectives
- ❌ Overuse of jargon without definitions
- ❌ Results without context or interpretation
- ❌ Missing author contact information

**Technical Mistakes**:
- ❌ Wrong poster dimensions for conference requirements
- ❌ RGB colors sent to CMYK printer (color shift)
- ❌ Fonts not embedded in PDF
- ❌ File size too large for submission portal
- ❌ QR codes too small or not tested

**Best Practices**:
- ✅ Generate SIMPLE AI graphics with 3-5 elements max
- ✅ Use GIANT fonts (100pt+) for key numbers in graphics
- ✅ Specify "50% white space" in every AI prompt
- ✅ Follow conference size specifications exactly
- ✅ Test print at reduced scale before final printing
- ✅ Use high-contrast, accessible color schemes
- ✅ Keep text minimal and highly scannable
- ✅ Include clear contact information and QR codes
- ✅ Proofread carefully (errors are magnified on posters!)

## Package Installation

Ensure required LaTeX packages are installed:

```bash
# For TeX Live (Linux/Mac)
tlmgr install beamerposter tikzposter baposter

# For MiKTeX (Windows)
# Packages typically auto-install on first use

# Additional recommended packages
tlmgr install qrcode graphics xcolor tcolorbox subcaption
```

## Scripts and Automation

Helper scripts available in `scripts/` directory:

- `compile_poster.sh`: Automated compilation with error handling
- `generate_template.py`: Interactive template generator
- `resize_images.py`: Batch image optimization for posters
- `poster_checklist.py`: Pre-submission validation tool

## References

Comprehensive reference files for detailed guidance:

- `references/latex_poster_packages.md`: Detailed comparison of beamerposter, tikzposter, and baposter with examples
- `references/poster_layout_design.md`: Layout principles, grid systems, and visual flow
- `references/poster_design_principles.md`: Typography, color theory, visual hierarchy, and accessibility
- `references/poster_content_guide.md`: Content organization, writing style, and section-specific guidance

## Templates

Ready-to-use poster templates in `assets/` directory:

- beamerposter templates (classic, modern, colorful)
- tikzposter templates (default, rays, wave, envelope)
- baposter templates (portrait, landscape, minimal)
- Example posters from various scientific disciplines
- Color scheme definitions and institutional templates

Load these templates and customize for your specific research and conference requirements.

