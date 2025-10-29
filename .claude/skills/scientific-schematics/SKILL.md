# Scientific Schematics and Diagrams

## Overview

Scientific schematics and diagrams transform complex concepts, processes, and systems into clear visual representations for publication. Create methodology flowcharts, circuit diagrams, biological pathways, system architecture diagrams, and technical illustrations using TikZ/LaTeX and Python libraries. Generate publication-quality vector graphics that integrate seamlessly with scientific manuscripts.

## When to Use This Skill

This skill should be used when:
- Creating methodology flowcharts for study design and participant flow (CONSORT diagrams)
- Illustrating experimental workflows and data processing pipelines
- Drawing circuit diagrams and electrical schematics for engineering papers
- Visualizing biological pathways, signaling cascades, and molecular interactions
- Depicting system architecture and block diagrams for technical papers
- Creating process flow diagrams and decision trees
- Generating network diagrams showing relationships and hierarchies
- Illustrating equipment setups and experimental apparatus
- Designing conceptual frameworks and theoretical models
- Preparing diagrams that need to match LaTeX typography and style

## Core Capabilities

### 1. Diagram Types Supported

**Methodology Flowcharts**
- CONSORT participant flow diagrams for clinical trials
- Study design overview diagrams
- Data collection and processing workflows
- Analysis pipeline visualization
- Subject enrollment and exclusion flows

**Circuit Diagrams**
- Analog and digital electronic circuits
- Signal processing block diagrams
- Sensor and measurement system schematics
- Control system diagrams
- Communication protocol flows

**Biological Diagrams**
- Cellular signaling pathways
- Metabolic pathway diagrams
- Gene regulatory networks
- Protein-protein interaction networks
- Experimental procedure workflows (cloning, assays)

**System Architecture Diagrams**
- Software architecture and component diagrams
- Hardware system block diagrams
- Data flow diagrams
- Network topology diagrams
- Hierarchical organization charts

**Process Diagrams**
- Sequential process flows
- Decision trees and flowcharts
- State machines and transitions
- Timeline diagrams
- Workflow automation diagrams

### 2. TikZ/LaTeX Integration

TikZ is the gold standard for creating publication-quality diagrams in LaTeX documents. Benefits include:

**Seamless Document Integration**
- Typography matches document font automatically
- Math notation renders identically to document equations
- Color schemes coordinate with document style
- Cross-referencing works natively with \ref and \label

**Vector Graphics Excellence**
- Infinite scalability without quality loss
- Precise positioning and alignment
- Native PDF output for publications
- Smaller file sizes than raster alternatives

**Programmatic Control**
- Define diagrams as code for version control
- Parameterized diagrams that update automatically
- Reusable styles and components
- Easy iteration and refinement

**Key TikZ Packages**
- `tikz` - Core drawing package
- `pgfplots` - Data plotting and visualization
- `circuitikz` - Electrical circuit diagrams
- `tikz-cd` - Commutative diagrams (mathematics)
- `chemfig` - Chemical structure diagrams
- `forest` - Tree diagrams

For comprehensive TikZ syntax and techniques, see `references/tikz_guide.md`.

### 3. Python-Based Diagram Generation

For complex or data-driven diagrams, Python libraries enable programmatic generation:

**Schemdraw** - Circuit and electrical diagrams
- Intuitive Python API for circuit elements
- Automatic wire routing and connections
- Export to SVG, PNG, or embed in matplotlib figures
- Extensive library of electrical components

**NetworkX + Matplotlib** - Network and graph diagrams
- Algorithmic graph layout (spring, hierarchical, circular)
- Network analysis metrics as visual properties
- Customizable node and edge styling
- Integration with scientific data

**Matplotlib Patches** - Custom diagram components
- Rectangle, Circle, Polygon, Arrow primitives
- Complex composite shapes
- Precise positioning and transformations
- Text annotations with LaTeX rendering

For detailed guides and examples, see `references/python_libraries.md`.

### 4. Publication Standards

All diagrams follow scientific publication best practices:

**Vector Format Output**
- PDF for LaTeX integration (preferred)
- SVG for web and presentations
- EPS for legacy publishing systems
- High-resolution PNG as fallback (300+ DPI)

**Colorblind-Friendly Design**
- Okabe-Ito palette for categorical elements
- Perceptually uniform colormaps for continuous data
- Redundant encoding (shapes + colors)
- Grayscale compatibility verification

**Typography Standards**
- Sans-serif fonts (Arial, Helvetica) for consistency
- Minimum 7-8 pt text at final print size
- Clear, readable labels with units
- Consistent notation throughout

**Accessibility**
- High contrast between elements
- Adequate line weights (0.5-1 pt minimum)
- Clear visual hierarchy
- Descriptive captions and alt text

For comprehensive publication guidelines, see `references/best_practices.md`.

## Quick Start Examples

### Example 1: Simple Flowchart in TikZ

```latex
\documentclass{article}
\usepackage{tikz}
\usetikzlibrary{shapes.geometric, arrows.meta}

% Load colorblind-safe colors
\input{tikz_styles.tex}

\begin{document}

\begin{figure}[h]
\centering
\begin{tikzpicture}[
    node distance=2cm,
    process/.style={rectangle, rounded corners, draw=black, thick, 
                    fill=okabe-blue!20, minimum width=3cm, minimum height=1cm},
    decision/.style={diamond, draw=black, thick, fill=okabe-orange!20, 
                     minimum width=2cm, aspect=2},
    arrow/.style={-Stealth, thick}
]

% Nodes
\node (start) [process] {Screen Participants\\(n=500)};
\node (exclude) [process, below of=start] {Exclude (n=150)\\Age $<$ 18 years};
\node (randomize) [process, below of=exclude] {Randomize (n=350)};
\node (treatment) [process, below left=1.5cm and 2cm of randomize] 
                  {Treatment Group\\(n=175)};
\node (control) [process, below right=1.5cm and 2cm of randomize] 
                {Control Group\\(n=175)};
\node (analyze) [process, below=3cm of randomize] {Analyze Data};

% Arrows
\draw [arrow] (start) -- (exclude);
\draw [arrow] (exclude) -- (randomize);
\draw [arrow] (randomize) -| (treatment);
\draw [arrow] (randomize) -| (control);
\draw [arrow] (treatment) |- (analyze);
\draw [arrow] (control) |- (analyze);

\end{tikzpicture}
\caption{Study participant flow diagram following CONSORT guidelines.}
\label{fig:consort}
\end{figure}

\end{document}
```

### Example 2: Circuit Diagram with Schemdraw

```python
import schemdraw
import schemdraw.elements as elm

# Create drawing with colorblind-safe colors
d = schemdraw.Drawing()

# Voltage source
d += elm.SourceV().label('$V_s$')

# Resistors in series
d += elm.Resistor().right().label('$R_1$\n1kΩ')
d += elm.Resistor().label('$R_2$\n2kΩ')

# Capacitor
d += elm.Capacitor().down().label('$C_1$\n10µF')

# Close the circuit
d += elm.Line().left().tox(d.elements[0].start)

# Add ground
d += elm.Ground()

# Save as vector graphics
d.save('circuit_diagram.svg')
d.save('circuit_diagram.pdf')
```

### Example 3: Biological Pathway with Python

```python
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# Okabe-Ito colorblind-safe palette
colors = {
    'protein': '#56B4E9',    # Blue
    'gene': '#009E73',       # Green
    'process': '#F0E442',    # Yellow
    'inhibition': '#D55E00'  # Orange
}

fig, ax = plt.subplots(figsize=(8, 6))

# Define proteins as rounded rectangles
proteins = [
    ('Receptor', 1, 5),
    ('Kinase A', 3, 5),
    ('Kinase B', 5, 5),
    ('TF', 7, 5),
    ('Gene', 7, 3)
]

for name, x, y in proteins:
    color = colors['gene'] if name == 'Gene' else colors['protein']
    box = FancyBboxPatch((x-0.4, y-0.3), 0.8, 0.6, 
                         boxstyle="round,pad=0.1", 
                         facecolor=color, edgecolor='black', linewidth=2)
    ax.add_patch(box)
    ax.text(x, y, name, ha='center', va='center', fontsize=10, fontweight='bold')

# Add activation arrows
arrows = [
    (1.5, 5, 2.5, 5, 'black'),   # Receptor -> Kinase A
    (3.5, 5, 4.5, 5, 'black'),   # Kinase A -> Kinase B
    (5.5, 5, 6.5, 5, 'black'),   # Kinase B -> TF
    (7, 4.7, 7, 3.6, 'black')    # TF -> Gene
]

for x1, y1, x2, y2, color in arrows:
    arrow = FancyArrowPatch((x1, y1), (x2, y2),
                           arrowstyle='->', mutation_scale=20, 
                           linewidth=2, color=color)
    ax.add_patch(arrow)

# Configure axes
ax.set_xlim(0, 8.5)
ax.set_ylim(2, 6)
ax.set_aspect('equal')
ax.axis('off')

plt.tight_layout()
plt.savefig('signaling_pathway.pdf', bbox_inches='tight', dpi=300)
plt.savefig('signaling_pathway.png', bbox_inches='tight', dpi=300)
```

## Workflow for Creating Diagrams

### Planning Phase

1. **Identify diagram purpose** - What concept needs visualization?
2. **Choose diagram type** - Flowchart, circuit, pathway, architecture?
3. **Select tool** - TikZ for LaTeX integration, Python for data-driven
4. **Sketch layout** - Rough hand sketch or wireframe
5. **Plan color scheme** - Use colorblind-safe palettes

### Creation Phase

**For TikZ Diagrams:**
1. Start with template from `assets/` directory
2. Load `tikz_styles.tex` for consistent styling
3. Define node styles and positions
4. Add connections and arrows
5. Label all elements clearly
6. Compile to verify appearance

**For Python Diagrams:**
1. Choose appropriate library (Schemdraw, NetworkX, Matplotlib)
2. Set up figure with publication size
3. Create elements programmatically
4. Apply colorblind-safe palette
5. Export in vector format (PDF, SVG)

### Refinement Phase

1. **Verify readability** - Check text size at final print size
2. **Test accessibility** - View in grayscale, check contrast
3. **Align elements** - Ensure clean, professional appearance
4. **Simplify** - Remove unnecessary elements
5. **Add context** - Include scale bars, legends, annotations
6. **Write caption** - Comprehensive description for figure

### Integration Phase

1. **Place in document** - Use `\input{}` for TikZ, `\includegraphics{}` for external
2. **Reference in text** - Explain diagram in narrative
3. **Cross-reference** - Use `\ref{}` and `\label{}`
4. **Check layout** - Verify placement and text flow
5. **Final compilation** - Ensure all elements render correctly

## Common Use Cases

### Use Case 1: CONSORT Participant Flow Diagram

Clinical trials require standardized participant flow diagrams. Use the flowchart template:

```latex
% Load template
\input{assets/flowchart_template.tex}

% Customize with your numbers
\begin{tikzpicture}[consort]
  \node (assessed) [flowbox] {Assessed for eligibility (n=500)};
  \node (excluded) [flowbox, below=of assessed] {Excluded (n=150)};
  \node (reasons) [infobox, right=of excluded] {
    \begin{tabular}{l}
    Age $<$ 18: n=80 \\
    Declined: n=50 \\
    Other: n=20
    \end{tabular}
  };
  % ... continue diagram
\end{tikzpicture}
```

See `assets/flowchart_template.tex` for complete template.

### Use Case 2: Electronics Circuit Schematic

For electronics papers, use Schemdraw or CircuitikZ:

```python
# Python with Schemdraw - see scripts/circuit_generator.py
from scripts.circuit_generator import create_circuit

circuit = create_circuit(
    components=['voltage_source', 'resistor', 'capacitor', 'ground'],
    values=['5V', '1kΩ', '10µF', None],
    layout='series'
)
circuit.save('my_circuit.pdf')
```

Or use CircuitikZ in LaTeX - see `assets/circuit_template.tex`.

### Use Case 3: Biological Signaling Pathway

Visualize molecular interactions and signaling cascades:

```python
# Python script - see scripts/pathway_diagram.py
from scripts.pathway_diagram import PathwayGenerator

pathway = PathwayGenerator()
pathway.add_protein('EGFR', position=(1, 5))
pathway.add_protein('RAS', position=(3, 5))
pathway.add_protein('RAF', position=(5, 5))
pathway.add_activation('EGFR', 'RAS')
pathway.add_activation('RAS', 'RAF')
pathway.save('mapk_pathway.pdf')
```

Or create in TikZ - see `assets/pathway_template.tex`.

### Use Case 4: System Architecture Diagram

Illustrate software/hardware components and relationships:

```latex
% Use block diagram template
\input{assets/block_diagram_template.tex}

\begin{tikzpicture}[architecture]
  \node (sensor) [component] {Sensor};
  \node (adc) [component, right=of sensor] {ADC};
  \node (micro) [component, right=of adc] {Microcontroller};
  \node (wifi) [component, above right=of micro] {WiFi Module};
  \node (display) [component, below right=of micro] {Display};
  
  \draw [dataflow] (sensor) -- node[above] {Analog} (adc);
  \draw [dataflow] (adc) -- node[above] {Digital} (micro);
  \draw [dataflow] (micro) -- (wifi);
  \draw [dataflow] (micro) -- (display);
\end{tikzpicture}
```

See `assets/block_diagram_template.tex` for complete template.

## Helper Scripts

The `scripts/` directory contains Python utilities for automated diagram generation:

### `generate_flowchart.py`

Convert text descriptions into TikZ flowcharts:

```python
from scripts.generate_flowchart import text_to_flowchart

description = """
1. Screen participants (n=500)
2. Exclude if age < 18 (n=150)
3. Randomize remaining (n=350)
4. Treatment group (n=175)
5. Control group (n=175)
6. Follow up at 3 months
7. Analyze data
"""

tikz_code = text_to_flowchart(description)
with open('methodology_flow.tex', 'w') as f:
    f.write(tikz_code)
```

### `circuit_generator.py`

Generate circuit diagrams using Schemdraw:

```python
from scripts.circuit_generator import CircuitBuilder

builder = CircuitBuilder()
builder.add_voltage_source('Vs', '5V')
builder.add_resistor('R1', '1kΩ')
builder.add_capacitor('C1', '10µF')
builder.add_ground()
builder.save('circuit.pdf')
```

### `pathway_diagram.py`

Create biological pathway diagrams:

```python
from scripts.pathway_diagram import PathwayGenerator

gen = PathwayGenerator()
gen.add_node('Receptor', type='protein', position=(1, 5))
gen.add_node('Kinase', type='protein', position=(3, 5))
gen.add_edge('Receptor', 'Kinase', interaction='activation')
gen.save('pathway.pdf')
```

### `compile_tikz.py`

Standalone TikZ compilation utility:

```bash
# Compile TikZ to PDF
python scripts/compile_tikz.py flowchart.tex -o flowchart.pdf

# Also generate PNG
python scripts/compile_tikz.py flowchart.tex -o flowchart.pdf --png --dpi 300

# Preview in window
python scripts/compile_tikz.py flowchart.tex --preview
```

## Templates and Assets

Pre-built templates in `assets/` directory provide starting points:

- **`flowchart_template.tex`** - Methodology flowcharts (CONSORT style)
- **`circuit_template.tex`** - Electrical circuit diagrams
- **`pathway_template.tex`** - Biological pathway diagrams
- **`block_diagram_template.tex`** - System architecture diagrams
- **`tikz_styles.tex`** - Reusable style definitions (ALWAYS load this)

All templates use colorblind-safe Okabe-Ito palette and publication-ready styling.

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
- **Solution**: Increase `node distance`, adjust positioning manually

**Problem**: Arrows not connecting properly
- **Solution**: Use anchor points: `(node.east)`, `(node.north)`, etc.

### Python Generation Issues

**Problem**: Schemdraw elements not aligning
- **Solution**: Use `.at()` method for precise positioning

**Problem**: Matplotlib text rendering issues
- **Solution**: Set `plt.rcParams['text.usetex'] = True` for LaTeX rendering

**Problem**: Export quality poor
- **Solution**: Increase DPI: `plt.savefig(..., dpi=300, bbox_inches='tight')`

### Accessibility Problems

**Problem**: Colors indistinguishable in grayscale
- **Solution**: Add patterns, shapes, or line styles for redundancy

**Problem**: Text too small when printed
- **Solution**: Design at final size, use minimum 7-8 pt fonts

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

- [ ] Vector format (PDF/SVG) or 300+ DPI raster
- [ ] Colorblind-safe palette (Okabe-Ito)
- [ ] Works in grayscale (test conversion)
- [ ] Text minimum 7-8 pt at final size
- [ ] All elements labeled clearly
- [ ] Consistent styling with other figures
- [ ] Comprehensive caption written
- [ ] Referenced in manuscript text
- [ ] Source files (.tex, .py) saved for revision
- [ ] Exported in required format for journal

Use this skill to create clear, accessible, publication-quality diagrams that effectively communicate complex scientific concepts.

