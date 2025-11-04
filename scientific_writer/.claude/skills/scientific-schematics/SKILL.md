---
name: scientific-schematics
description: "Create publication-quality scientific diagrams, flowcharts, and schematics using Python (graphviz, matplotlib, schemdraw, networkx). Specialized in neural network architectures, system diagrams, and flowcharts. Generates SVG/EPS in figures/ folder with automated quality verification."
---

# Scientific Schematics and Diagrams

## Overview

Scientific schematics and diagrams transform complex concepts into clear visual representations for publication. Generate neural network architectures, flowcharts, circuit diagrams, biological pathways, and system diagrams using best-in-class Python libraries. **All diagrams are created as SVG/EPS files, stored in the figures/ subfolder, and referenced in papers/posters** - never embedded directly in LaTeX.

## Zero-Shot Diagram Generation Workflow

**Standard workflow for ALL diagrams:**

1. **Analyze requirements** - Identify diagram type and components
2. **Choose optimal library** - Select best tool for the specific diagram type
3. **Generate vector graphic** - Create SVG/EPS with proper spacing and layout
4. **Store in figures/** - Save to `figures/` subfolder with descriptive name
5. **Run quality checks** - Verify no overlaps, good contrast, proper resolution
6. **Reference in document** - Use `\includegraphics{figures/diagram_name.pdf}` in LaTeX

**Key principle:** Generate standalone vector graphics first, then integrate into documents.

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

## Best Libraries by Diagram Type

Choose the optimal library for your specific diagram type:

### Neural Network Architectures (Transformers, CNNs, etc.)
**Best library:** `graphviz` via Python's `pygraphviz` or `pydot`
- Excellent automatic layout algorithms
- Clean, professional appearance
- Perfect for layer stacks and connections
- Handles complex cross-connections well

**Alternative:** Custom `matplotlib` with careful positioning
- More control over exact placement
- Better for highly customized designs
- Requires more manual positioning

### Flowcharts and Process Diagrams
**Best library:** `graphviz` with `dot` or `flowchart` layout
- Automatic optimal positioning
- Standard flowchart shapes
- Clean arrow routing
- Minimal overlap issues

**Alternative:** `diagrams` library (for cloud/system architecture style)

### Circuit Diagrams
**Best library:** `schemdraw`
- Purpose-built for electrical circuits
- Extensive component library
- Automatic wire routing
- Professional engineering standard output

### Biological Pathways
**Best library:** `networkx` with custom rendering
- Graph-based pathway representation
- Algorithm-driven layout
- Flexible node/edge styling

### Block Diagrams and System Architecture
**Best library:** `graphviz` or `diagrams`
- Clean hierarchical layouts
- Automatic spacing
- Professional appearance

## Zero-Shot Examples for Common Diagram Types

### Example 1: Transformer Architecture (Neural Network)

Creating a Transformer encoder-decoder diagram like in "Attention Is All You Need":

```python
import graphviz
from pathlib import Path

def create_transformer_diagram(output_dir='figures'):
    """
    Create a Transformer architecture diagram.
    Zero-shot generation with automatic layout.
    """
    Path(output_dir).mkdir(exist_ok=True)
    
    # Create directed graph with TB (top-to-bottom) layout
    dot = graphviz.Digraph(
        'transformer',
        format='pdf',
        graph_attr={
            'rankdir': 'BT',  # Bottom to top (like the original paper)
            'splines': 'ortho',  # Orthogonal edges
            'nodesep': '0.5',
            'ranksep': '0.8',
            'bgcolor': 'white',
            'dpi': '300'
        },
        node_attr={
            'shape': 'box',
            'style': 'rounded,filled',
            'fillcolor': 'lightgray',
            'fontname': 'Arial',
            'fontsize': '11',
            'width': '2.5',
            'height': '0.5'
        },
        edge_attr={
            'color': 'black',
            'penwidth': '1.5'
        }
    )
    
    # ENCODER STACK (left side)
    with dot.subgraph(name='cluster_encoder') as enc:
        enc.attr(label='Encoder', fontsize='14', fontname='Arial-Bold')
        enc.attr(style='rounded', color='blue', penwidth='2')
        
        # Encoder layers (bottom to top)
        enc.node('enc_input_emb', 'Input Embedding', fillcolor='#E8F4F8')
        enc.node('enc_pos', 'Positional Encoding', fillcolor='#E8F4F8')
        enc.node('enc_mha', 'Multi-Head\nAttention', fillcolor='#B3D9E6')
        enc.node('enc_an1', 'Add & Norm', fillcolor='#CCE5FF')
        enc.node('enc_ff', 'Feed Forward', fillcolor='#B3D9E6')
        enc.node('enc_an2', 'Add & Norm', fillcolor='#CCE5FF')
        
        # Encoder flow
        enc.edge('enc_input_emb', 'enc_pos')
        enc.edge('enc_pos', 'enc_mha')
        enc.edge('enc_mha', 'enc_an1')
        enc.edge('enc_an1', 'enc_ff')
        enc.edge('enc_ff', 'enc_an2')
    
    # DECODER STACK (right side)
    with dot.subgraph(name='cluster_decoder') as dec:
        dec.attr(label='Decoder', fontsize='14', fontname='Arial-Bold')
        dec.attr(style='rounded', color='red', penwidth='2')
        
        # Decoder layers (bottom to top)
        dec.node('dec_output_emb', 'Output Embedding', fillcolor='#FFE8E8')
        dec.node('dec_pos', 'Positional Encoding', fillcolor='#FFE8E8')
        dec.node('dec_mmha', 'Masked Self-\nAttention', fillcolor='#FFB3B3')
        dec.node('dec_an1', 'Add & Norm', fillcolor='#FFCCCC')
        dec.node('dec_cross', 'Cross-Attention', fillcolor='#FFB3B3')
        dec.node('dec_an2', 'Add & Norm', fillcolor='#FFCCCC')
        dec.node('dec_ff', 'Feed Forward', fillcolor='#FFB3B3')
        dec.node('dec_an3', 'Add & Norm', fillcolor='#FFCCCC')
        dec.node('dec_linear', 'Linear & Softmax', fillcolor='#FF9999')
        dec.node('dec_output', 'Output\nProbabilities', fillcolor='#FFE8E8')
        
        # Decoder flow
        dec.edge('dec_output_emb', 'dec_pos')
        dec.edge('dec_pos', 'dec_mmha')
        dec.edge('dec_mmha', 'dec_an1')
        dec.edge('dec_an1', 'dec_cross')
        dec.edge('dec_cross', 'dec_an2')
        dec.edge('dec_an2', 'dec_ff')
        dec.edge('dec_ff', 'dec_an3')
        dec.edge('dec_an3', 'dec_linear')
        dec.edge('dec_linear', 'dec_output')
    
    # Cross-attention connection (encoder to decoder)
    dot.edge('enc_an2', 'dec_cross', 
             style='dashed', 
             color='purple', 
             label='  context  ',
             fontsize='9')
    
    # Input and output labels
    dot.node('input_seq', 'Input Sequence', 
             shape='ellipse', fillcolor='lightgreen')
    dot.node('target_seq', 'Target Sequence', 
             shape='ellipse', fillcolor='lightgreen')
    
    dot.edge('input_seq', 'enc_input_emb')
    dot.edge('target_seq', 'dec_output_emb')
    
    # Render to files
    output_path = f'{output_dir}/transformer_architecture'
    dot.render(output_path, cleanup=True)
    
    # Also save as SVG and EPS
    dot.format = 'svg'
    dot.render(output_path, cleanup=True)
    dot.format = 'eps'
    dot.render(output_path, cleanup=True)
    
    print(f"✓ Transformer diagram created:")
    print(f"  - {output_path}.pdf")
    print(f"  - {output_path}.svg")
    print(f"  - {output_path}.eps")
    
    return f"{output_path}.pdf"

# Usage
if __name__ == '__main__':
    diagram_path = create_transformer_diagram('figures')
    
    # Run quality checks
    from quality_checker import run_quality_checks
    run_quality_checks(diagram_path.replace('.pdf', '.png'))
```

**LaTeX integration:**
```latex
\begin{figure}[htbp]
\centering
\includegraphics[width=0.9\textwidth]{figures/transformer_architecture.pdf}
\caption{Transformer encoder-decoder architecture showing multi-head attention,
         feed-forward layers, and cross-attention mechanism.}
\label{fig:transformer}
\end{figure}
```

### Example 2: Simple Flowchart (CONSORT-style)

```python
import graphviz
from pathlib import Path

def create_consort_flowchart(output_dir='figures'):
    """Create a CONSORT participant flow diagram."""
    Path(output_dir).mkdir(exist_ok=True)
    
    dot = graphviz.Digraph(
        'consort',
        format='pdf',
        graph_attr={
            'rankdir': 'TB',
            'splines': 'ortho',
            'nodesep': '0.6',
            'ranksep': '0.8',
            'bgcolor': 'white'
        },
        node_attr={
            'shape': 'box',
            'style': 'rounded,filled',
            'fillcolor': '#E8F4F8',
            'fontname': 'Arial',
            'fontsize': '10',
            'width': '3',
            'height': '0.6'
        }
    )
    
    # Enrollment
    dot.node('assessed', 'Assessed for eligibility\n(n=500)')
    dot.node('excluded', 'Excluded (n=150)\n• Age < 18: n=80\n• Declined: n=50\n• Other: n=20')
    dot.node('randomized', 'Randomized\n(n=350)')
    
    # Allocation
    dot.node('treatment', 'Allocated to treatment\n(n=175)', fillcolor='#C8E6C9')
    dot.node('control', 'Allocated to control\n(n=175)', fillcolor='#FFECB3')
    
    # Follow-up
    dot.node('treat_lost', 'Lost to follow-up (n=15)', fillcolor='#FFCDD2')
    dot.node('ctrl_lost', 'Lost to follow-up (n=10)', fillcolor='#FFCDD2')
    
    # Analysis
    dot.node('treat_analyzed', 'Analyzed (n=160)', fillcolor='#C8E6C9')
    dot.node('ctrl_analyzed', 'Analyzed (n=165)', fillcolor='#FFECB3')
    
    # Connect nodes
    dot.edge('assessed', 'excluded')
    dot.edge('assessed', 'randomized')
    dot.edge('randomized', 'treatment')
    dot.edge('randomized', 'control')
    dot.edge('treatment', 'treat_lost')
    dot.edge('treatment', 'treat_analyzed')
    dot.edge('control', 'ctrl_lost')
    dot.edge('control', 'ctrl_analyzed')
    
    # Render
    output_path = f'{output_dir}/consort_flowchart'
    dot.render(output_path, cleanup=True)
    
    print(f"✓ CONSORT flowchart created: {output_path}.pdf")
    return f"{output_path}.pdf"
```

### Example 3: CNN Architecture

```python
def create_cnn_architecture(output_dir='figures'):
    """Create a CNN architecture diagram."""
    dot = graphviz.Digraph(
        'cnn',
        format='pdf',
        graph_attr={'rankdir': 'LR', 'bgcolor': 'white'}
    )
    
    # Define layers
    layers = [
        ('input', 'Input\n32×32×3', '#FFE8E8'),
        ('conv1', 'Conv 3×3\n32 filters', '#B3D9E6'),
        ('pool1', 'MaxPool\n2×2', '#FFE5B3'),
        ('conv2', 'Conv 3×3\n64 filters', '#B3D9E6'),
        ('pool2', 'MaxPool\n2×2', '#FFE5B3'),
        ('flatten', 'Flatten', '#D4E8D4'),
        ('fc1', 'FC 128', '#C8B3E6'),
        ('fc2', 'FC 10', '#C8B3E6'),
        ('softmax', 'Softmax', '#FFC8C8')
    ]
    
    # Create nodes
    for node_id, label, color in layers:
        dot.node(node_id, label, 
                shape='box', style='rounded,filled', 
                fillcolor=color, fontname='Arial')
    
    # Connect layers
    for i in range(len(layers) - 1):
        dot.edge(layers[i][0], layers[i+1][0])
    
    output_path = f'{output_dir}/cnn_architecture'
    dot.render(output_path, cleanup=True)
    
    print(f"✓ CNN diagram created: {output_path}.pdf")
    return f"{output_path}.pdf"
```

## Core Capabilities

### 1. Diagram Types Supported

**Neural Network Architectures**
- Transformer encoder-decoder models
- Convolutional Neural Networks (CNNs)
- Recurrent networks (LSTM, GRU)
- Attention mechanisms and variants
- Custom deep learning architectures

**Methodology Flowcharts**
- CONSORT participant flow diagrams
- PRISMA systematic review flows
- Data processing pipelines
- Algorithm workflows
- Subject enrollment flows

**Circuit Diagrams**
- Analog and digital electronic circuits
- Signal processing block diagrams
- Control system diagrams

**Biological Diagrams**
- Signaling pathways
- Metabolic pathway diagrams
- Gene regulatory networks
- Protein interaction networks

**System Architecture Diagrams**
- Software architecture and components
- Data flow diagrams
- Network topology diagrams
- Hierarchical organization charts

## Required Libraries and Installation

### Primary Library: Graphviz (Recommended for 90% of diagrams)

Graphviz is the best tool for most scientific diagrams due to automatic layout, clean rendering, and zero-overlap guarantee.

**Installation:**
```bash
# Install Graphviz binary (required)
# macOS
brew install graphviz

# Ubuntu/Debian
sudo apt-get install graphviz

# Install Python bindings
pip install graphviz
```

**Why Graphviz is optimal:**
- ✓ Automatic optimal layout (no manual positioning needed)
- ✓ Zero overlaps guaranteed by layout algorithms
- ✓ Professional appearance out of the box
- ✓ Supports complex hierarchies and cross-connections
- ✓ Native SVG, PDF, EPS output
- ✓ Minimal code for maximum quality

### Specialized Libraries

**Schemdraw** - Circuit diagrams only
```bash
pip install schemdraw
```

**NetworkX** - Complex network analysis + visualization
```bash
pip install networkx matplotlib
```

**Matplotlib** - Custom manual diagrams (when you need exact control)
```bash
pip install matplotlib
```

## Quick Start Guide for Zero-Shot Diagram Creation

Follow this systematic approach for any diagram type:

### Step 1: Identify Diagram Structure

Ask yourself:
- **Is it a hierarchy?** → Use `rankdir='TB'` or `'BT'` (top-to-bottom or bottom-to-top)
- **Is it a sequence?** → Use `rankdir='LR'` (left-to-right)
- **Does it have parallel branches?** → Use subgraphs/clusters
- **Does it have cross-connections?** → Graphviz handles this automatically

### Step 2: Set Up Base Template

Start with this template and customize:

```python
import graphviz
from pathlib import Path

def create_diagram(output_dir='figures', diagram_name='my_diagram'):
    """Universal diagram creation template."""
    Path(output_dir).mkdir(exist_ok=True, parents=True)
    
    dot = graphviz.Digraph(
        name=diagram_name,
        format='pdf',
        graph_attr={
            'rankdir': 'TB',      # TB, BT, LR, or RL
            'splines': 'ortho',   # ortho (straight) or curved
            'nodesep': '0.6',     # horizontal spacing
            'ranksep': '0.8',     # vertical spacing
            'bgcolor': 'white',
            'dpi': '300'
        },
        node_attr={
            'shape': 'box',       # box, ellipse, diamond, etc.
            'style': 'rounded,filled',
            'fillcolor': 'lightgray',
            'fontname': 'Arial',
            'fontsize': '11',
            'margin': '0.2',
            'width': '2',         # minimum width
            'height': '0.5'       # minimum height
        },
        edge_attr={
            'color': 'black',
            'penwidth': '1.5',
            'arrowsize': '0.8'
        }
    )
    
    # Add your nodes and edges here
    dot.node('node1', 'Label 1')
    dot.node('node2', 'Label 2')
    dot.edge('node1', 'node2')
    
    # Render to multiple formats
    output_path = f'{output_dir}/{diagram_name}'
    dot.render(output_path, cleanup=True)  # PDF
    dot.format = 'svg'
    dot.render(output_path, cleanup=True)  # SVG
    dot.format = 'eps'
    dot.render(output_path, cleanup=True)  # EPS
    
    print(f"✓ Diagram saved: {output_path}.{{pdf,svg,eps}}")
    return f"{output_path}.pdf"
```

### Step 3: Add Nodes with Clear Labels

**Best practices:**
- Use descriptive node IDs: `'encoder_layer1'` not `'n1'`
- Use `\n` for multi-line labels
- Use fill colors to group related components
- Keep labels concise (3-5 words max per line)

```python
# Good node definitions
dot.node('input_layer', 'Input Layer\n(512 dims)', fillcolor='#E8F4F8')
dot.node('attention', 'Multi-Head\nAttention', fillcolor='#B3D9E6')
dot.node('output', 'Output', fillcolor='#C8E6C9')
```

### Step 4: Connect Nodes with Edges

**Edge types:**
```python
# Standard arrow
dot.edge('node1', 'node2')

# Dashed line (for information flow)
dot.edge('encoder', 'decoder', style='dashed')

# Bidirectional
dot.edge('node1', 'node2', dir='both')

# With label
dot.edge('layer1', 'layer2', label='  ReLU  ')

# Different color
dot.edge('input', 'output', color='red', penwidth='2')
```

### Step 5: Use Subgraphs for Grouping

**For parallel structures (like Encoder/Decoder):**
```python
# Encoder cluster
with dot.subgraph(name='cluster_encoder') as enc:
    enc.attr(label='Encoder', style='rounded', color='blue')
    enc.node('enc1', 'Encoder Layer 1')
    enc.node('enc2', 'Encoder Layer 2')
    enc.edge('enc1', 'enc2')

# Decoder cluster
with dot.subgraph(name='cluster_decoder') as dec:
    dec.attr(label='Decoder', style='rounded', color='red')
    dec.node('dec1', 'Decoder Layer 1')
    dec.node('dec2', 'Decoder Layer 2')
    dec.edge('dec1', 'dec2')

# Cross-connection between clusters
dot.edge('enc2', 'dec1', style='dashed', color='purple')
```

### Step 6: Render and Verify

```python
# Always render to PDF (for LaTeX) and SVG (for web/slides)
output_path = f'{output_dir}/{diagram_name}'

# PDF for papers
dot.format = 'pdf'
dot.render(output_path, cleanup=True)

# SVG for posters/slides
dot.format = 'svg'
dot.render(output_path, cleanup=True)

# EPS for some journals
dot.format = 'eps'
dot.render(output_path, cleanup=True)
```

## Common Graphviz Attributes Quick Reference

### Graph Attributes (overall layout)
```python
graph_attr={
    'rankdir': 'TB',        # Direction: TB, BT, LR, RL
    'splines': 'ortho',     # Edge style: ortho, curved, line, polyline
    'nodesep': '0.5',       # Space between nodes (inches)
    'ranksep': '0.8',       # Space between ranks (inches)
    'bgcolor': 'white',     # Background color
    'dpi': '300',           # Resolution for raster output
    'compound': 'true',     # Allow edges between clusters
    'concentrate': 'true'   # Merge multiple edges
}
```

### Node Attributes (boxes/shapes)
```python
node_attr={
    'shape': 'box',         # box, ellipse, circle, diamond, plaintext
    'style': 'rounded,filled',  # rounded, filled, dashed, bold
    'fillcolor': '#E8F4F8', # Fill color (hex or name)
    'color': 'black',       # Border color
    'penwidth': '1.5',      # Border width
    'fontname': 'Arial',    # Font family
    'fontsize': '11',       # Font size (points)
    'fontcolor': 'black',   # Text color
    'width': '2',           # Minimum width (inches)
    'height': '0.5',        # Minimum height (inches)
    'margin': '0.2'         # Internal padding
}
```

### Edge Attributes (arrows/connections)
```python
edge_attr={
    'color': 'black',       # Line color
    'penwidth': '1.5',      # Line width
    'style': 'solid',       # solid, dashed, dotted, bold
    'arrowsize': '1.0',     # Arrow head size
    'dir': 'forward',       # forward, back, both, none
    'arrowhead': 'normal'   # normal, vee, diamond, dot, none
}
```

## Colorblind-Safe Palettes

Use these color sets to ensure accessibility:

### Okabe-Ito Palette (8 colors)
```python
OKABE_ITO = {
    'orange': '#E69F00',
    'sky_blue': '#56B4E9',
    'green': '#009E73',
    'yellow': '#F0E442',
    'blue': '#0072B2',
    'vermillion': '#D55E00',
    'purple': '#CC79A7',
    'black': '#000000'
}
```

### Light Backgrounds (for filled nodes)
```python
LIGHT_FILLS = {
    'blue': '#E8F4F8',
    'green': '#E8F5E9',
    'orange': '#FFF3E0',
    'purple': '#F3E5F5',
    'red': '#FFEBEE',
    'yellow': '#FFFDE7',
    'gray': '#F5F5F5'
}
```

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

## Production Workflow (From Concept to Publication)

Follow this systematic workflow for all diagrams:

### Phase 1: Analysis (2 minutes)

1. **Identify diagram type** - What are you visualizing?
   - Neural network architecture? → Use graphviz
   - Flowchart (CONSORT, PRISMA)? → Use graphviz
   - Circuit diagram? → Use schemdraw
   - Complex network? → Use networkx + graphviz

2. **Determine layout direction**
   - Vertical flow (top-to-bottom)? → `rankdir='TB'`
   - Bottom-up (like Transformer)? → `rankdir='BT'`  
   - Left-to-right sequence? → `rankdir='LR'`
   - Right-to-left? → `rankdir='RL'`

3. **Identify groupings**
   - Parallel structures (encoder/decoder)? → Use clusters/subgraphs
   - Sequential only? → Simple node chain
   - Cross-connections? → Graphviz handles automatically

### Phase 2: Implementation (10-15 minutes)

**Standard procedure for 95% of diagrams:**

```python
import graphviz
from pathlib import Path

# 1. Set up output directory
output_dir = 'figures'
Path(output_dir).mkdir(exist_ok=True, parents=True)

# 2. Create diagram with base template
dot = graphviz.Digraph(
    'my_diagram',
    format='pdf',
    graph_attr={
        'rankdir': 'TB',      # Adjust based on Phase 1
        'splines': 'ortho',   # Clean orthogonal edges
        'nodesep': '0.6',     # Good default spacing
        'ranksep': '0.8',
        'bgcolor': 'white',
        'dpi': '300'
    },
    node_attr={
        'shape': 'box',
        'style': 'rounded,filled',
        'fillcolor': 'lightgray',
        'fontname': 'Arial',
        'fontsize': '11'
    },
    edge_attr={'color': 'black', 'penwidth': '1.5'}
)

# 3. Add nodes (with descriptive IDs and clear labels)
dot.node('input', 'Input Layer', fillcolor='#E8F4F8')
dot.node('hidden', 'Hidden Layer', fillcolor='#B3D9E6')
dot.node('output', 'Output Layer', fillcolor='#C8E6C9')

# 4. Add edges
dot.edge('input', 'hidden')
dot.edge('hidden', 'output')

# 5. Render to figures/ folder
output_path = f'{output_dir}/my_diagram'
dot.render(output_path, cleanup=True)  # Creates PDF
dot.format = 'svg'
dot.render(output_path, cleanup=True)  # Creates SVG
dot.format = 'eps'
dot.render(output_path, cleanup=True)  # Creates EPS

print(f"✓ Saved to: {output_path}.{{pdf,svg,eps}}")
```

### Phase 3: Quality Verification (5 minutes)

**Automatic checks:**
```python
# Convert PDF to PNG for quality checking
from pdf2image import convert_from_path

pages = convert_from_path(f'{output_path}.pdf', dpi=300)
pages[0].save(f'{output_path}.png')

# Run quality checks
from quality_checker import run_quality_checks
report = run_quality_checks(f'{output_path}.png')

if report['overall_status'] != 'PASS':
    print("⚠️ Issues detected - review quality_reports/")
    # Adjust spacing: increase nodesep or ranksep
    # Adjust colors: check accessibility report
else:
    print("✓ Quality checks passed!")
```

**Manual verification:**
1. Open PDF in viewer - check for overlaps
2. Verify text is readable (zoom to 100%)
3. Check alignment and spacing looks professional
4. Ensure colors are distinguishable

### Phase 4: LaTeX Integration (2 minutes)

**In your LaTeX document:**

```latex
% In preamble
\usepackage{graphicx}

% In document
\begin{figure}[htbp]
\centering
\includegraphics[width=0.8\textwidth]{figures/my_diagram.pdf}
\caption{Clear, descriptive caption explaining all components and abbreviations.
         Define any non-standard notation used in the diagram.}
\label{fig:my_diagram}
\end{figure}

% Reference in text
As shown in Figure~\ref{fig:my_diagram}, the architecture consists of...
```

**For posters (beamer):**
```latex
\begin{frame}{Architecture}
\begin{center}
\includegraphics[width=0.9\textwidth]{figures/my_diagram.pdf}
\end{center}
\end{frame}
```

### Phase 5: Version Control (1 minute)

**Always commit:**
1. Python source code (`create_my_diagram.py`)
2. Generated outputs (`figures/my_diagram.{pdf,svg,eps}`)
3. Quality reports (`my_diagram_quality_reports/`)

```bash
git add create_my_diagram.py
git add figures/my_diagram.*
git add my_diagram_quality_reports/
git commit -m "Add architecture diagram with quality verification"
```

## Troubleshooting Common Issues

### Graphviz-Specific Problems

**Problem:** Nodes overlap or are too close
```python
# Solution: Increase spacing
graph_attr={
    'nodesep': '1.0',   # Increase from default 0.6
    'ranksep': '1.2'    # Increase from default 0.8
}
```

**Problem:** Edges cross in confusing ways
```python
# Solution 1: Use orthogonal splines
graph_attr={'splines': 'ortho'}

# Solution 2: Adjust rank direction
graph_attr={'rankdir': 'LR'}  # Try different directions
```

**Problem:** Labels are cut off or too small
```python
# Solution: Adjust node size and font
node_attr={
    'fontsize': '12',      # Increase from 11
    'margin': '0.3',       # More internal padding
    'width': '2.5',        # Wider boxes
    'height': '0.6'        # Taller boxes
}
```

**Problem:** Clusters/subgraphs not appearing
```python
# Solution: Cluster names MUST start with 'cluster_'
with dot.subgraph(name='cluster_encoder') as enc:  # ✓ Correct
    enc.attr(label='Encoder')

with dot.subgraph(name='encoder') as enc:  # ✗ Won't show as cluster
    enc.attr(label='Encoder')
```

**Problem:** Cross-cluster edges not working
```python
# Solution: Enable compound edges
dot.attr(compound='true')

# Then use lhead/ltail for cluster connections
dot.edge('node1', 'node2', lhead='cluster_decoder')
```

**Problem:** Graphviz not found error
```bash
# Solution: Install graphviz binary (not just Python package)
# macOS
brew install graphviz

# Ubuntu
sudo apt-get install graphviz

# Then install Python bindings
pip install graphviz
```

### Visual Quality Issues

**Problem:** Colors not colorblind-safe
```python
# Solution: Use Okabe-Ito palette
COLORS = {
    'blue': '#56B4E9',
    'green': '#009E73',
    'orange': '#E69F00',
    'purple': '#CC79A7'
}
dot.node('n1', 'Node', fillcolor=COLORS['blue'])
```

**Problem:** Text too small when printed
```python
# Solution: Increase font size and DPI
node_attr={'fontsize': '12'}  # Minimum 11-12 for print
graph_attr={'dpi': '300'}     # Publication quality
```

**Problem:** PDF too large
```python
# Solution 1: Use simpler edge routing
graph_attr={'splines': 'line'}  # Simpler than 'ortho'

# Solution 2: Reduce DPI for drafts
graph_attr={'dpi': '150'}  # For drafts only
```

### Workflow Issues

**Problem:** Need to regenerate diagram after changes
```python
# Solution: Make diagram generation a function
def create_diagram(params):
    # ... diagram code ...
    return output_path

# Easy to regenerate with different parameters
create_diagram({'nodesep': '0.8', 'ranksep': '1.0'})
```

**Problem:** Diagram doesn't match paper figures style
```python
# Solution: Create a reusable style configuration
PAPER_STYLE = {
    'graph_attr': {
        'rankdir': 'TB',
        'bgcolor': 'white',
        'dpi': '300'
    },
    'node_attr': {
        'fontname': 'Arial',
        'fontsize': '11',
        'style': 'rounded,filled',
        'fillcolor': '#E8F4F8'
    },
    'edge_attr': {
        'color': 'black',
        'penwidth': '1.5'
    }
}

# Use for all diagrams
dot = graphviz.Digraph(**PAPER_STYLE)
```

## Visual Verification and Quality Control

All diagrams undergo automated visual quality checks to prevent overlaps, ensure readability, and verify accessibility. This multi-stage verification process uses computer vision techniques to detect common issues.

### Stage 1: Overlap Detection

Automatically detect overlapping elements that reduce clarity:

```python
import numpy as np
from PIL import Image
import json
from pathlib import Path

def detect_overlaps(image_path, threshold=0.95):
    """
    Detect potential overlapping regions in a diagram.
    
    Args:
        image_path: Path to the rendered diagram (PNG/PDF)
        threshold: Similarity threshold for detecting overlaps (0-1)
        
    Returns:
        dict: Overlap report with locations and severity
    """
    # Load image
    img = Image.open(image_path).convert('RGB')
    img_array = np.array(img)
    
    # Detect dense regions (potential overlaps)
    gray = np.mean(img_array, axis=2)
    
    # Edge detection to find boundaries
    from scipy.ndimage import sobel
    edges_x = sobel(gray, axis=0)
    edges_y = sobel(gray, axis=1)
    edge_magnitude = np.hypot(edges_x, edges_y)
    
    # Find regions with high edge density (overlaps)
    from scipy.ndimage import label, find_objects
    binary_edges = edge_magnitude > np.percentile(edge_magnitude, 85)
    labeled_regions, num_features = label(binary_edges)
    
    overlaps = []
    slices = find_objects(labeled_regions)
    
    for i, slice_obj in enumerate(slices):
        if slice_obj is not None:
            region = edge_magnitude[slice_obj]
            density = np.mean(region)
            
            # High density suggests potential overlap
            if density > threshold * np.max(edge_magnitude):
                y_center = (slice_obj[0].start + slice_obj[0].stop) // 2
                x_center = (slice_obj[1].start + slice_obj[1].stop) // 2
                
                overlaps.append({
                    'region_id': i + 1,
                    'position': (x_center, y_center),
                    'density': float(density),
                    'severity': 'high' if density > 0.98 * np.max(edge_magnitude) else 'medium'
                })
    
    report = {
        'image': str(image_path),
        'overlaps_detected': len(overlaps),
        'overlap_regions': overlaps,
        'status': 'PASS' if len(overlaps) == 0 else 'WARNING'
    }
    
    return report

def save_overlap_report(report, output_path='overlap_report.json'):
    """Save overlap detection report to JSON."""
    with open(output_path, 'w') as f:
        json.dump(report, indent=2, fp=f)
    
    print(f"Overlap Report: {report['status']}")
    print(f"  - Overlaps detected: {report['overlaps_detected']}")
    if report['overlap_regions']:
        print("  - Regions requiring review:")
        for region in report['overlap_regions']:
            print(f"    * Region {region['region_id']}: "
                  f"Position {region['position']}, Severity: {region['severity']}")
```

### Stage 2: Contrast and Accessibility Verification

Ensure diagrams meet accessibility standards for colorblind readers:

```python
def verify_accessibility(image_path):
    """
    Verify diagram meets accessibility standards.
    
    Checks:
    - Sufficient contrast ratios
    - Grayscale readability
    - Text size adequacy
    """
    from PIL import ImageFilter, ImageStat
    
    img = Image.open(image_path).convert('RGB')
    
    # Test 1: Grayscale conversion
    grayscale = img.convert('L')
    gray_stat = ImageStat.Stat(grayscale)
    
    # Calculate contrast (std dev of grayscale)
    contrast = gray_stat.stddev[0]
    min_contrast = 30  # Minimum standard deviation for good contrast
    
    # Test 2: Color distribution
    rgb_array = np.array(img)
    unique_colors = len(np.unique(rgb_array.reshape(-1, 3), axis=0))
    
    # Test 3: Simulate common color blindness (deuteranopia)
    def simulate_colorblind(img_array):
        # Simplified deuteranopia simulation
        colorblind = img_array.copy().astype(float)
        colorblind[:, :, 0] = 0.625 * img_array[:, :, 0] + 0.375 * img_array[:, :, 1]
        colorblind[:, :, 1] = 0.7 * img_array[:, :, 1] + 0.3 * img_array[:, :, 0]
        return colorblind.astype(np.uint8)
    
    colorblind_img = simulate_colorblind(np.array(img))
    cb_image = Image.fromarray(colorblind_img)
    cb_gray = cb_image.convert('L')
    cb_stat = ImageStat.Stat(cb_gray)
    cb_contrast = cb_stat.stddev[0]
    
    report = {
        'image': str(image_path),
        'checks': {
            'grayscale_contrast': {
                'value': contrast,
                'threshold': min_contrast,
                'status': 'PASS' if contrast >= min_contrast else 'FAIL'
            },
            'colorblind_contrast': {
                'value': cb_contrast,
                'threshold': min_contrast * 0.8,
                'status': 'PASS' if cb_contrast >= min_contrast * 0.8 else 'FAIL'
            },
            'color_diversity': {
                'unique_colors': unique_colors,
                'status': 'INFO'
            }
        },
        'overall_status': 'PASS' if (contrast >= min_contrast and 
                                     cb_contrast >= min_contrast * 0.8) else 'FAIL'
    }
    
    return report

def save_accessibility_report(report, output_path='accessibility_report.json'):
    """Save accessibility report to JSON."""
    with open(output_path, 'w') as f:
        json.dump(report, indent=2, fp=f)
    
    print(f"Accessibility Report: {report['overall_status']}")
    for check_name, check_data in report['checks'].items():
        print(f"  - {check_name}: {check_data['status']}")
        if 'value' in check_data and 'threshold' in check_data:
            print(f"    Value: {check_data['value']:.2f}, Threshold: {check_data['threshold']:.2f}")
```

### Stage 3: Text Size and Resolution Validation

Verify text is readable at publication size:

```python
def validate_resolution(image_path, target_dpi=300, min_text_size_pt=7):
    """
    Validate image resolution and estimated text size.
    
    Args:
        image_path: Path to diagram image
        target_dpi: Target DPI for publication (default 300)
        min_text_size_pt: Minimum acceptable text size in points
    """
    from PIL import Image
    import pytesseract
    
    img = Image.open(image_path)
    
    # Check DPI
    dpi = img.info.get('dpi', (72, 72))
    actual_dpi = dpi[0] if isinstance(dpi, tuple) else dpi
    
    # Estimate text size (simplified - assumes text detection)
    # For production, use OCR or PDF text extraction
    width, height = img.size
    dpi_ratio = actual_dpi / 72  # Convert to screen pixels
    
    # Calculate physical size in inches
    width_inches = width / actual_dpi if actual_dpi > 0 else width / 72
    height_inches = height / actual_dpi if actual_dpi > 0 else height / 72
    
    report = {
        'image': str(image_path),
        'resolution': {
            'dpi': actual_dpi,
            'target_dpi': target_dpi,
            'status': 'PASS' if actual_dpi >= target_dpi else 'WARNING'
        },
        'dimensions': {
            'pixels': {'width': width, 'height': height},
            'inches': {'width': round(width_inches, 2), 
                      'height': round(height_inches, 2)}
        },
        'recommendations': []
    }
    
    if actual_dpi < target_dpi:
        report['recommendations'].append(
            f"Increase resolution to {target_dpi} DPI for publication quality"
        )
    
    if width_inches > 7:
        report['recommendations'].append(
            "Image width exceeds typical single-column width (7 inches)"
        )
    
    return report
```

### Stage 4: Comprehensive Quality Check Pipeline

Run all verification stages in sequence:

```python
def run_quality_checks(image_path, output_dir='quality_reports'):
    """
    Run comprehensive quality checks on diagram.
    
    Args:
        image_path: Path to diagram to verify
        output_dir: Directory to save reports
        
    Returns:
        dict: Comprehensive quality report
    """
    import os
    from datetime import datetime
    
    Path(output_dir).mkdir(exist_ok=True)
    
    print(f"Running quality checks on: {image_path}")
    print("=" * 60)
    
    # Stage 1: Overlap Detection
    print("\n[Stage 1/4] Detecting overlaps...")
    overlap_report = detect_overlaps(image_path)
    save_overlap_report(
        overlap_report, 
        f"{output_dir}/overlap_report.json"
    )
    
    # Stage 2: Accessibility
    print("\n[Stage 2/4] Verifying accessibility...")
    accessibility_report = verify_accessibility(image_path)
    save_accessibility_report(
        accessibility_report,
        f"{output_dir}/accessibility_report.json"
    )
    
    # Stage 3: Resolution
    print("\n[Stage 3/4] Validating resolution...")
    resolution_report = validate_resolution(image_path)
    with open(f"{output_dir}/resolution_report.json", 'w') as f:
        json.dump(resolution_report, f, indent=2)
    
    # Stage 4: Generate visual report
    print("\n[Stage 4/4] Generating visual report...")
    create_visual_report(
        image_path,
        overlap_report,
        accessibility_report,
        f"{output_dir}/visual_report.png"
    )
    
    # Comprehensive summary
    all_pass = (
        overlap_report['status'] != 'FAIL' and
        accessibility_report['overall_status'] != 'FAIL' and
        resolution_report['resolution']['status'] != 'FAIL'
    )
    
    summary = {
        'timestamp': datetime.now().isoformat(),
        'image': str(image_path),
        'overall_status': 'PASS' if all_pass else 'NEEDS REVIEW',
        'stage_results': {
            'overlap_detection': overlap_report['status'],
            'accessibility': accessibility_report['overall_status'],
            'resolution': resolution_report['resolution']['status']
        },
        'reports_saved_to': output_dir
    }
    
    with open(f"{output_dir}/summary.json", 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("\n" + "=" * 60)
    print(f"OVERALL STATUS: {summary['overall_status']}")
    print(f"Reports saved to: {output_dir}/")
    print("=" * 60)
    
    return summary

def create_visual_report(image_path, overlap_report, accessibility_report, output_path):
    """Create visual report with annotations."""
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Load original image
    img = Image.open(image_path)
    
    # Panel 1: Original with overlap markers
    axes[0].imshow(img)
    axes[0].set_title('Overlap Detection', fontsize=12, fontweight='bold')
    if overlap_report['overlap_regions']:
        for region in overlap_report['overlap_regions']:
            x, y = region['position']
            color = 'red' if region['severity'] == 'high' else 'orange'
            circle = Circle((x, y), 20, color=color, fill=False, linewidth=2)
            axes[0].add_patch(circle)
    axes[0].axis('off')
    axes[0].text(0.02, 0.98, f"Status: {overlap_report['status']}", 
                transform=axes[0].transAxes, fontsize=10,
                verticalalignment='top', bbox=dict(boxstyle='round', 
                facecolor='wheat', alpha=0.5))
    
    # Panel 2: Grayscale version
    gray_img = img.convert('L')
    axes[1].imshow(gray_img, cmap='gray')
    axes[1].set_title('Grayscale Preview', fontsize=12, fontweight='bold')
    axes[1].axis('off')
    gray_status = accessibility_report['checks']['grayscale_contrast']['status']
    axes[1].text(0.02, 0.98, f"Status: {gray_status}", 
                transform=axes[1].transAxes, fontsize=10,
                verticalalignment='top', bbox=dict(boxstyle='round', 
                facecolor='wheat', alpha=0.5))
    
    # Panel 3: Colorblind simulation
    img_array = np.array(img)
    colorblind = img_array.copy().astype(float)
    colorblind[:, :, 0] = 0.625 * img_array[:, :, 0] + 0.375 * img_array[:, :, 1]
    colorblind[:, :, 1] = 0.7 * img_array[:, :, 1] + 0.3 * img_array[:, :, 0]
    axes[2].imshow(colorblind.astype(np.uint8))
    axes[2].set_title('Colorblind Simulation', fontsize=12, fontweight='bold')
    axes[2].axis('off')
    cb_status = accessibility_report['checks']['colorblind_contrast']['status']
    axes[2].text(0.02, 0.98, f"Status: {cb_status}", 
                transform=axes[2].transAxes, fontsize=10,
                verticalalignment='top', bbox=dict(boxstyle='round', 
                facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"Visual report saved: {output_path}")
    plt.close()
```

### Usage Example: Complete Workflow with Verification

Here's how to create a diagram with full quality verification:

```python
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# Step 1: Create diagram
def create_flowchart_with_verification(output_base='flowchart'):
    """Create flowchart with automated quality checks."""
    
    # Okabe-Ito colorblind-safe palette
    colors = {
        'process': '#56B4E9',    # Blue
        'decision': '#E69F00',   # Orange
        'data': '#009E73',       # Green
        'terminal': '#CC79A7'    # Purple
    }
    
    fig, ax = plt.subplots(figsize=(8, 10))
    
    # Define flowchart elements with careful spacing
    elements = [
        ('Start', 4, 9, 'terminal'),
        ('Input Data', 4, 7.5, 'data'),
        ('Process A', 4, 6, 'process'),
        ('Decision?', 4, 4.5, 'decision'),
        ('Process B1', 2, 3, 'process'),
        ('Process B2', 6, 3, 'process'),
        ('Output', 4, 1.5, 'data'),
        ('End', 4, 0, 'terminal')
    ]
    
    # Draw boxes with adequate spacing
    box_positions = {}
    for label, x, y, element_type in elements:
        color = colors[element_type]
        width, height = (1.2, 0.6) if element_type != 'decision' else (1.5, 1.0)
        
        box = FancyBboxPatch(
            (x - width/2, y - height/2), width, height,
            boxstyle="round,pad=0.1" if element_type != 'decision' else "round,pad=0.05",
            facecolor=color, edgecolor='black', linewidth=2
        )
        ax.add_patch(box)
        ax.text(x, y, label, ha='center', va='center', 
               fontsize=10, fontweight='bold')
        box_positions[label] = (x, y)
    
    # Draw arrows with proper spacing
    arrows = [
        ('Start', 'Input Data'),
        ('Input Data', 'Process A'),
        ('Process A', 'Decision?'),
        ('Decision?', 'Process B1'),
        ('Decision?', 'Process B2'),
        ('Process B1', 'Output'),
        ('Process B2', 'Output'),
        ('Output', 'End')
    ]
    
    for start, end in arrows:
        x1, y1 = box_positions[start]
        x2, y2 = box_positions[end]
        
        # Calculate arrow start/end points to avoid overlap
        if x1 == x2:  # Vertical arrow
            y1_adj = y1 - 0.3 if y2 < y1 else y1 + 0.3
            y2_adj = y2 + 0.3 if y2 < y1 else y2 - 0.3
            arrow = FancyArrowPatch(
                (x1, y1_adj), (x2, y2_adj),
                arrowstyle='->', mutation_scale=20, linewidth=2, color='black'
            )
        else:  # Diagonal arrow
            arrow = FancyArrowPatch(
                (x1, y1 - 0.5), (x2, y2 + 0.3),
                arrowstyle='->', mutation_scale=20, linewidth=2, color='black'
            )
        ax.add_patch(arrow)
    
    ax.set_xlim(0, 8)
    ax.set_ylim(-0.5, 9.5)
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.tight_layout()
    
    # Save in multiple formats
    plt.savefig(f'{output_base}.pdf', bbox_inches='tight', dpi=300)
    plt.savefig(f'{output_base}.png', bbox_inches='tight', dpi=300)
    plt.savefig(f'{output_base}.svg', bbox_inches='tight')
    print(f"Diagram saved: {output_base}.pdf/.png/.svg")
    plt.close()
    
    # Step 2: Run quality checks
    print("\nRunning quality verification...")
    quality_report = run_quality_checks(
        f'{output_base}.png',
        output_dir=f'{output_base}_quality_reports'
    )
    
    # Step 3: Review and iterate if needed
    if quality_report['overall_status'] != 'PASS':
        print("\n⚠️  Diagram needs review. Check quality reports for details.")
        return False
    else:
        print("\n✓ Diagram passed all quality checks!")
        return True

# Run complete workflow
if __name__ == '__main__':
    success = create_flowchart_with_verification('my_flowchart')
```

### Iterative Refinement Loop

For complex diagrams, use an iterative refinement process:

```python
def iterative_diagram_refinement(create_function, max_iterations=3):
    """
    Iteratively refine diagram until it passes quality checks.
    
    Args:
        create_function: Function that creates and saves diagram
        max_iterations: Maximum refinement attempts
    """
    for iteration in range(1, max_iterations + 1):
        print(f"\n{'='*60}")
        print(f"ITERATION {iteration}/{max_iterations}")
        print(f"{'='*60}")
        
        # Create diagram
        diagram_path = create_function(iteration)
        
        # Run checks
        quality_report = run_quality_checks(
            diagram_path,
            output_dir=f'iteration_{iteration}_reports'
        )
        
        if quality_report['overall_status'] == 'PASS':
            print(f"\n✓ Diagram approved after {iteration} iteration(s)")
            return True
        else:
            print(f"\n⚠️  Issues found. Adjusting parameters for next iteration...")
            # Here you would adjust spacing, colors, etc. based on reports
    
    print(f"\n❌ Maximum iterations reached. Manual review required.")
    return False
```

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

The `scripts/` directory contains Python utilities for automated diagram generation and quality verification:

### `generate_flowchart.py`

Convert text descriptions into TikZ flowcharts with automatic quality checks:

```python
from scripts.generate_flowchart import text_to_flowchart, create_with_verification

description = """
1. Screen participants (n=500)
2. Exclude if age < 18 (n=150)
3. Randomize remaining (n=350)
4. Treatment group (n=175)
5. Control group (n=175)
6. Follow up at 3 months
7. Analyze data
"""

# Generate TikZ code
tikz_code = text_to_flowchart(description)
with open('methodology_flow.tex', 'w') as f:
    f.write(tikz_code)

# Or create with automatic verification
success = create_with_verification(
    description, 
    output='methodology_flow',
    verify=True
)
```

### `circuit_generator.py`

Generate circuit diagrams using Schemdraw with quality verification:

```python
from scripts.circuit_generator import CircuitBuilder

builder = CircuitBuilder()
builder.add_voltage_source('Vs', '5V')
builder.add_resistor('R1', '1kΩ')
builder.add_capacitor('C1', '10µF')
builder.add_ground()

# Save with automatic quality checks
builder.save('circuit.pdf', verify=True)

# Access quality report
print(builder.quality_report)
```

### `pathway_diagram.py`

Create biological pathway diagrams with overlap detection:

```python
from scripts.pathway_diagram import PathwayGenerator

gen = PathwayGenerator(
    colorblind_safe=True,
    auto_spacing=True  # Automatically adjust spacing to prevent overlaps
)

gen.add_node('Receptor', type='protein', position=(1, 5))
gen.add_node('Kinase', type='protein', position=(3, 5))
gen.add_edge('Receptor', 'Kinase', interaction='activation')

# Save with quality verification
quality_report = gen.save('pathway.pdf', verify=True)

# Iteratively refine if needed
if quality_report['status'] != 'PASS':
    gen.auto_adjust_spacing()
    gen.save('pathway.pdf', verify=True)
```

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

### `quality_checker.py`

Standalone quality verification tool for any diagram:

```bash
# Check single diagram
python scripts/quality_checker.py diagram.png

# Check with detailed report
python scripts/quality_checker.py diagram.png --detailed --output-dir reports/

# Batch check multiple diagrams
python scripts/quality_checker.py figures/*.png --batch

# Export visual comparison report
python scripts/quality_checker.py diagram.png --visual-report
```

```python
# Python API
from scripts.quality_checker import DiagramQualityChecker

checker = DiagramQualityChecker()

# Run all checks
report = checker.check_diagram('diagram.png')

# Access specific checks
overlap_report = checker.check_overlaps('diagram.png')
accessibility_report = checker.check_accessibility('diagram.png')
resolution_report = checker.check_resolution('diagram.png')

# Generate visual report
checker.create_visual_report('diagram.png', output='quality_report.png')

# Batch processing
results = checker.batch_check(['fig1.png', 'fig2.png', 'fig3.png'])
checker.save_batch_report(results, 'batch_quality_report.json')
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
- **Solution**: Run quality checker to identify overlaps: `python scripts/quality_checker.py diagram.png`
- **Solution**: Increase `node distance`, adjust positioning manually based on overlap report
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
- **Solution**: Increase DPI: `plt.savefig(..., dpi=300, bbox_inches='tight')`
- **Solution**: Run resolution checker: `quality_checker.check_resolution(image_path, target_dpi=300)`

**Problem**: Elements overlap after generation
- **Solution**: Run `detect_overlaps()` function to identify problem regions
- **Solution**: Use iterative refinement: `iterative_diagram_refinement(create_function)`
- **Solution**: Increase spacing between elements by 20-30%

### Quality Check Issues

**Problem**: False positive overlap detection
- **Solution**: Adjust threshold: `detect_overlaps(image_path, threshold=0.98)`
- **Solution**: Manually review flagged regions in visual report

**Problem**: Quality checker fails on PDF files
- **Solution**: Convert PDF to PNG first: `from pdf2image import convert_from_path`
- **Solution**: Use PNG output format for quality checks

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
- [ ] Vector format (PDF/SVG) or 300+ DPI raster
- [ ] No overlapping elements (verified by quality checker)
- [ ] Adequate spacing between all components
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

Use this skill to create clear, accessible, publication-quality diagrams that effectively communicate complex scientific concepts. The integrated quality verification workflow ensures all diagrams meet professional standards before publication.

