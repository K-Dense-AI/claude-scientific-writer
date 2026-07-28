# AI Graphics for Posters

Full rules, worked examples, and the mandatory review gates for generating poster
visuals. `SKILL.md` carries the hard limits; this file carries the reasoning, the
per-graphic-type tables, and the complete before/after prompt examples.

### CRITICAL: Preventing Content Overflow

**⚠️ POSTERS MUST NOT HAVE TEXT OR CONTENT CUT OFF AT EDGES.**

**Common Overflow Problems:**
1. **Title/footer text extending beyond page boundaries**
2. **Too many sections crammed into available space**
3. **Figures placed too close to edges**
4. **Text blocks exceeding column widths**

**Prevention Rules:**

**1. Limit Content Sections (MAXIMUM 5-6 sections for A0):**
```
✅ GOOD - 5 sections with room to breathe:
   - Title/Header
   - Introduction/Problem
   - Methods
   - Results (1-2 key findings)
   - Conclusions

❌ BAD - 8+ sections crammed together:
   - Overview, Introduction, Background, Methods, 
   - Results 1, Results 2, Discussion, Conclusions, Future Work
```

**2. Set Safe Margins in LaTeX:**
```latex
% tikzposter - add generous margins
\documentclass[25pt, a0paper, portrait, margin=25mm]{tikzposter}

% baposter - ensure content doesn't touch edges
\begin{poster}{
  columns=3,
  colspacing=2em,           % Space between columns
  headerheight=0.1\textheight,  % Smaller header
  % Leave space at bottom
}
```

**3. Figure Sizing - Never 100% Width:**
```latex
% Leave margins around figures
\includegraphics[width=0.85\linewidth]{figure.png}  % NOT 1.0\linewidth
```

**4. Check for Overflow Before Printing:**
```bash
# Compile and check PDF at 100% zoom
pdflatex poster.tex

# Look for:
# - Text cut off at any edge
# - Content touching page boundaries  
# - Overfull hbox warnings in .log file
grep -i "overfull" poster.log
```

**5. Word Count Limits:**
- **A0 poster**: 300-800 words MAXIMUM
- **Per section**: 50-100 words maximum
- **If you have more content**: Cut it or make a handout

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

**MANDATORY prompt requirements for EVERY poster graphic:**

```
POSTER FORMAT REQUIREMENTS (STRICTLY ENFORCE):
- ABSOLUTE MAXIMUM 3-4 elements per graphic (3 is ideal)
- ABSOLUTE MAXIMUM 10 words total in the entire graphic
- NO complex workflows with 5+ steps (split into 2-3 simple graphics instead)
- NO multi-level nested diagrams (flatten to single level)
- NO case studies with multiple sub-sections (one key point per case)
- ALL text GIANT BOLD (80pt+ for labels, 120pt+ for key numbers)
- High contrast ONLY (dark on white OR white on dark, NO gradients with text)
- MANDATORY 50% white space minimum (half the graphic should be empty)
- Thick lines only (5px+ minimum), large icons (200px+ minimum)
- ONE SINGLE MESSAGE per graphic (not 3 related messages)
```

**⚠️ BEFORE GENERATING: Review your prompt and count elements**
- If your description has 5+ items → STOP. Split into multiple graphics
- If your workflow has 5+ stages → STOP. Show only 3-4 high-level steps
- If your comparison has 4+ methods → STOP. Show only top 3 or Our vs Best Baseline

**Content limits per graphic type (STRICT):**
| Graphic Type | Max Elements | Max Words | Reject If | Good Example |
|--------------|--------------|-----------|-----------|--------------|
| Flowchart | **3-4 boxes MAX** | **8 words** | 5+ stages, nested steps | "DISCOVER → VALIDATE → APPROVE" (3 words) |
| Key findings | **3 items MAX** | **9 words** | 4+ metrics, paragraphs | "95% ACCURATE" "2X FASTER" "FDA READY" (6 words) |
| Comparison chart | **3 bars MAX** | **6 words** | 4+ methods, legend text | "OURS: 95%" "BEST: 85%" (4 words) |
| Case study | **1 case, 3 elements** | **6 words** | Multiple cases, substories | Logo + "18 MONTHS" + "to discovery" (2 words) |
| Timeline | **3-4 points MAX** | **8 words** | Year-by-year detail | "2020 START" "2022 TRIAL" "2024 APPROVED" (6 words) |

**Example - WRONG (7-stage workflow - TOO COMPLEX):**
```bash
# ❌ BAD - This creates tiny unreadable text like the drug discovery poster
python scripts/generate_schematic.py "Drug discovery workflow showing: Stage 1 Target Identification, Stage 2 Molecular Synthesis, Stage 3 Virtual Screening, Stage 4 AI Lead Optimization, Stage 5 Clinical Trial Design, Stage 6 FDA Approval. Include success metrics, timelines, and validation steps for each stage." -o figures/workflow.png
# Result: 7+ stages with tiny text, unreadable from 6 feet - POSTER FAILURE
```

**Example - CORRECT (simplified to 3 key stages):**
```bash
# ✅ GOOD - Same content, split into ONE simple high-level graphic
python scripts/generate_schematic.py "POSTER FORMAT for A0. ULTRA-SIMPLE 3-box workflow: 'DISCOVER' → 'VALIDATE' → 'APPROVE'. Each word in GIANT bold (120pt+). Thick arrows (10px). 60% white space. NO substeps, NO details. 3 words total. Readable from 10 feet." -o figures/workflow_overview.png
# Result: Clean, impactful, readable - can add detail graphics separately if needed
```

**Example - WRONG (complex case studies with multiple sections):**
```bash
# ❌ BAD - Creates cramped unreadable sections
python scripts/generate_schematic.py "Case studies: Insilico Medicine (drug candidate, discovery time, clinical trials), Recursion Pharma (platform, methodology, results), Exscientia (drug candidates, FDA status, timeline). Include company logos, metrics, and outcomes." -o figures/cases.png
# Result: 3 case studies with 4+ elements each = 12+ total elements, tiny text
```

**Example - CORRECT (one case study, one key metric):**
```bash
# ✅ GOOD - Show ONE case with ONE key number
python scripts/generate_schematic.py "POSTER FORMAT for A0. ONE case study card: Company logo (large), '18 MONTHS' in GIANT text (150pt), 'to discovery' below (60pt). 3 elements total: logo + number + caption. 50% white space. Readable from 10 feet." -o figures/case_single.png
# Result: Clear, readable, impactful. Make 3 separate graphics if you need 3 cases.
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
- "generous margins" and "no text near edges"

---

### CRITICAL: AI-Generated Graphic Sizing

**⚠️ Each AI-generated graphic should focus on ONE concept with MINIMAL content.**

**Problem**: Generating complex diagrams with many elements leads to small text.

**Solution**: Generate SIMPLE graphics with FEW elements and LARGE text.

**Example - WRONG (too complex, text will be small):**
```bash
# BAD - too many elements in one graphic
python scripts/generate_schematic.py "Complete ML pipeline showing data collection, 
preprocessing with 5 steps, feature engineering with 8 techniques, model training 
with hyperparameter tuning, validation with cross-validation, and deployment with 
monitoring. Include all labels and descriptions." -o figures/pipeline.png
```

**Example - CORRECT (simple, focused, large text):**
```bash
# GOOD - split into multiple simple graphics with large text

# Graphic 1: High-level overview (3-4 elements max)
python scripts/generate_schematic.py "POSTER FORMAT for A0: Simple 4-step pipeline. 
Four large boxes: DATA → PROCESS → MODEL → RESULTS. 
GIANT labels (80pt+), thick arrows, lots of white space. 
Only 4 words total. Readable from 8 feet." -o figures/overview.png

# Graphic 2: Key result (1 metric highlighted)
python scripts/generate_schematic.py "POSTER FORMAT for A0: Single key metric display.
Giant '95%' text (150pt+) with 'ACCURACY' below (60pt+).
Checkmark icon. Minimal design, high contrast.
Readable from 10 feet." -o figures/accuracy.png
```

**Rules for AI-generated poster graphics:**
| Rule | Limit | Reason |
|------|-------|--------|
| **Elements per graphic** | 3-5 maximum | More elements = smaller text |
| **Words per graphic** | 10-15 maximum | Minimal text = larger fonts |
| **Flowchart steps** | 4-5 maximum | Keeps labels readable |
| **Chart categories** | 3-4 maximum | Prevents crowding |
| **Nested levels** | 1-2 maximum | Avoids complexity |

**Split complex content into multiple simple graphics:**
```
Instead of 1 complex diagram with 12 elements:
→ Create 3 simple diagrams with 4 elements each
→ Each graphic can have LARGER text
→ Arrange in poster with clear visual flow
```

---

### Step 0: MANDATORY Pre-Generation Review (DO THIS FIRST)

**⚠️ BEFORE generating ANY graphics, review your content plan:**

**For EACH planned graphic, ask these questions:**
1. **Element count**: Can I describe this in 3-4 items or less?
   - ❌ NO → Simplify or split into multiple graphics
   - ✅ YES → Continue

2. **Complexity check**: Is this a multi-stage workflow (5+ steps) or nested diagram?
   - ❌ YES → Flatten to 3-4 high-level steps only
   - ✅ NO → Continue

3. **Word count**: Can I describe all text in 10 words or less?
   - ❌ NO → Cut text, use single-word labels
   - ✅ YES → Continue

4. **Message clarity**: Does this graphic convey ONE clear message?
   - ❌ NO → Split into multiple focused graphics
   - ✅ YES → Continue to generation

**Common patterns that ALWAYS fail (reject these):**
- "Show stages 1 through 7..." → Split into high-level overview (3 stages) + detail graphics
- "Multiple case studies..." → One case per graphic
- "Timeline from 2015 to 2024 with annual milestones..." → Show only 3-4 key years
- "Comparison of 6 methods..." → Show only top 3 or Our method vs Best baseline
- "Architecture with all layers and connections..." → High-level only (3-4 components)

### Step 1: Plan Your Poster Elements

After passing the pre-generation review, identify visual elements needed:

1. **Title Block** - Stylized title with institutional branding (optional - can be LaTeX text)
2. **Introduction Graphic** - Conceptual overview (3 elements max)
3. **Methods Diagram** - High-level workflow (3-4 steps max)
4. **Results Figures** - Key findings (3 metrics max per figure, may need 2-3 separate figures)
5. **Conclusion Graphic** - Summary visual (3 takeaways max)
6. **Supplementary Icons** - Simple icons, QR codes, logos (minimal)

### Step 2: Generate Each Element (After Pre-Generation Review)

**⚠️ CRITICAL: Review Step 0 checklist before proceeding.**

Use the appropriate tool for each element type:

**For Schematics and Diagrams (scientific-schematics):**
```bash
# Create figures directory
mkdir -p figures

# Drug discovery workflow - HIGH-LEVEL ONLY, 3 stages
# BAD: "Stage 1: Target ID, Stage 2: Molecular Synthesis, Stage 3: Virtual Screening, Stage 4: AI Lead Opt..."
# GOOD: Collapse to 3 mega-stages
python scripts/generate_schematic.py "POSTER FORMAT for A0. ULTRA-SIMPLE 3-box workflow: 'DISCOVER' (120pt bold) → 'VALIDATE' (120pt bold) → 'APPROVE' (120pt bold). Thick arrows (10px). 60% white space. ONLY these 3 words. NO substeps. Readable from 12 feet." -o figures/workflow_simple.png

# System architecture - MAXIMUM 3 components
python scripts/generate_schematic.py "POSTER FORMAT for A0. ULTRA-SIMPLE 3-component stack: 'DATA' box (120pt) → 'AI MODEL' box (120pt) → 'PREDICTION' box (120pt). Thick vertical arrows. 60% white space. 3 words only. Readable from 12 feet." -o figures/architecture.png

# Timeline - ONLY 3 key milestones (not year-by-year)
# BAD: "2018, 2019, 2020, 2021, 2022, 2023, 2024 with events"
# GOOD: Only 3 breakthrough moments
python scripts/generate_schematic.py "POSTER FORMAT for A0. Timeline with ONLY 3 points: '2018' + icon, '2021' + icon, '2024' + icon. GIANT years (120pt). Large icons. 60% white space. NO connecting lines or details. Readable from 12 feet." -o figures/timeline.png

# Case study - ONE case, ONE key metric
# BAD: "3 case studies: Insilico (details), Recursion (details), Exscientia (details)"
# GOOD: ONE case with ONE number
python scripts/generate_schematic.py "POSTER FORMAT for A0. ONE case study: Large logo + '18 MONTHS' (150pt bold) + 'to discovery' (60pt). 3 elements total. 60% white space. Readable from 12 feet." -o figures/case1.png

# If you need 3 cases → make 3 separate simple graphics (not one complex graphic)
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

### Step 2b: MANDATORY Post-Generation Review (Before Assembly)

**⚠️ CRITICAL: Review EVERY generated graphic before adding to poster.**

**For each generated figure, open at 25% zoom and check:**

1. **✅ PASS criteria (all must be true):**
   - Can read ALL text clearly at 25% zoom
   - Count elements: 3-4 or fewer
   - White space: 50%+ of image is empty
   - Simple enough to understand in 2 seconds
   - NOT a complex workflow with 5+ stages
   - NOT multiple nested sections

2. **❌ FAIL criteria (regenerate if ANY are true):**
   - Text is small or hard to read at 25% zoom → REGENERATE with "150pt+" fonts
   - More than 4 elements → REGENERATE with "ONLY 3 elements"
   - Less than 50% white space → REGENERATE with "60% white space"
   - Complex multi-stage workflow → SPLIT into 2-3 simple graphics
   - Multiple case studies cramped together → SPLIT into separate graphics
   - Takes more than 3 seconds to understand → SIMPLIFY and regenerate

**Common failures and fixes:**
- "7-stage workflow with tiny text" → Regenerate as "3 high-level stages only"
- "3 case studies in one graphic" → Generate 3 separate simple graphics
- "Timeline with 8 years" → Regenerate with "ONLY 3 key milestones"
- "Comparison of 5 methods" → Regenerate with "ONLY Our method vs Best baseline (2 bars)"

**DO NOT PROCEED to assembly if ANY graphic fails the checks above.**

### Step 3: Assemble in LaTeX Template

After all figures pass the post-generation review, include them in your poster template:

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

**Full workflow with ALL quality checks:**

```bash
# STEP 0: Pre-Generation Review (MANDATORY)
# Content plan: Drug discovery poster
# - Workflow: 7 stages → ❌ TOO MANY → Reduce to 3 mega-stages ✅
# - 3 case studies → ❌ TOO MANY → One case per graphic (make 3 graphics) ✅
# - Timeline 2018-2024 → ❌ TOO DETAILED → Only 3 key years ✅

# STEP 1: Create figures directory
mkdir -p figures

# STEP 2: Generate ULTRA-SIMPLE graphics with strict limits

# Workflow - HIGH-LEVEL ONLY (collapsed from 7 stages to 3)
python scripts/generate_schematic.py "POSTER FORMAT for A0. ULTRA-SIMPLE 3-box workflow: 'DISCOVER' → 'VALIDATE' → 'APPROVE'. Each word 120pt+ bold. Thick arrows (10px). 60% white space. ONLY 3 words total. Readable from 12 feet." -o figures/workflow.png

# Case study 1 - ONE case, ONE metric (will make 3 separate graphics)
python scripts/generate_schematic.py "POSTER FORMAT for A0. ONE case: Company logo + '18 MONTHS' (150pt bold) + 'to drug discovery' (60pt). 3 elements only. 60% white space. Readable from 12 feet." -o figures/case1.png

python scripts/generate_schematic.py "POSTER FORMAT for A0. ONE case: Company logo + '95% SUCCESS' (150pt bold) + 'in trials' (60pt). 3 elements only. 60% white space." -o figures/case2.png

python scripts/generate_schematic.py "POSTER FORMAT for A0. ONE case: Company logo + 'FDA APPROVED' (150pt bold) + '2024' (60pt). 3 elements only. 60% white space." -o figures/case3.png

# Timeline - ONLY 3 key years (not 7 years)
python scripts/generate_schematic.py "POSTER FORMAT for A0. ONLY 3 years: '2018' (150pt) + icon, '2021' (150pt) + icon, '2024' (150pt) + icon. Large icons. 60% white space. NO lines or details. Readable from 12 feet." -o figures/timeline.png

# Results - ONLY 2 bars (our method vs best baseline, not 5 methods)
python scripts/generate_schematic.py "POSTER FORMAT for A0. TWO bars only: 'BASELINE 70%' and 'OURS 95%' (highlighted). GIANT percentages (150pt) ON bars. NO axis, NO legend. 60% white space. Readable from 12 feet." -o figures/results.png

# STEP 2b: Post-Generation Review (MANDATORY)
# Open each figure at 25% zoom:
# ✅ workflow.png: 3 elements, text readable, 60% white - PASS
# ✅ case1.png: 3 elements, giant numbers, clean - PASS
# ✅ case2.png: 3 elements, giant numbers, clean - PASS  
# ✅ case3.png: 3 elements, giant numbers, clean - PASS
# ✅ timeline.png: 3 elements, readable, simple - PASS
# ✅ results.png: 2 bars, giant percentages, clear - PASS
# ALL PASS → Proceed to assembly

# STEP 3: Compile LaTeX poster
pdflatex poster.tex

# STEP 4: PDF Overflow Check (see Section 11)
grep "Overfull" poster.log
# Open at 100% and check all 4 edges
```

**If ANY graphic fails Step 2b review:**
- Too many elements → Regenerate with "ONLY 3 elements"
- Small text → Regenerate with "150pt+" or "GIANT BOLD (150pt+)"
- Cluttered → Regenerate with "60% white space" and "ULTRA-SIMPLE"
- Complex workflow → SPLIT into multiple simple 3-element graphics

### Visual Element Guidelines

**⚠️ CRITICAL: Each graphic must have ONE message and MAXIMUM 3-4 elements.**

**ABSOLUTE LIMITS - These are NOT guidelines, these are HARD LIMITS:**
- **MAXIMUM 3-4 elements** per graphic (3 is ideal)
- **MAXIMUM 10 words** total per graphic
- **MINIMUM 50% white space** (60% is better)
- **MINIMUM 120pt** for key numbers/metrics
- **MINIMUM 80pt** for labels

**For each poster section - STRICT requirements:**

| Section | Max Elements | Max Words | Example Prompt (REQUIRED PATTERN) |
|---------|--------------|-----------|-------------------------------------|
| **Introduction** | 3 icons | 6 words | "POSTER FORMAT for A0: ULTRA-SIMPLE 3 icons: [icon1] [icon2] [icon3]. ONE WORD labels (100pt bold). 60% white space. 3 words total." |
| **Methods** | 3 boxes | 6 words | "POSTER FORMAT for A0: ULTRA-SIMPLE 3-box workflow: 'STEP1' → 'STEP2' → 'STEP3'. GIANT labels (120pt+). 60% white space. 3 words only." |
| **Results** | 2-3 bars | 6 words | "POSTER FORMAT for A0: TWO bars: 'BASELINE 70%' 'OURS 95%'. GIANT percentages (150pt+) ON bars. NO axis. 60% white space." |
| **Conclusions** | 3 cards | 9 words | "POSTER FORMAT for A0: THREE cards: '95%' (150pt) 'ACCURATE', '2X' (150pt) 'FASTER', checkmark 'READY'. 60% white space." |
| **Case Study** | 3 elements | 5 words | "POSTER FORMAT for A0: ONE case: logo + '18 MONTHS' (150pt) + 'to discovery' (60pt). 60% white space." |
| **Timeline** | 3 points | 3 words | "POSTER FORMAT for A0: THREE years only: '2018' '2021' '2024' (150pt each). Large icons. 60% white space. NO details." |

**MANDATORY prompt elements (ALL required, NO exceptions):**
1. **"POSTER FORMAT for A0"** - MUST be first
2. **"ULTRA-SIMPLE"** or **"ONLY X elements"** - content limit
3. **"GIANT (120pt+)"** or specific font sizes - readability
4. **"60% white space"** - mandatory breathing room
5. **"readable from 10-12 feet"** - viewing distance
6. **Exact count** of words/elements - "3 words total" or "ONLY 3 icons"

**PATTERNS THAT ALWAYS FAIL (REJECT IMMEDIATELY):**
- ❌ "7-stage drug discovery workflow" → Split to "3 mega-stages"
- ❌ "Timeline from 2015-2024 with annual updates" → "ONLY 3 key years"
- ❌ "3 case studies with details" → Make 3 separate simple graphics
- ❌ "Comparison of 5 methods with metrics" → "ONLY 2: ours vs best"
- ❌ "Complete architecture showing all layers" → "3 components only"
- ❌ "Show stages 1,2,3,4,5,6" → "3 high-level stages"

**PATTERNS THAT WORK:**
- ✅ "3 mega-stages collapsed from 7" → Proper simplification
- ✅ "ONE case with ONE metric" → Will make multiple if needed
- ✅ "ONLY 3 milestones" → Selective, focused
- ✅ "2 bars: ours vs baseline" → Direct comparison
- ✅ "3-component high-level view" → Appropriately simplified

---
