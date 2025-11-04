# Scientific Diagram Types: Catalog and Examples

## Overview

This guide catalogs common scientific diagram types used in research publications, with guidance on when to use each type, design considerations, and example implementations.

## 1. Methodology Flowcharts

### Purpose
Visualize study design, participant flow, data processing pipelines, and experimental workflows.

### When to Use
- Clinical trial participant flow (CONSORT diagrams)
- Systematic review selection process (PRISMA flowcharts)
- Data processing and analysis pipelines
- Experimental procedure workflows
- Algorithm or computational workflows

### Key Elements
- **Start/End nodes**: Rounded rectangles (terminals)
- **Process boxes**: Rectangles for actions/steps
- **Decision diamonds**: For conditional branches
- **Data boxes**: Parallelograms for data inputs/outputs
- **Arrows**: Show sequence and flow direction
- **Annotations**: Numbers (n=X) for participant counts, exclusion criteria

### Design Guidelines
- Flow top-to-bottom or left-to-right consistently
- Align nodes for professional appearance
- Include sample sizes at each step
- Use color sparingly (colorblind-safe palette)
- Keep text concise within nodes
- Add legends for symbols if needed

### Example Use Cases

**CONSORT Participant Flow**
```
Assessed for eligibility (n=500)
    ↓
Excluded (n=150)
- Age < 18: n=80
- Declined: n=50
- Other: n=20
    ↓
Randomized (n=350)
    ↓
  /   \
Treatment  Control
(n=175)   (n=175)
```

**Data Processing Pipeline**
```
Raw Data → Quality Control → Normalization → 
Statistical Analysis → Visualization → Report
```

**Systematic Review Selection**
```
Records identified → Duplicates removed → 
Title/Abstract screening → Full-text review → 
Studies included in meta-analysis
```

## 2. Circuit Diagrams

### Purpose
Illustrate electrical circuits, signal processing systems, and electronic schematics.

### When to Use
- Electronics and electrical engineering papers
- Sensor system designs
- Signal processing workflows
- Measurement apparatus descriptions
- Control system diagrams
- Communication protocol implementations

### Key Elements
- **Voltage/current sources**: Standard symbols
- **Resistors, capacitors, inductors**: Standard component symbols
- **Integrated circuits**: Rectangular blocks with pins
- **Connections**: Solid lines (wires), dots at junctions
- **Ground symbols**: Standard ground notation
- **Labels**: Component values, node voltages

### Design Guidelines
- Follow IEEE/IEC standard symbols
- Wire connections: dots at junctions, no dots for crossovers
- Label all components with values and units
- Use consistent wire thickness
- Indicate signal direction with arrows when helpful
- Group functional blocks with dashed boxes

### Example Use Cases

**Simple RC Circuit**
```
Voltage Source --- Resistor (R1) --- Capacitor (C1) --- Ground
                                  |
                              Output node
```

**Amplifier Circuit**
```
Input → Coupling Capacitor → Transistor → Load Resistor → Output
                              ↑
                          Bias Network
```

**Signal Processing Block Diagram**
```
Sensor → Amplifier → Filter → ADC → Microcontroller → DAC → Actuator
```

## 3. Biological Diagrams

### Purpose
Visualize cellular processes, molecular interactions, signaling pathways, and biological systems.

### When to Use
- Signaling cascade illustrations
- Metabolic pathways
- Gene regulatory networks
- Protein-protein interactions
- Cellular processes and organelle functions
- Experimental procedures (cloning, assays)

### Key Elements
- **Proteins/genes**: Rounded rectangles or ovals
- **Small molecules**: Circles or hexagons
- **Activation arrows**: Standard arrows (→)
- **Inhibition**: Blunt-ended lines (⊣)
- **Transcription**: Bent arrows
- **Translocation**: Dashed arrows across membranes
- **Complex formation**: Connecting lines

### Design Guidelines
- Use standard Systems Biology Graphical Notation (SBGN) when possible
- Italicize gene names, regular font for proteins
- Show subcellular location (cytoplasm, nucleus, membrane)
- Use color to distinguish entity types (proteins, metabolites, genes)
- Include legends for arrow types
- Indicate time progression if relevant

### Example Use Cases

**MAPK Signaling Pathway**
```
Growth Factor → Receptor → RAS → RAF → MEK → ERK → 
Transcription Factor → Gene Expression
```

**Metabolic Pathway**
```
Glucose → Glucose-6-P → Fructose-6-P → Fructose-1,6-BP →
(enzymes labeled at each arrow)
```

**Gene Regulation Network**
```
         ┌─────────┐
         │ Gene A  │
         └────┬────┘
              ↓ activates
         ┌─────────┐
         │ Gene B  │ ⊣ inhibits
         └────┬────┘     ↓
              ↓      ┌─────────┐
         ┌─────────┐│ Gene C  │
         │ Protein │└─────────┘
         └─────────┘
```

**Cell Signaling with Compartments**
```
Membrane: [Receptor] → [G-protein]
              ↓
Cytoplasm: [2nd Messenger] → [Kinase Cascade]
              ↓
Nucleus:   [Transcription Factor] → [Gene]
```

## 4. Block Diagrams / System Architecture

### Purpose
Show system components and their relationships, data flow, or hierarchical organization.

### When to Use
- Software architecture
- Hardware system design
- Data flow diagrams
- Control systems
- Network architecture
- Experimental apparatus setup
- Conceptual frameworks

### Key Elements
- **Components**: Rectangles with labels
- **Subsystems**: Grouped components in larger boxes
- **Connections**: Arrows showing data/signal/control flow
- **Interfaces**: Labeled connection points
- **External entities**: Distinct styling for external components
- **Annotations**: Data types, protocols, frequencies

### Design Guidelines
- Organize hierarchically (high-level to low-level)
- Align blocks in rows or columns
- Use consistent block sizes for similar components
- Label all connections with data types or protocols
- Use colors to distinguish component types
- Include legends for line types (data, control, power)

### Example Use Cases

**Data Acquisition System**
```
┌────────┐    ┌─────┐    ┌──────────────┐    ┌──────────┐
│ Sensor │ → │ ADC │ → │ Microcontrol.│ → │ Database │
└────────┘    └─────┘    └──────────────┘    └──────────┘
                              ↓
                         ┌─────────┐
                         │ Display │
                         └─────────┘
```

**Software Architecture (Three-Tier)**
```
Presentation Layer: [Web UI] [Mobile App]
        ↓
Business Logic Layer: [API Server] [Auth Service]
        ↓
Data Layer: [Database] [Cache] [File Storage]
```

**Experimental Setup**
```
[Light Source] → [Sample Chamber] → [Detector] → [Amplifier] → 
[Data Acquisition] → [Computer]
      ↑                                              ↓
[Temperature Controller] ←───────────────── [Control Software]
```

## 5. Process Flow Diagrams

### Purpose
Illustrate sequential processes, decision logic, and workflows.

### When to Use
- Manufacturing processes
- Quality control procedures
- Algorithm logic flow
- Decision trees
- Standard operating procedures (SOPs)
- Troubleshooting guides

### Key Elements
- **Start/End**: Ovals or rounded rectangles
- **Process**: Rectangles
- **Decision**: Diamonds with yes/no branches
- **Input/Output**: Parallelograms
- **Subprocess**: Rectangle with double borders
- **Arrows**: Show flow direction
- **Connectors**: Circles for off-page or looping connections

### Design Guidelines
- Single entry and exit points
- Clear decision branch labels (Yes/No, True/False)
- Avoid crossing lines when possible
- Use connectors for complex flows
- Number steps if sequence is critical
- Keep decision questions simple and binary

### Example Use Cases

**Quality Control Decision Tree**
```
Start → Measure Parameter → [Within Spec?] 
                              Yes ↓    No ↓
                           Accept   Adjust Settings → Retest
                              ↓         ↓
                             End ← [Pass?] → Reject
```

**Algorithm Flowchart**
```
Initialize Variables → Read Input → [Data Valid?]
                                      No ↓      Yes ↓
                                Error Message  Process Data
                                      ↓             ↓
                                   End ←──── Output Results
```

## 6. Network Diagrams

### Purpose
Visualize relationships, connections, and network topology.

### When to Use
- Computer networks
- Social networks
- Protein interaction networks
- Collaboration networks
- Communication pathways
- Graph-based data structures

### Key Elements
- **Nodes**: Circles, rectangles, or custom shapes
- **Edges**: Lines connecting nodes
- **Directed edges**: Arrows showing direction
- **Weighted edges**: Line thickness or labels showing weights
- **Node attributes**: Color, size, or labels
- **Clusters**: Grouped nodes with boundaries

### Design Guidelines
- Use layout algorithms for complex networks (force-directed, hierarchical)
- Size nodes by importance/degree if relevant
- Color-code node types or communities
- Show edge weights if important
- Minimize edge crossings
- Include network statistics if relevant (N nodes, M edges)

### Example Use Cases

**Communication Network**
```
    [Server]
    /  |  \
  /    |    \
[PC1] [PC2] [PC3]
  \    |    /
   \   |   /
    [Router] ← [Internet]
```

**Protein Interaction Network**
```
Nodes = proteins (colored by function)
Edges = experimentally verified interactions
Node size = expression level
```

**Collaboration Network**
```
Nodes = researchers
Edges = co-authorship
Node color = institution
Edge thickness = number of collaborations
```

## 7. Timeline Diagrams

### Purpose
Show events, phases, or changes over time.

### When to Use
- Study design timelines
- Treatment schedules
- Historical progressions
- Project milestones
- Developmental stages
- Longitudinal study visits

### Key Elements
- **Time axis**: Horizontal or vertical line
- **Events**: Markers, dots, or boxes at time points
- **Durations**: Bars or shaded regions
- **Labels**: Time points and event descriptions
- **Phases**: Color-coded segments
- **Annotations**: Additional information for events

### Design Guidelines
- Use consistent time scale
- Clearly label all time points
- Use color to distinguish phases or types
- Include scale bar or time units
- Align events vertically for clarity
- Show overlapping events with vertical offset

### Example Use Cases

**Clinical Trial Timeline**
```
Week:     0    4    8   12   16   20   24
          |----|----|----|----|----|----|
Events:   ●    ●    ●    ●    ●         ●
       Baseline Randomize   Follow-ups  End
          |=========|=========|
        Screening Treatment  Follow-up
```

**Experimental Protocol**
```
Day 0: Baseline measurements
  ↓
Days 1-7: Treatment A
  ↓
Day 8: Washout period
  ↓
Days 9-15: Treatment B
  ↓
Day 16: Final measurements
```

**Project Gantt Chart Style**
```
Task 1  |████████|
Task 2     |██████████|
Task 3           |████████|
        0  2  4  6  8  10 (months)
```

## 8. Hierarchical / Tree Diagrams

### Purpose
Show hierarchical relationships, classifications, or organizational structure.

### When to Use
- Organizational charts
- Taxonomic classifications
- Decision trees
- File system structures
- Phylogenetic trees
- Category hierarchies

### Key Elements
- **Root node**: Top-level element
- **Parent nodes**: Intermediate levels
- **Child nodes**: Terminal elements
- **Branches**: Connections showing relationships
- **Levels**: Horizontal tiers of hierarchy
- **Labels**: Node names and attributes

### Design Guidelines
- Organize top-to-bottom or left-to-right
- Align nodes at same hierarchical level
- Use consistent spacing between levels
- Size nodes by importance if relevant
- Keep branch angles consistent
- Label branch points if needed (e.g., evolutionary distances)

### Example Use Cases

**Organizational Structure**
```
         [Director]
            /  \
           /    \
    [Manager A] [Manager B]
      /    \       /    \
   [Staff] [Staff] [Staff] [Staff]
```

**Taxonomic Classification**
```
Kingdom
  ↓
Phylum → [Multiple branches]
  ↓
Class
  ↓
Order
  ↓
Family → [Species groups]
```

**Decision Tree (Classification)**
```
[Feature 1 > threshold?]
  Yes /        \ No
[Class A]   [Feature 2 > threshold?]
            Yes /          \ No
         [Class B]      [Class C]
```

## 9. Venn Diagrams / Set Relationships

### Purpose
Show overlaps, intersections, and relationships between sets.

### When to Use
- Shared features or categories
- Overlap analysis (gene lists, patient cohorts)
- Logical relationships
- Comparison of groups
- Inclusion/exclusion criteria

### Key Elements
- **Circles/ovals**: Representing sets
- **Overlaps**: Intersecting regions
- **Labels**: Set names and sizes
- **Numbers**: Element counts in each region
- **Color**: Distinguish sets (use transparency for overlaps)

### Design Guidelines
- Use 2-3 circles maximum for clarity
- Label all regions with counts
- Use colorblind-safe palette with transparency
- Ensure circles overlap proportionally if area matters
- Include total counts for each set
- Consider alternatives for >3 sets (UpSet plots)

### Example Use Cases

**Gene Expression Overlap**
```
    [Treatment A]  [Treatment B]
         200          150
           \    80   /
            \───────/
         Differentially expressed genes
```

**Patient Eligibility**
```
[Age 18-65]  ∩  [No contraindications]  ∩  [Willing to participate]
     = Eligible participants
```

## 10. Heatmaps / Matrix Diagrams

### Purpose
Visualize matrix data, correlations, or relationships between two categorical variables.

### When to Use
- Correlation matrices
- Gene expression across samples
- Confusion matrices (classification)
- Pairwise comparisons
- Presence/absence data
- Intensity measurements across conditions

### Key Elements
- **Grid cells**: Representing matrix values
- **Color scale**: Mapping values to colors
- **Row/column labels**: Categories or variables
- **Color bar**: Legend for color scale
- **Annotations**: Values within cells if readable

### Design Guidelines
- Use perceptually uniform colormap (viridis, plasma)
- Include color bar with scale
- Order rows/columns meaningfully (hierarchical clustering)
- Annotate cells if space permits
- Use diverging colormap for centered data (correlations)
- Keep cell aspect ratio square

### Example Use Cases

**Correlation Matrix**
```
       Var1  Var2  Var3
Var1 [ 1.0   0.7   0.3 ]
Var2 [ 0.7   1.0   0.5 ]
Var3 [ 0.3   0.5   1.0 ]

Color scale: -1 (blue) to +1 (red)
```

**Gene Expression Heatmap**
```
Rows = genes
Columns = samples/conditions
Color = expression level (low to high)
Hierarchical clustering on both axes
```

## Diagram Selection Guide

| **Goal** | **Diagram Type** | **Best For** |
|----------|-----------------|--------------|
| Show sequence | Flowchart, Timeline | Processes, events over time |
| Show components | Block diagram | System architecture |
| Show relationships | Network, Tree | Connections, hierarchies |
| Show overlap | Venn diagram | Set intersections |
| Show pathway | Biological diagram | Signaling, metabolism |
| Show circuit | Circuit diagram | Electronics, signals |
| Show data matrix | Heatmap | Correlations, patterns |
| Show decisions | Decision tree, Flowchart | Logic, classification |
| Show organization | Tree, Org chart | Hierarchies, structure |

## Combining Diagram Types

Often, complex figures combine multiple diagram types:

**Example: Experimental Design + Timeline**
```
[Flowchart showing participant groups]
    +
[Timeline showing intervention schedule]
    +
[Measurement points indicated]
```

**Example: System Architecture + Data Flow**
```
[Block diagram of components]
    +
[Arrows showing data flow with annotations]
    +
[Network diagram of connections]
```

## Common Mistakes to Avoid

1. **Too much information**: Simplify, create multiple figures if needed
2. **Inconsistent styling**: Use templates and style files
3. **Poor alignment**: Use grids and alignment tools
4. **Unclear flow**: Ensure arrows and sequence are obvious
5. **Missing labels**: Label all components, axes, and connections
6. **Color overuse**: Stick to colorblind-safe palette, use sparingly
7. **Tiny text**: Ensure readability at final print size
8. **Crossing lines**: Minimize or use bridges/gaps to indicate
9. **No legend**: Include legends for symbols, colors, line types
10. **Inconsistent scale**: Maintain proportions and spacing

## Accessibility Checklist

- [ ] Colorblind-safe palette (Okabe-Ito)
- [ ] Works in grayscale
- [ ] Text minimum 7-8 pt at final size
- [ ] High contrast between elements
- [ ] Redundant encoding (not just color)
- [ ] Clear, descriptive labels
- [ ] Comprehensive figure caption
- [ ] Logical reading order

## Further Reading

- **CONSORT Flow Diagram**: http://www.consort-statement.org/consort-statement/flow-diagram
- **PRISMA Flow Diagram**: http://prisma-statement.org/
- **Systems Biology Graphical Notation (SBGN)**: https://sbgn.github.io/
- **IEEE Standard Graphic Symbols for Electrical and Electronics Diagrams**: IEEE Std 315
- **Graph Visualization**: Graphviz documentation

Use this catalog to select the appropriate diagram type for your scientific communication needs, then refer to the TikZ guide and templates for implementation.

