---
name: scientific-schematics
description: "Create publication-quality scientific diagrams using Nano Banana Pro AI with iterative refinement. AI generation is the default method for all diagram types. Generates high-fidelity images with automatic quality review. Specialized in neural network architectures, system diagrams, flowcharts, biological pathways, and complex scientific visualizations."
allowed-tools: [Read, Write, Edit, Bash]
---

# Scientific Schematics and Diagrams

## Overview

Scientific schematics and diagrams transform complex concepts into clear visual representations for publication. **This skill uses Nano Banana Pro AI for all diagram generation.**

**How it works:**
- Describe your diagram in natural language
- Nano Banana Pro generates publication-quality images automatically
- Automatic iterative refinement (3 iterations by default)
- Built-in quality review and improvement
- Publication-ready output in minutes
- No coding, templates, or manual drawing required

**Simply describe what you want, and Nano Banana Pro creates it.** All diagrams are stored in the figures/ subfolder and referenced in papers/posters.

## Quick Start: Generate Any Diagram

Create any scientific diagram by simply describing it. Nano Banana Pro handles everything automatically:

```bash
# Generate any scientific diagram from a description
python scripts/generate_schematic.py "CONSORT participant flow diagram with 500 screened, 150 excluded, 350 randomized" -o figures/consort.png

# Neural network architecture
python scripts/generate_schematic.py "Transformer encoder-decoder architecture showing multi-head attention, feed-forward layers, and residual connections" -o figures/transformer.png

# Biological pathway
python scripts/generate_schematic.py "MAPK signaling pathway from EGFR to gene transcription" -o figures/mapk_pathway.png

# Custom iterations for complex diagrams
python scripts/generate_schematic.py "Complex circuit diagram with op-amp, resistors, and capacitors" -o figures/circuit.png --iterations 5
```

**What happens behind the scenes:**
1. **Generation 1**: Nano Banana Pro creates initial image following scientific diagram best practices
2. **Review 1**: AI evaluates clarity, labels, accuracy, and accessibility
3. **Generation 2**: Improved prompt based on critique, regenerate
4. **Review 2**: Second evaluation with specific feedback
5. **Generation 3**: Final polished version addressing all critiques

**Output**: Three versions (v1, v2, v3) plus a detailed review log with quality scores and critiques.

### Configuration

Set your OpenRouter API key:
```bash
export OPENROUTER_API_KEY='your_api_key_here'
```

Get an API key at: https://openrouter.ai/keys

### AI Generation Best Practices

**Effective Prompts for Scientific Diagrams:**

✓ **Good prompts** (specific, detailed):
- "CONSORT flowchart showing participant flow from screening (n=500) through randomization to final analysis"
- "Transformer neural network architecture with encoder stack on left, decoder stack on right, showing multi-head attention and cross-attention connections"
- "Biological signaling cascade: EGFR receptor → RAS → RAF → MEK → ERK → nucleus, with phosphorylation steps labeled"
- "Block diagram of IoT system: sensors → microcontroller → WiFi module → cloud server → mobile app"

✗ **Avoid vague prompts**:
- "Make a flowchart" (too generic)
- "Neural network" (which type? what components?)
- "Pathway diagram" (which pathway? what molecules?)

**Key elements to include:**
- **Type**: Flowchart, architecture diagram, pathway, circuit, etc.
- **Components**: Specific elements to include
- **Flow/Direction**: How elements connect (left-to-right, top-to-bottom)
- **Labels**: Key annotations or text to include
- **Style**: Any specific visual requirements

**Scientific Quality Guidelines** (automatically applied):
- Clean white/light background
- High contrast for readability
- Clear, readable labels (minimum 10pt)
- Professional typography (sans-serif fonts)
- Colorblind-friendly colors (Okabe-Ito palette)
- Proper spacing to prevent crowding
- Scale bars, legends, axes where appropriate

## Classic Code-Based Generation

For reproducible, version-controlled diagrams with full programmatic control, use the traditional code-based approach.

## When to Use This Skill

This skill should be used when:
- Creating neural network architecture diagrams (Transformers, CNNs, RNNs, etc.)
- Illustrating system architectures and data flow diagrams
- Drawing methodology flowcharts for study design (CONSORT, PRISMA)
- Visualizing algorithm workflows and processing pipelines
- Creating circuit diagrams and electrical schematics
- Depicting biological pathways and molecular interactions
- Generating network topologies and hierarchical structures
- Illustrating conceptual frameworks and theoretical models
- Designing block diagrams for technical papers

## How to Use This Skill

**Simply describe your diagram in natural language.** Nano Banana Pro generates it automatically:

```bash
python scripts/generate_schematic.py "your diagram description" -o output.png
```

**That's it!** The AI handles:
- ✓ Layout and composition
- ✓ Labels and annotations
- ✓ Colors and styling
- ✓ Quality review and refinement
- ✓ Publication-ready output

**Works for all diagram types:**
- Flowcharts (CONSORT, PRISMA, etc.)
- Neural network architectures
- Biological pathways
- Circuit diagrams
- System architectures
- Block diagrams
- Any scientific visualization

**No coding, no templates, no manual drawing required.**

---

# AI Generation Mode (Nano Banana Pro)

## Iterative Refinement Workflow

The AI generation system uses a sophisticated three-iteration refinement process:

### Iteration 1: Initial Generation
**Prompt Construction:**
```
Scientific diagram guidelines + User request
```

**Example internal prompt:**
```
Create a high-quality scientific diagram with:
- Clean white background
- High contrast for readability
- Clear labels (minimum 10pt font)
- Professional typography
- Colorblind-friendly colors
- Proper spacing

USER REQUEST: CONSORT participant flow diagram showing screening, 
exclusion, randomization, and analysis phases with participant counts
```

**Output:** `diagram_v1.png`

### Iteration 2: Review and Improve
**AI Quality Review:**
- Evaluates scientific accuracy
- Checks label clarity and readability
- Assesses layout and composition
- Verifies accessibility (grayscale, colorblind)
- Assigns quality score (0-10)
- Provides specific improvement suggestions

**Example critique:**
```
Score: 7/10

Strengths:
- Clear flow from top to bottom
- Good use of colors
- All phases labeled

Issues:
- Participant counts (n=X) are too small to read
- "Excluded" box overlaps with arrow
- Would benefit from reasons for exclusion

Suggestions:
- Increase font size for all numbers to at least 12pt
- Add more vertical spacing between boxes
- Include exclusion criteria in a separate annotation box
```

**Improved Prompt:**
```
[Original guidelines + user request]

ITERATION 2: Address these improvements:
- Increase font size for participant counts to 12pt minimum
- Add vertical spacing to prevent overlaps
- Include exclusion criteria in annotation box
```

**Output:** `diagram_v2.png`

### Iteration 3: Final Polish
**Second Review:**
- Verifies improvements were implemented
- Checks for any remaining issues
- Final quality assessment

**Final Generation:**
- Incorporates all feedback
- Produces publication-ready diagram

**Output:** `diagram_v3.png` (final version)

### Review Log
All iterations are saved with a JSON review log:
```json
{
  "user_prompt": "CONSORT participant flow diagram...",
  "iterations": [
    {
      "iteration": 1,
      "image_path": "figures/consort_v1.png",
      "score": 7.0,
      "critique": "..."
    },
    {
      "iteration": 2,
      "image_path": "figures/consort_v2.png",
      "score": 8.5,
      "critique": "..."
    },
    {
      "iteration": 3,
      "image_path": "figures/consort_v3.png",
      "score": 9.5,
      "critique": "..."
    }
  ],
  "final_score": 9.5
}
```

## Advanced AI Generation Usage

### Python API

```python
from scripts.generate_schematic_ai import ScientificSchematicGenerator

# Initialize generator
generator = ScientificSchematicGenerator(
    api_key="your_openrouter_key",
    verbose=True
)

# Generate with iterative refinement
results = generator.generate_iterative(
    user_prompt="Transformer architecture diagram",
    output_path="figures/transformer.png",
    iterations=3
)

# Access results
print(f"Final score: {results['final_score']}/10")
print(f"Final image: {results['final_image']}")

# Review individual iterations
for iteration in results['iterations']:
    print(f"Iteration {iteration['iteration']}: {iteration['score']}/10")
    print(f"Critique: {iteration['critique']}")
```

### Command-Line Options

```bash
# Basic usage
python scripts/generate_schematic.py "diagram description" -o output.png

# Custom iterations (1-10)
python scripts/generate_schematic.py "complex diagram" -o diagram.png --iterations 5

# Verbose output (see all API calls and reviews)
python scripts/generate_schematic.py "flowchart" -o flow.png -v

# Provide API key via flag
python scripts/generate_schematic.py "diagram" -o out.png --api-key "sk-or-v1-..."
```

### Prompt Engineering Tips

**1. Be Specific About Layout:**
```
✓ "Flowchart with vertical flow, top to bottom"
✓ "Architecture diagram with encoder on left, decoder on right"
✓ "Circular pathway diagram with clockwise flow"
```

**2. Include Quantitative Details:**
```
✓ "Neural network with input layer (784 nodes), hidden layer (128 nodes), output (10 nodes)"
✓ "Flowchart showing n=500 screened, n=150 excluded, n=350 randomized"
✓ "Circuit with 1kΩ resistor, 10µF capacitor, 5V source"
```

**3. Specify Visual Style:**
```
✓ "Minimalist block diagram with clean lines"
✓ "Detailed biological pathway with protein structures"
✓ "Technical schematic with engineering notation"
```

**4. Request Specific Labels:**
```
✓ "Label all arrows with activation/inhibition"
✓ "Include layer dimensions in each box"
✓ "Show time progression with timestamps"
```

**5. Mention Color Requirements:**
```
✓ "Use colorblind-friendly colors"
✓ "Grayscale-compatible design"
✓ "Color-code by function: blue for input, green for processing, red for output"
```

## AI Generation Examples

### Example 1: CONSORT Flowchart
```bash
python scripts/generate_schematic.py \
  "CONSORT participant flow diagram for randomized controlled trial. \
   Start with 'Assessed for eligibility (n=500)' at top. \
   Show 'Excluded (n=150)' with reasons: age<18 (n=80), declined (n=50), other (n=20). \
   Then 'Randomized (n=350)' splits into two arms: \
   'Treatment group (n=175)' and 'Control group (n=175)'. \
   Each arm shows 'Lost to follow-up' (n=15 and n=10). \
   End with 'Analyzed' (n=160 and n=165). \
   Use blue boxes for process steps, orange for exclusion, green for final analysis." \
  -o figures/consort.png
```

### Example 2: Neural Network Architecture
```bash
python scripts/generate_schematic.py \
  "Transformer encoder-decoder architecture diagram. \
   Left side: Encoder stack with input embedding, positional encoding, \
   multi-head self-attention, add & norm, feed-forward, add & norm. \
   Right side: Decoder stack with output embedding, positional encoding, \
   masked self-attention, add & norm, cross-attention (receiving from encoder), \
   add & norm, feed-forward, add & norm, linear & softmax. \
   Show cross-attention connection from encoder to decoder with dashed line. \
   Use light blue for encoder, light red for decoder. \
   Label all components clearly." \
  -o figures/transformer.png --iterations 3
```

### Example 3: Biological Pathway
```bash
python scripts/generate_schematic.py \
  "MAPK signaling pathway diagram. \
   Start with EGFR receptor at cell membrane (top). \
   Arrow down to RAS (with GTP label). \
   Arrow to RAF kinase. \
   Arrow to MEK kinase. \
   Arrow to ERK kinase. \
   Final arrow to nucleus showing gene transcription. \
   Label each arrow with 'phosphorylation' or 'activation'. \
   Use rounded rectangles for proteins, different colors for each. \
   Include membrane boundary line at top." \
  -o figures/mapk_pathway.png
```

### Example 4: System Architecture
```bash
python scripts/generate_schematic.py \
  "IoT system architecture block diagram. \
   Bottom layer: Sensors (temperature, humidity, motion) in green boxes. \
   Middle layer: Microcontroller (ESP32) in blue box. \
   Connections to WiFi module (orange box) and Display (purple box). \
   Top layer: Cloud server (gray box) connected to mobile app (light blue box). \
   Show data flow arrows between all components. \
   Label connections with protocols: I2C, UART, WiFi, HTTPS." \
  -o figures/iot_architecture.png
```

---

# Additional Tools

## TikZ Compilation (compile_tikz.py)

If you have existing TikZ `.tex` files that need compilation:

```bash
# Compile TikZ diagram to PDF
python scripts/compile_tikz.py diagram.tex -o diagram.pdf

# Compile and generate PNG
python scripts/compile_tikz.py diagram.tex --png --dpi 300

# Compile and preview
python scripts/compile_tikz.py diagram.tex --preview
```

For details on using `compile_tikz.py`, run:
```bash
python scripts/compile_tikz.py --help
```

---

## Unified Entry Point: generate_schematic.py

The main entry point supports both AI and code-based generation:

```bash
# AI generation (default)
python scripts/generate_schematic.py "diagram description" -o output.png

# Explicit AI method
python scripts/generate_schematic.py "diagram description" -o output.png --method ai

# Code-based generation
python scripts/generate_schematic.py "1. Step one\n2. Step two" -o flow.tex --method code --type flowchart

# Custom iterations for AI
python scripts/generate_schematic.py "complex diagram" -o diagram.png --iterations 5

# Verbose mode
python scripts/generate_schematic.py "diagram" -o out.png -v
```

**Method Selection:**
- `--method ai`: Use Nano Banana Pro with iterative refinement (default)
- `--method code`: Use traditional code-based generation

**Code-Based Types:**
- `--type flowchart`: Generate TikZ flowchart
- `--type circuit`: Generate circuit diagram
- `--type pathway`: Generate biological pathway

## Helper Scripts

### `compile_tikz.py`

Standalone TikZ compilation utility with quality checks:

```bash
# Compile TikZ to PDF with verification
python scripts/compile_tikz.py flowchart.tex -o flowchart.pdf --verify

# Generate PNG with quality report
python scripts/compile_tikz.py flowchart.tex -o flowchart.pdf --png --dpi 300 --verify

# Preview with quality overlay
python scripts/compile_tikz.py flowchart.tex --preview --show-quality
```

**Note:** The Nano Banana Pro AI generation system includes automatic quality review in its iterative refinement process. Each iteration is evaluated for scientific accuracy, clarity, and accessibility.

## Best Practices Summary

### Design Principles

1. **Clarity over complexity** - Simplify, remove unnecessary elements
2. **Consistent styling** - Use templates and style files
3. **Colorblind accessibility** - Use Okabe-Ito palette, redundant encoding
4. **Appropriate typography** - Sans-serif fonts, minimum 7-8 pt
5. **Vector format** - Always use PDF/SVG for publication

### Technical Requirements

1. **Resolution** - Vector preferred, or 300+ DPI for raster
2. **File format** - PDF for LaTeX, SVG for web, PNG as fallback
3. **Color space** - RGB for digital, CMYK for print (convert if needed)
4. **Line weights** - Minimum 0.5 pt, typical 1-2 pt
5. **Text size** - 7-8 pt minimum at final size

### Integration Guidelines

1. **Include in LaTeX** - Use `\input{}` for TikZ, `\includegraphics{}` for external
2. **Caption thoroughly** - Describe all elements and abbreviations
3. **Reference in text** - Explain diagram in narrative flow
4. **Maintain consistency** - Same style across all figures in paper
5. **Version control** - Keep source files (.tex, .py) in repository

## Troubleshooting Common Issues

### TikZ Compilation Errors

**Problem**: `! Package tikz Error: I do not know the key '/tikz/...`
- **Solution**: Missing library - add `\usetikzlibrary{...}` to preamble

**Problem**: Overlapping text or elements
- **Solution**: Use AI generation which automatically handles spacing
- **Solution**: Increase iterations: `--iterations 5` for better refinement
- **Solution**: Use `auto_spacing=True` in pathway generator for automatic adjustment

**Problem**: Arrows not connecting properly
- **Solution**: Use anchor points: `(node.east)`, `(node.north)`, etc.
- **Solution**: Check overlap report for arrow/node intersections

### Python Generation Issues

**Problem**: Schemdraw elements not aligning
- **Solution**: Use `.at()` method for precise positioning
- **Solution**: Enable `auto_spacing` to prevent overlaps

**Problem**: Matplotlib text rendering issues
- **Solution**: Set `plt.rcParams['text.usetex'] = True` for LaTeX rendering
- **Solution**: Ensure LaTeX installation is available

**Problem**: Export quality poor
- **Solution**: AI generation produces high-quality images automatically
- **Solution**: For TikZ, use: `python scripts/compile_tikz.py diagram.tex --png --dpi 300`

**Problem**: Elements overlap after generation
- **Solution**: Run `detect_overlaps()` function to identify problem regions
- **Solution**: Use iterative refinement: `iterative_diagram_refinement(create_function)`
- **Solution**: Increase spacing between elements by 20-30%

### Quality Check Issues

**Problem**: False positive overlap detection
- **Solution**: Adjust threshold: `detect_overlaps(image_path, threshold=0.98)`
- **Solution**: Manually review flagged regions in visual report

**Problem**: Generated image quality is low
- **Solution**: AI generation produces high-quality images by default
- **Solution**: Increase iterations for better results: `--iterations 5`

**Problem**: Colorblind simulation shows poor contrast
- **Solution**: Switch to Okabe-Ito palette explicitly in code
- **Solution**: Add redundant encoding (shapes, patterns, line styles)
- **Solution**: Increase color saturation and lightness differences

**Problem**: High-severity overlaps detected
- **Solution**: Review overlap_report.json for exact positions
- **Solution**: Increase spacing in those specific regions
- **Solution**: Re-run with adjusted parameters and verify again

**Problem**: Visual report generation fails
- **Solution**: Check Pillow and matplotlib installations
- **Solution**: Ensure image file is readable: `Image.open(path).verify()`
- **Solution**: Check sufficient disk space for report generation

### Accessibility Problems

**Problem**: Colors indistinguishable in grayscale
- **Solution**: Run accessibility checker: `verify_accessibility(image_path)`
- **Solution**: Add patterns, shapes, or line styles for redundancy
- **Solution**: Increase contrast between adjacent elements

**Problem**: Text too small when printed
- **Solution**: Run resolution validator: `validate_resolution(image_path)`
- **Solution**: Design at final size, use minimum 7-8 pt fonts
- **Solution**: Check physical dimensions in resolution report

**Problem**: Accessibility checks consistently fail
- **Solution**: Review accessibility_report.json for specific failures
- **Solution**: Increase color contrast by at least 20%
- **Solution**: Test with actual grayscale conversion before finalizing

## Resources and References

### Detailed References

Load these files for comprehensive information on specific topics:

- **`references/tikz_guide.md`** - Complete TikZ syntax, positioning, styles, and techniques
- **`references/diagram_types.md`** - Catalog of scientific diagram types with examples
- **`references/best_practices.md`** - Publication standards and accessibility guidelines
- **`references/python_libraries.md`** - Guide to Schemdraw, NetworkX, and Matplotlib for diagrams

### External Resources

**TikZ and LaTeX**
- TikZ & PGF Manual: https://pgf-tikz.github.io/pgf/pgfmanual.pdf
- TeXample.net: http://www.texample.net/tikz/ (examples gallery)
- CircuitikZ Manual: https://ctan.org/pkg/circuitikz

**Python Libraries**
- Schemdraw Documentation: https://schemdraw.readthedocs.io/
- NetworkX Documentation: https://networkx.org/documentation/
- Matplotlib Documentation: https://matplotlib.org/

**Publication Standards**
- Nature Figure Guidelines: https://www.nature.com/nature/for-authors/final-submission
- Science Figure Guidelines: https://www.science.org/content/page/instructions-preparing-initial-manuscript
- CONSORT Diagram: http://www.consort-statement.org/consort-statement/flow-diagram

## Integration with Other Skills

This skill works synergistically with:

- **Scientific Writing** - Diagrams follow figure best practices
- **Scientific Visualization** - Shares color palettes and styling
- **LaTeX Posters** - Reuse TikZ styles for poster diagrams
- **Research Grants** - Methodology diagrams for proposals
- **Peer Review** - Evaluate diagram clarity and accessibility

## Quick Reference Checklist

Before submitting diagrams, verify:

### Visual Quality
- [ ] High-quality image format (PNG from AI generation)
- [ ] No overlapping elements (AI handles automatically)
- [ ] Adequate spacing between all components (AI optimizes)
- [ ] Clean, professional alignment
- [ ] All arrows connect properly to intended targets

### Accessibility
- [ ] Colorblind-safe palette (Okabe-Ito) used
- [ ] Works in grayscale (tested with accessibility checker)
- [ ] Sufficient contrast between elements (verified)
- [ ] Redundant encoding where appropriate (shapes + colors)
- [ ] Colorblind simulation passes all checks

### Typography and Readability
- [ ] Text minimum 7-8 pt at final size
- [ ] All elements labeled clearly and completely
- [ ] Consistent font family and sizing
- [ ] No text overlaps or cutoffs
- [ ] Units included where applicable

### Publication Standards
- [ ] Consistent styling with other figures in manuscript
- [ ] Comprehensive caption written with all abbreviations defined
- [ ] Referenced appropriately in manuscript text
- [ ] Meets journal-specific dimension requirements
- [ ] Exported in required format for journal (PDF/EPS/TIFF)

### Quality Verification (Required)
- [ ] Ran `run_quality_checks()` and achieved PASS status
- [ ] Reviewed overlap detection report (zero high-severity overlaps)
- [ ] Passed accessibility verification (grayscale and colorblind)
- [ ] Resolution validated at target DPI (300+ for print)
- [ ] Visual quality report generated and reviewed
- [ ] All quality reports saved with figure files

### Documentation and Version Control
- [ ] Source files (.tex, .py) saved for future revision
- [ ] Quality reports archived in `quality_reports/` directory
- [ ] Configuration parameters documented (colors, spacing, sizes)
- [ ] Git commit includes source, output, and quality reports
- [ ] README or comments explain how to regenerate figure

### Final Integration Check
- [ ] Figure displays correctly in compiled manuscript
- [ ] Cross-references work (`\ref{}` points to correct figure)
- [ ] Figure number matches text citations
- [ ] Caption appears on correct page relative to figure
- [ ] No compilation warnings or errors related to figure

## Summary: AI vs Code-Based Generation

### Quick Decision Guide

**Choose AI Generation (Nano Banana Pro) if:**
- ✓ Speed is important (get results in minutes)
- ✓ You want automatic quality review and refinement
- ✓ The diagram is complex with many visual elements
- ✓ You prefer natural language over coding
- ✓ You need publication-ready images immediately
- ✓ You're exploring different design options

**Choose Code-Based Generation if:**
- ✓ You need exact reproducibility from source code
- ✓ You want version control for the diagram source
- ✓ You're generating many similar diagrams programmatically
- ✓ You need LaTeX-native TikZ integration
- ✓ You want pixel-perfect control over every element
- ✓ The diagram is generated from data/algorithms

### Workflow Comparison

| Aspect | AI Generation | Code-Based |
|--------|---------------|------------|
| **Time to first result** | 2-3 minutes | 15-30 minutes |
| **Iterations** | Automatic (3 rounds) | Manual |
| **Quality review** | Automatic by AI | Manual or scripted |
| **Customization** | Natural language | Full programmatic control |
| **Reproducibility** | Prompt-based | Code-based (exact) |
| **Learning curve** | Low (just describe) | Medium-High (learn libraries) |
| **Output format** | PNG/JPG | PDF/SVG/EPS/PNG |
| **Version control** | Prompt + images | Source code + outputs |
| **Best for** | Quick iteration, complex visuals | Reproducible research, data-driven |

### Hybrid Approach (Recommended)

Many users find success with a hybrid workflow:

1. **Prototype with AI**: Generate initial designs quickly using natural language
2. **Review and refine**: Use the AI's iterative refinement to get close to final
3. **Recreate in code** (optional): If exact reproducibility is needed, recreate the approved design in code
4. **Version control**: Keep both the AI prompts and code versions

### Environment Setup

**For AI Generation:**
```bash
# Required
export OPENROUTER_API_KEY='your_api_key_here'

# Get key at: https://openrouter.ai/keys
```

**For Code-Based Generation:**
```bash
# Install Graphviz
brew install graphviz  # macOS
sudo apt-get install graphviz  # Linux

# Install Python packages
pip install graphviz schemdraw networkx matplotlib
```

### Getting Started

**Simplest possible usage (AI):**
```bash
python scripts/generate_schematic.py "your diagram description" -o output.png
```

**Simplest possible usage (Code):**
```bash
python scripts/generate_schematic.py "1. Step one\n2. Step two" -o flow.tex --method code
```

---

Use this skill to create clear, accessible, publication-quality diagrams that effectively communicate complex scientific concepts. The AI-powered workflow with iterative refinement ensures diagrams meet professional standards, while the code-based approach provides exact reproducibility for research publications.

