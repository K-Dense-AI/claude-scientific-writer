# Python Libraries for Scientific Diagram Generation

## Overview

This guide covers Python libraries for programmatic generation of scientific diagrams: Schemdraw for circuit diagrams, NetworkX for network diagrams, and Matplotlib for custom diagrams. These tools enable data-driven diagram creation, batch generation, and integration with scientific workflows.

## Installation

```bash
# Install all diagram-related packages
pip install schemdraw networkx matplotlib numpy

# Optional for enhanced features
pip install pygraphviz  # Better NetworkX layouts (requires Graphviz)
pip install pillow      # Image export options
```

## Schemdraw: Circuit and Electrical Diagrams

### Overview

Schemdraw creates publication-quality electrical schematics with an intuitive Python API. Perfect for electronics papers, instrumentation descriptions, and signal processing diagrams.

**Official Documentation**: https://schemdraw.readthedocs.io/

### Basic Usage

```python
import schemdraw
import schemdraw.elements as elm

# Create drawing
d = schemdraw.Drawing()

# Add components
d += elm.SourceV().label('5V')
d += elm.Resistor().right().label('1kΩ')
d += elm.Capacitor().down().label('10µF')
d += elm.Line().left()
d += elm.Ground()

# Display or save
d.save('circuit.pdf')
d.save('circuit.svg')
d.save('circuit.png', dpi=300)
```

### Core Concepts

**Element Addition**
```python
# Add elements with +=
d += elm.Resistor()

# Chain methods for placement
d += elm.Resistor().right().label('R1')

# Positioning
d += elm.Capacitor().down()   # Go down
d += elm.Resistor().left()    # Go left
d += elm.Diode().up()          # Go up
d += elm.Resistor().right()    # Go right (default)
```

**Connections and Flow**
```python
# Schemdraw maintains current position
d += elm.Resistor()            # From current pos, going right
d += elm.Capacitor().down()    # From end of resistor, going down
d += elm.Line().left()         # From end of capacitor, going left

# Return to a saved position
r1 = d.add(elm.Resistor())
d += elm.Capacitor().down()
d += elm.Line().to(r1.start)  # Connect back to start of r1
```

**Labeling**
```python
# Simple label
d += elm.Resistor().label('1kΩ')

# Label position
d += elm.Resistor().label('R1', loc='top')     # Above
d += elm.Resistor().label('1kΩ', loc='bottom') # Below

# Multiple labels
d += elm.Resistor().label('R1', loc='top').label('1kΩ', loc='bottom')

# Math notation
d += elm.Capacitor().label('$C_1$')
d += elm.Resistor().label('$R_{load}$')
```

### Common Components

**Passive Components**
```python
# Resistors
d += elm.Resistor()
d += elm.ResistorVar()         # Variable resistor
d += elm.Potentiometer()

# Capacitors
d += elm.Capacitor()
d += elm.Capacitor().flip()    # Flip polarity
d += elm.CapacitorVar()        # Variable capacitor

# Inductors
d += elm.Inductor()
d += elm.Inductor2()           # Alternative symbol

# Other passives
d += elm.Diode()
d += elm.DiodeZener()
d += elm.LED()
```

**Sources**
```python
# Voltage sources
d += elm.SourceV().label('V')
d += elm.SourceSin().label('~')
d += elm.SourceSquare()

# Current sources
d += elm.SourceI().label('I')
d += elm.SourceControlled().label('V_c')
```

**Active Components**
```python
# Transistors
d += elm.BjtNpn()
d += elm.BjtPnp()
d += elm.NFet()
d += elm.PFet()

# Op-amps
d += elm.Opamp()

# Integrated circuits
d += elm.Ic(pins=[...])  # Custom pin configuration
```

**Measurement and Misc**
```python
# Meters
d += elm.Meter().label('V')
d += elm.Ammeter()

# Switches
d += elm.Switch()
d += elm.SwitchDpst()

# Ground and reference
d += elm.Ground()
d += elm.GroundSignal()
```

### Advanced Techniques

**Precise Positioning with .at()**
```python
# Position at specific coordinate
d += elm.Resistor().at((2, 3))

# Position at another element
r1 = d.add(elm.Resistor())
d += elm.Capacitor().at(r1.end)
```

**Anchor Points**
```python
# Most elements have .start, .end, .center
r1 = d.add(elm.Resistor())
d += elm.Line().at(r1.center).down()
```

**Angles and Rotation**
```python
# Rotate element
d += elm.Resistor().theta(45)  # 45 degrees

# Diagonal connections
d += elm.Resistor().to((5, 3))  # Go to specific point
```

**Dot Markers for Junctions**
```python
# Add dot at junction
d += elm.Dot()

# Dot at element position
d += elm.Dot().at(r1.end)
```

**Styling and Color**
```python
# Color (use colorblind-safe palette)
d += elm.Resistor().color('#E69F00')  # Okabe-Ito orange

# Line width
d += elm.Resistor().linewidth(2)

# Fill
d += elm.Capacitor().fill('#56B4E9')  # Okabe-Ito blue
```

### Complete Example: RC Filter

```python
import schemdraw
import schemdraw.elements as elm

# Publication styling
d = schemdraw.Drawing(fontsize=10, font='Arial')

# Input
d += elm.Dot().label('$V_{in}$', loc='left')
d += elm.Resistor().right().label('$R$\n1kΩ', loc='top')

# Junction
d += elm.Dot()
d.push()  # Save position

# Capacitor to ground
d += elm.Capacitor().down().label('$C$\n10µF', loc='right')
d += elm.Ground()

# Output
d.pop()  # Return to saved position
d += elm.Line().right()
d += elm.Dot().label('$V_{out}$', loc='right')

# Save
d.save('rc_filter.pdf')
d.save('rc_filter.png', dpi=300)
```

### Export Options

```python
# Vector formats (preferred)
d.save('diagram.svg')
d.save('diagram.pdf')

# Raster format
d.save('diagram.png', dpi=300)

# Display in Jupyter
d.draw()

# Get matplotlib Figure for further customization
fig = d.draw()
# Can now use matplotlib commands on fig
```

## NetworkX: Network and Graph Diagrams

### Overview

NetworkX creates, analyzes, and visualizes complex networks and graphs. Ideal for collaboration networks, protein interactions, citations, and any relationship data.

**Official Documentation**: https://networkx.org/

### Basic Usage

```python
import networkx as nx
import matplotlib.pyplot as plt

# Create graph
G = nx.Graph()

# Add nodes and edges
G.add_nodes_from([1, 2, 3, 4])
G.add_edges_from([(1, 2), (1, 3), (2, 4), (3, 4)])

# Draw
nx.draw(G, with_labels=True)
plt.savefig('network.pdf')
```

### Graph Creation

**Undirected Graphs**
```python
G = nx.Graph()
G.add_edge('A', 'B')  # Adds nodes automatically
G.add_edge('B', 'C')
G.add_edge('C', 'A')
```

**Directed Graphs**
```python
G = nx.DiGraph()
G.add_edge('Gene1', 'Protein1')  # Gene1 -> Protein1
G.add_edge('Protein1', 'Gene2')
```

**Weighted Graphs**
```python
G = nx.Graph()
G.add_edge('A', 'B', weight=0.5)
G.add_edge('B', 'C', weight=0.8)
G.add_edge('C', 'A', weight=0.3)
```

**From Data**
```python
import pandas as pd

# From edge list DataFrame
df = pd.DataFrame({
    'source': ['A', 'B', 'C'],
    'target': ['B', 'C', 'A'],
    'weight': [0.5, 0.8, 0.3]
})

G = nx.from_pandas_edgelist(df, source='source', target='target', 
                            edge_attr='weight')
```

### Layout Algorithms

**Spring Layout (Force-Directed)**
```python
pos = nx.spring_layout(G, k=0.5, iterations=50)
nx.draw(G, pos, with_labels=True)
```

**Circular Layout**
```python
pos = nx.circular_layout(G)
nx.draw(G, pos, with_labels=True)
```

**Hierarchical Layout**
```python
# Requires pygraphviz
pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
nx.draw(G, pos, with_labels=True)
```

**Shell Layout (Concentric)**
```python
# Define shells (groups of nodes)
shells = [['A', 'B'], ['C', 'D', 'E']]
pos = nx.shell_layout(G, nlist=shells)
nx.draw(G, pos, with_labels=True)
```

**Manual Positioning**
```python
pos = {
    'A': (0, 0),
    'B': (1, 1),
    'C': (2, 0),
    'D': (1, -1)
}
nx.draw(G, pos, with_labels=True)
```

### Styling Networks

**Node Styling**
```python
# Colorblind-safe Okabe-Ito palette
okabe_ito = ['#E69F00', '#56B4E9', '#009E73', '#F0E442',
             '#0072B2', '#D55E00', '#CC79A7', '#000000']

# Color by attribute
node_colors = [okabe_ito[G.nodes[node]['type']] for node in G.nodes()]

# Size by degree
node_sizes = [300 * G.degree(node) for node in G.nodes()]

nx.draw(G, pos,
        node_color=node_colors,
        node_size=node_sizes,
        with_labels=True,
        font_size=10,
        font_family='Arial')
```

**Edge Styling**
```python
# Edge width by weight
edges = G.edges()
weights = [G[u][v]['weight'] for u, v in edges]
widths = [w * 3 for w in weights]  # Scale for visibility

nx.draw_networkx_edges(G, pos, width=widths, alpha=0.6, 
                        edge_color='#56B4E9')
```

**Labels**
```python
# Node labels
nx.draw_networkx_labels(G, pos, font_size=10, font_family='Arial')

# Edge labels
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8)
```

### Publication-Quality Network Diagram

```python
import networkx as nx
import matplotlib.pyplot as plt

# Create graph
G = nx.Graph()
G.add_edges_from([
    ('A', 'B', {'weight': 0.8}),
    ('A', 'C', {'weight': 0.5}),
    ('B', 'D', {'weight': 0.7}),
    ('C', 'D', {'weight': 0.6}),
])

# Layout
pos = nx.spring_layout(G, k=1, iterations=50, seed=42)

# Create figure
fig, ax = plt.subplots(figsize=(6, 6))

# Okabe-Ito colors
colors = ['#E69F00', '#56B4E9', '#009E73', '#F0E442']
node_colors = {node: colors[i] for i, node in enumerate(G.nodes())}

# Draw edges
edges = G.edges()
weights = [G[u][v]['weight'] for u, v in edges]
nx.draw_networkx_edges(G, pos, width=[w*5 for w in weights],
                        alpha=0.5, edge_color='#666666', ax=ax)

# Draw nodes
nx.draw_networkx_nodes(G, pos, 
                       node_color=[node_colors[n] for n in G.nodes()],
                       node_size=800, 
                       edgecolors='black', 
                       linewidths=2, 
                       ax=ax)

# Draw labels
nx.draw_networkx_labels(G, pos, font_size=12, font_family='Arial',
                        font_weight='bold', ax=ax)

# Formatting
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)
ax.axis('off')

plt.tight_layout()
plt.savefig('network.pdf', bbox_inches='tight')
plt.savefig('network.png', dpi=300, bbox_inches='tight')
```

## Matplotlib Patches: Custom Diagrams

### Overview

Matplotlib's patches module provides geometric shapes for building custom diagrams: rectangles, circles, arrows, polygons. Perfect for biological pathways, custom flowcharts, and conceptual diagrams.

### Basic Shapes

**Rectangle**
```python
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, ax = plt.subplots(figsize=(8, 6))

# Create rectangle: (x, y, width, height)
rect = mpatches.Rectangle((0.2, 0.5), 0.3, 0.2, 
                           facecolor='#56B4E9', 
                           edgecolor='black', 
                           linewidth=2)
ax.add_patch(rect)

# Add text
ax.text(0.35, 0.6, 'Process', ha='center', va='center', 
        fontsize=12, fontweight='bold')

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')
plt.show()
```

**Circle**
```python
# Circle: (center_x, center_y), radius
circle = mpatches.Circle((0.5, 0.5), 0.1, 
                          facecolor='#E69F00', 
                          edgecolor='black', 
                          linewidth=2)
ax.add_patch(circle)
```

**Ellipse**
```python
# Ellipse: (center_x, center_y), width, height
ellipse = mpatches.Ellipse((0.5, 0.5), 0.3, 0.2,
                            facecolor='#009E73',
                            edgecolor='black',
                            linewidth=2)
ax.add_patch(ellipse)
```

**Polygon**
```python
# Polygon: list of (x, y) coordinates
triangle = mpatches.Polygon([(0.3, 0.2), (0.7, 0.2), (0.5, 0.6)],
                             facecolor='#F0E442',
                             edgecolor='black',
                             linewidth=2)
ax.add_patch(triangle)
```

**Rounded Rectangle (FancyBboxPatch)**
```python
from matplotlib.patches import FancyBboxPatch

rounded_rect = FancyBboxPatch((0.2, 0.5), 0.3, 0.2,
                               boxstyle="round,pad=0.02",
                               facecolor='#0072B2',
                               edgecolor='black',
                               linewidth=2)
ax.add_patch(rounded_rect)
```

### Arrows and Connections

**FancyArrowPatch**
```python
from matplotlib.patches import FancyArrowPatch

# Arrow from (x1, y1) to (x2, y2)
arrow = FancyArrowPatch((0.2, 0.5), (0.7, 0.5),
                        arrowstyle='->', 
                        mutation_scale=20,
                        linewidth=2,
                        color='black')
ax.add_patch(arrow)
```

**Arrow Styles**
```python
# Different arrow styles
'->'   # Standard arrow
'->>'  # Double arrow
'-|>'  # Fancy arrow
'<->'  # Double-headed
'-['   # Bracket
'|-|'  # Bar-bar
'fancy'  # Fancy, customizable
```

**Curved Arrows**
```python
# Curved connection
arrow = FancyArrowPatch((0.2, 0.5), (0.7, 0.8),
                        arrowstyle='->',
                        connectionstyle="arc3,rad=0.3",  # Curvature
                        mutation_scale=20,
                        linewidth=2,
                        color='black')
ax.add_patch(arrow)
```

### Biological Pathway Example

```python
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# Okabe-Ito palette
colors = {
    'protein': '#56B4E9',
    'gene': '#009E73',
    'metabolite': '#F0E442'
}

fig, ax = plt.subplots(figsize=(10, 6))

# Define proteins
proteins = [
    ('Receptor', 1, 4, 'protein'),
    ('Kinase A', 3, 4, 'protein'),
    ('Kinase B', 5, 4, 'protein'),
    ('TF', 7, 4, 'protein'),
    ('Gene', 7, 2, 'gene')
]

# Draw proteins/genes
for name, x, y, ptype in proteins:
    if ptype == 'gene':
        # Genes as rectangles
        box = mpatches.Rectangle((x-0.4, y-0.25), 0.8, 0.5,
                                  facecolor=colors[ptype],
                                  edgecolor='black',
                                  linewidth=2)
    else:
        # Proteins as rounded rectangles
        box = FancyBboxPatch((x-0.4, y-0.25), 0.8, 0.5,
                             boxstyle="round,pad=0.05",
                             facecolor=colors[ptype],
                             edgecolor='black',
                             linewidth=2)
    ax.add_patch(box)
    ax.text(x, y, name, ha='center', va='center',
            fontsize=10, fontweight='bold', fontfamily='Arial')

# Activation arrows
activations = [
    (1.5, 4, 2.5, 4),   # Receptor -> Kinase A
    (3.5, 4, 4.5, 4),   # Kinase A -> Kinase B
    (5.5, 4, 6.5, 4),   # Kinase B -> TF
    (7, 3.75, 7, 2.6)   # TF -> Gene
]

for x1, y1, x2, y2 in activations:
    arrow = FancyArrowPatch((x1, y1), (x2, y2),
                           arrowstyle='->', mutation_scale=20,
                           linewidth=2.5, color='black')
    ax.add_patch(arrow)

# Format
ax.set_xlim(0, 8.5)
ax.set_ylim(1, 5)
ax.set_aspect('equal')
ax.axis('off')

plt.tight_layout()
plt.savefig('signaling_pathway.pdf', bbox_inches='tight')
plt.savefig('signaling_pathway.png', dpi=300, bbox_inches='tight')
```

## Integrating with LaTeX

### Matplotlib LaTeX Rendering

```python
import matplotlib.pyplot as plt

# Enable LaTeX text rendering
plt.rcParams['text.usetex'] = True
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10

# Use LaTeX in labels
ax.text(0.5, 0.5, r'$\alpha + \beta = \gamma$', fontsize=12)
ax.set_xlabel(r'Time $t$ (seconds)')
ax.set_ylabel(r'$\Delta$ Temperature ($^\circ$C)')
```

### PGF Backend for Perfect LaTeX Integration

```python
import matplotlib
matplotlib.use('pgf')
import matplotlib.pyplot as plt

# Configure PGF
plt.rcParams.update({
    'pgf.texsystem': 'pdflatex',
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})

# Create figure
fig, ax = plt.subplots()
# ... plotting code ...

# Save as PGF (can be included in LaTeX)
plt.savefig('diagram.pgf')
```

Then in LaTeX:
```latex
\begin{figure}
  \centering
  \input{diagram.pgf}
  \caption{My diagram}
\end{figure}
```

## Best Practices

### 1. Colorblind-Safe Palettes

```python
# Okabe-Ito palette (use this!)
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

# Use in diagrams
node_color = OKABE_ITO['blue']
edge_color = OKABE_ITO['orange']
```

### 2. Publication-Quality Settings

```python
import matplotlib.pyplot as plt

# Set publication defaults
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica']
plt.rcParams['font.size'] = 8
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['pdf.fonttype'] = 42  # TrueType fonts in PDF
plt.rcParams['ps.fonttype'] = 42

# Save with proper settings
fig.savefig('diagram.pdf', dpi=300, bbox_inches='tight',
            pad_inches=0.05, transparent=False)
```

### 3. Consistent Sizing

```python
# Design at final size
# Single column: 3.5 inches
# Double column: 7.0 inches

fig, ax = plt.subplots(figsize=(3.5, 2.5))  # Single column
# or
fig, ax = plt.subplots(figsize=(7.0, 4.0))  # Double column
```

### 4. Vector Output

```python
# Always prefer vector formats
d.save('circuit.pdf')      # Schemdraw
plt.savefig('network.svg') # NetworkX/Matplotlib

# Raster only as fallback
plt.savefig('diagram.png', dpi=300)
```

## Troubleshooting

**Issue**: Fonts not embedded in PDF
```python
# Solution: Set fonttype to TrueType
plt.rcParams['pdf.fonttype'] = 42
```

**Issue**: Text appears pixelated
```python
# Solution: Use vector format or higher DPI
plt.savefig('fig.png', dpi=300)  # or use PDF
```

**Issue**: NetworkX layout looks messy
```python
# Solution: Try different layouts or manual positioning
pos = nx.spring_layout(G, k=2, iterations=100, seed=42)
# Increase k for more spacing, set seed for reproducibility
```

**Issue**: Schemdraw elements not connecting
```python
# Solution: Use .to() or .at() for precise positioning
d += elm.Line().to(other_element.end)
```

## Further Resources

- **Schemdraw**: https://schemdraw.readthedocs.io/
- **NetworkX**: https://networkx.org/documentation/
- **Matplotlib**: https://matplotlib.org/stable/api/patches_api.html
- **Python Graph Gallery**: https://python-graph-gallery.com/

These Python libraries provide powerful tools for creating publication-quality scientific diagrams programmatically, enabling reproducible, data-driven visualizations.

