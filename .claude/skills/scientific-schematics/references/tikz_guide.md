# TikZ Guide for Scientific Diagrams

## Overview

TikZ (TikZ ist kein Zeichenprogramm - "TikZ is not a drawing program") is a powerful LaTeX package for creating high-quality vector graphics. This guide focuses on using TikZ for scientific diagrams, flowcharts, and schematics in research publications.

## Basic TikZ Structure

### Minimal Example

```latex
\documentclass{article}
\usepackage{tikz}

\begin{document}

\begin{tikzpicture}
  % Your drawing commands here
  \draw (0,0) -- (2,0);  % Line from (0,0) to (2,0)
  \node at (1,0.5) {Label};  % Text at position
\end{tikzpicture}

\end{document}
```

### Required Packages and Libraries

```latex
\usepackage{tikz}
\usetikzlibrary{
  shapes.geometric,  % Rectangles, circles, diamonds, etc.
  shapes.arrows,     % Arrow shapes
  arrows.meta,       % Modern arrow tips
  positioning,       % Relative positioning (above, below, right of)
  calc,             % Coordinate calculations
  fit,              % Fitting boxes around multiple nodes
  backgrounds,      % Background layers
  decorations.pathreplacing  % Braces and decorations
}
```

## Coordinate Systems

### Cartesian Coordinates

```latex
\draw (0,0) -- (3,2);     % From origin to (3,2)
\draw (1,1) circle (0.5); % Circle at (1,1) with radius 0.5
```

### Relative Coordinates

```latex
\draw (0,0) -- ++(2,0)    % Move 2 right from (0,0), update position
           -- ++(0,2)     % Move 2 up from current position
           -- ++(-2,0);   % Move 2 left from current position

\draw (0,0) -- +(1,1);    % Move to (1,1) but don't update position
```

### Polar Coordinates

```latex
\draw (0,0) -- (30:2);    % Angle 30°, distance 2
\draw (0,0) -- (90:1.5);  % Angle 90°, distance 1.5
```

### Named Coordinates

```latex
\coordinate (A) at (0,0);
\coordinate (B) at (3,2);
\draw (A) -- (B);
```

## Drawing Basic Shapes

### Lines and Paths

```latex
% Straight line
\draw (0,0) -- (2,0);

% Multiple connected segments
\draw (0,0) -- (1,1) -- (2,0) -- (0,0);

% Closed path
\draw (0,0) -- (1,1) -- (2,0) -- cycle;

% Curved path (Bezier)
\draw (0,0) .. controls (1,1) and (2,1) .. (3,0);

% Smooth curve through points
\draw plot[smooth] coordinates {(0,0) (1,2) (2,1) (3,3)};
```

### Rectangles and Circles

```latex
% Rectangle: (lower-left) rectangle (upper-right)
\draw (0,0) rectangle (2,1);

% Circle: (center) circle (radius)
\draw (1,1) circle (0.5);

% Ellipse: (center) ellipse (x-radius and y-radius)
\draw (1,1) ellipse (1 and 0.5);

% Rounded rectangle
\draw[rounded corners=5pt] (0,0) rectangle (2,1);
```

### Arcs and Curves

```latex
% Arc: (start) arc (start-angle:end-angle:radius)
\draw (0,0) arc (0:90:1);       % Quarter circle
\draw (0,0) arc (0:180:1.5);    % Semicircle

% Partial ellipse arc
\draw (0,0) arc (0:270:1.5 and 1);
```

## Nodes - The Foundation of Diagrams

### Basic Nodes

```latex
% Simple node
\node at (0,0) {Text};

% Node with name for referencing
\node (A) at (0,0) {Node A};
\node (B) at (2,0) {Node B};
\draw (A) -- (B);  % Connect nodes

% Node on a path
\draw (0,0) -- node {middle} (2,0);
```

### Node Shapes

```latex
% Rectangle (default)
\node[draw, rectangle] at (0,0) {Rectangle};

% Circle
\node[draw, circle] at (2,0) {Circle};

% Ellipse
\node[draw, ellipse] at (4,0) {Ellipse};

% Diamond (requires shapes.geometric library)
\node[draw, diamond] at (6,0) {Diamond};

% Rounded rectangle
\node[draw, rounded corners] at (8,0) {Rounded};
```

### Node Styling

```latex
% Size
\node[minimum width=3cm, minimum height=1cm] {Wide node};

% Colors
\node[fill=blue!20, draw=blue!80] {Colored};

% Line style
\node[draw, thick, dashed] {Dashed border};
\node[draw, ultra thick] {Thick border};

% Text styling
\node[font=\large\bfseries] {Bold Large Text};
```

### Node Anchors

Nodes have anchor points for precise connections:

```latex
\node[draw] (A) at (0,0) {Node};

% Anchor points: north, south, east, west, 
%                north east, north west, south east, south west
%                center

\draw[red] (A.north) -- ++(0,0.5);    % From top of node
\draw[blue] (A.east) -- ++(0.5,0);    % From right side
\draw[green] (A.south) -- ++(0,-0.5); % From bottom
```

## Positioning

### Absolute Positioning

```latex
\node[draw] at (0,0) {A};
\node[draw] at (3,2) {B};
```

### Relative Positioning (positioning library)

```latex
\node[draw] (A) {Node A};
\node[draw, right=of A] (B) {Node B};
\node[draw, below=of A] (C) {Node C};
\node[draw, above right=of A] (D) {Node D};

% With custom distance
\node[draw] (A) {A};
\node[draw, right=2cm of A] (B) {B};
\node[draw, below=1.5cm of A] (C) {C};
```

### Positioning Patterns

```latex
% Chained positioning
\node[draw] (A) {A};
\node[draw, right=of A] (B) {B};
\node[draw, right=of B] (C) {C};
\node[draw, right=of C] (D) {D};

% Grid layout
\node[draw] (A) at (0,2) {A};
\node[draw] (B) at (2,2) {B};
\node[draw] (C) at (0,0) {C};
\node[draw] (D) at (2,0) {D};

% Circular arrangement
\foreach \i in {0,1,...,7} {
  \node[draw, circle] at ({360/8 * \i}:2) {\i};
}
```

## Arrows and Connections

### Arrow Styles (arrows.meta library)

```latex
% Modern arrow tips
\draw[-Stealth] (0,0) -- (2,0);        % Stealth arrow tip
\draw[-Latex] (0,0.5) -- (2,0.5);      % LaTeX arrow tip
\draw[-Triangle] (0,1) -- (2,1);       % Triangle tip

% Both ends
\draw[Stealth-Stealth] (0,1.5) -- (2,1.5);

% Larger arrows
\draw[-{Stealth[length=5mm, width=3mm]}] (0,2) -- (2,2);

% Multiple arrows
\draw[-{Stealth}{Stealth}] (0,2.5) -- (2,2.5);
```

### Connection Paths

```latex
\node[draw] (A) {A};
\node[draw, right=3cm of A] (B) {B};

% Straight arrow
\draw[-Stealth] (A) -- (B);

% Horizontal then vertical
\draw[-Stealth] (A) -| (B);

% Vertical then horizontal
\draw[-Stealth] (A) |- (B);

% Curved (Bezier)
\draw[-Stealth] (A) to[bend left=30] (B);
\draw[-Stealth] (A) to[bend right=30] (B);

% Out and in angles
\draw[-Stealth] (A) to[out=45, in=135] (B);
```

### Edge Labels

```latex
\node[draw] (A) {A};
\node[draw, right=3cm of A] (B) {B};

% Label above
\draw[-Stealth] (A) -- node[above] {label} (B);

% Label below
\draw[-Stealth] (A) -- node[below] {label} (B);

% Label at specific position (0=start, 0.5=middle, 1=end)
\draw[-Stealth] (A) -- node[pos=0.25, above] {quarter} (B);

% Sloped text
\draw[-Stealth] (A) -- node[above, sloped] {sloped} (B);
```

## Styles and Customization

### Defining Custom Styles

```latex
\begin{tikzpicture}[
  % Define styles within tikzpicture options
  process/.style={rectangle, draw, fill=blue!20, 
                  minimum width=3cm, minimum height=1cm},
  decision/.style={diamond, draw, fill=orange!20, aspect=2},
  arrow/.style={-Stealth, thick}
]

\node[process] (p1) {Process};
\node[decision, below=of p1] (d1) {Decision?};
\draw[arrow] (p1) -- (d1);

\end{tikzpicture}
```

### Global Style Definitions

```latex
% In preamble or separate file
\tikzset{
  process/.style={
    rectangle, 
    rounded corners,
    draw=black, 
    thick,
    fill=blue!20,
    minimum width=3cm,
    minimum height=1cm,
    text width=2.5cm,
    align=center
  },
  decision/.style={
    diamond,
    draw=black,
    thick,
    fill=orange!20,
    minimum width=2cm,
    aspect=2,
    align=center
  },
  data/.style={
    trapezium,
    trapezium left angle=70,
    trapezium right angle=110,
    draw=black,
    thick,
    fill=green!20,
    minimum width=2cm,
    minimum height=1cm
  }
}
```

### Color Definitions (Okabe-Ito Colorblind-Safe Palette)

```latex
\definecolor{okabe-orange}{RGB}{230, 159, 0}
\definecolor{okabe-blue}{RGB}{86, 180, 233}
\definecolor{okabe-green}{RGB}{0, 158, 115}
\definecolor{okabe-yellow}{RGB}{240, 228, 66}
\definecolor{okabe-dblue}{RGB}{0, 114, 178}
\definecolor{okabe-vermillion}{RGB}{213, 94, 0}
\definecolor{okabe-purple}{RGB}{204, 121, 167}
\definecolor{okabe-black}{RGB}{0, 0, 0}

% Use in styles
\node[fill=okabe-blue!30, draw=okabe-dblue] {Text};
```

## Advanced Techniques

### Loops and Repetition

```latex
% Simple loop
\foreach \x in {0,1,2,3,4} {
  \node[draw] at (\x,0) {\x};
}

% Loop with calculations
\foreach \x in {0,1,...,5} {
  \draw (\x,0) circle (0.2);
}

% Multiple variables
\foreach \x/\y/\label in {0/0/A, 1/1/B, 2/0/C} {
  \node[draw] at (\x,\y) {\label};
}

% Nested loops
\foreach \x in {0,1,2} {
  \foreach \y in {0,1,2} {
    \node[draw] at (\x,\y) {\x,\y};
  }
}
```

### Calculations (calc library)

```latex
% Midpoint
\coordinate (A) at (0,0);
\coordinate (B) at (4,3);
\coordinate (M) at ($(A)!0.5!(B)$);  % Midpoint between A and B
\node[draw] at (M) {Middle};

% Point along path
\coordinate (C) at ($(A)!0.25!(B)$);  % 25% from A to B

% Perpendicular point
\coordinate (P) at ($(A)!0.5!(B)$);
\coordinate (Q) at ($(P)!1cm!90:(B)$);  % 1cm perpendicular to AB
```

### Backgrounds and Layers

```latex
\begin{tikzpicture}
  % Main content
  \node[draw] (A) {Node A};
  \node[draw, right=of A] (B) {Node B};
  
  % Background layer
  \begin{scope}[on background layer]
    \node[fill=gray!20, rounded corners, fit=(A) (B),
          inner sep=10pt] {};
  \end{scope}
\end{tikzpicture}
```

### Scope for Local Styling

```latex
\begin{tikzpicture}
  % Normal drawing
  \draw (0,0) -- (1,0);
  
  % Apply style only within scope
  \begin{scope}[thick, blue]
    \draw (0,0.5) -- (1,0.5);
    \draw (0,1) -- (1,1);
  \end{scope}
  
  % Back to normal
  \draw (0,1.5) -- (1,1.5);
\end{tikzpicture}
```

## Common Scientific Diagram Patterns

### Flowchart Pattern

```latex
\begin{tikzpicture}[
  node distance=1.5cm and 2cm,
  process/.style={rectangle, rounded corners, draw, thick, 
                  fill=blue!20, minimum width=3cm, minimum height=1cm},
  decision/.style={diamond, draw, thick, fill=orange!20, aspect=2},
  arrow/.style={-Stealth, thick}
]

\node[process] (start) {Start};
\node[process, below=of start] (step1) {Process Step};
\node[decision, below=of step1] (decision) {Decision?};
\node[process, below left=of decision] (yes) {Yes Path};
\node[process, below right=of decision] (no) {No Path};
\node[process, below=3cm of decision] (end) {End};

\draw[arrow] (start) -- (step1);
\draw[arrow] (step1) -- (decision);
\draw[arrow] (decision) -| node[near start, above] {yes} (yes);
\draw[arrow] (decision) -| node[near start, above] {no} (no);
\draw[arrow] (yes) |- (end);
\draw[arrow] (no) |- (end);

\end{tikzpicture}
```

### Block Diagram Pattern

```latex
\begin{tikzpicture}[
  block/.style={rectangle, draw, thick, fill=blue!20, 
                minimum width=2.5cm, minimum height=1cm},
  arrow/.style={-Stealth, thick}
]

\node[block] (input) {Input};
\node[block, right=2cm of input] (process) {Process};
\node[block, right=2cm of process] (output) {Output};

\draw[arrow] (input) -- node[above] {data} (process);
\draw[arrow] (process) -- node[above] {result} (output);

% Feedback loop
\draw[arrow] (output.north) |- ++(0,1) -| 
             node[near end, above] {feedback} (process.north);

\end{tikzpicture}
```

### Network Diagram Pattern

```latex
\begin{tikzpicture}[
  node/.style={circle, draw, thick, fill=blue!20, minimum size=1cm},
  edge/.style={-Stealth, thick}
]

% Nodes
\node[node] (1) at (0,0) {1};
\node[node] (2) at (2,1.5) {2};
\node[node] (3) at (2,-1.5) {3};
\node[node] (4) at (4,0) {4};

% Edges
\draw[edge] (1) -- (2);
\draw[edge] (1) -- (3);
\draw[edge] (2) -- (4);
\draw[edge] (3) -- (4);
\draw[edge, bend left] (2) to (3);

\end{tikzpicture}
```

### Timeline Pattern

```latex
\begin{tikzpicture}
  % Timeline axis
  \draw[thick, -Stealth] (0,0) -- (10,0) node[right] {Time};
  
  % Events
  \foreach \x/\label in {1/Baseline, 3/Week 4, 5/Week 8, 7/Week 12, 9/Final} {
    \draw[thick] (\x,0.1) -- (\x,-0.1);
    \node[below] at (\x,-0.1) {\label};
    \node[circle, fill=blue!20, draw, inner sep=2pt] at (\x,0) {};
  }
  
  % Interventions as bars
  \draw[thick, blue] (1,0.5) -- (5,0.5) node[midway, above] {Treatment A};
  \draw[thick, red] (5,0.8) -- (9,0.8) node[midway, above] {Treatment B};
  
\end{tikzpicture}
```

## CircuitikZ for Circuit Diagrams

CircuitikZ extends TikZ specifically for electrical circuits:

```latex
\usepackage{circuitikz}

\begin{circuitikz}[american]
  % Voltage source
  \draw (0,0) to[V, v=$V_s$] (0,2)
  
  % Resistors
        to[R, l=$R_1$] (2,2)
        to[R, l=$R_2$] (4,2)
  
  % Capacitor
        to[C, l=$C_1$] (4,0)
  
  % Close circuit
        to[short] (0,0);
  
  % Ground
  \draw (0,0) node[ground] {};
  
\end{circuitikz}
```

## Best Practices for Scientific Diagrams

### 1. Consistent Node Spacing

```latex
% Define node distance globally
\begin{tikzpicture}[node distance=2cm and 3cm]
  % All nodes will be spaced consistently
\end{tikzpicture}
```

### 2. Use Styles for Consistency

```latex
% Define styles once, use everywhere
\tikzset{
  myprocess/.style={/* styling */},
  mydecision/.style={/* styling */}
}
```

### 3. Named Nodes for Flexibility

```latex
% Always name nodes you'll reference
\node (A) {Node A};  % Good
\node at (0,0) {Node};  % Hard to reference later
```

### 4. Anchor Points for Precise Connections

```latex
% Use anchors for clean connections
\draw (A.east) -- (B.west);  % Good
\draw (A) -- (B);  % May not connect cleanly
```

### 5. Layer Complex Diagrams

```latex
% Draw in logical order: background -> main -> annotations
\begin{scope}[on background layer]
  % Background elements
\end{scope}
% Main diagram
% Annotations on top
```

### 6. Modularity with \input

```latex
% Main document
\begin{figure}
  \centering
  \input{figures/my_diagram.tikz}
  \caption{My diagram}
\end{figure}

% my_diagram.tikz contains just the tikzpicture
\begin{tikzpicture}
  % diagram code
\end{tikzpicture}
```

## Compilation and Optimization

### Standalone Compilation

Create standalone TikZ documents for faster iteration:

```latex
\documentclass[tikz, border=2mm]{standalone}
\usepackage{tikz}
\usetikzlibrary{shapes, arrows.meta, positioning}

\begin{document}
\begin{tikzpicture}
  % Your diagram
\end{tikzpicture}
\end{document}
```

Compile to PDF:
```bash
pdflatex diagram.tex
```

### External Graphics (for large documents)

For complex diagrams, compile separately and include:

```latex
% Enable externalization
\usetikzlibrary{external}
\tikzexternalize

% In document
\begin{tikzpicture}
  % Complex diagram - compiled once, cached
\end{tikzpicture}
```

## Troubleshooting Common Issues

**Issue**: Nodes overlapping text
- **Solution**: Increase `minimum width` or `minimum height`, or use `text width` with `align=center`

**Issue**: Arrows not pointing to node edges
- **Solution**: Use anchor points: `\draw (A.east) -- (B.west);`

**Issue**: Inconsistent spacing
- **Solution**: Set `node distance` globally in tikzpicture options

**Issue**: Curved arrows going wrong direction
- **Solution**: Adjust `bend left/right` angle or use `out` and `in` angles

**Issue**: Text overflowing nodes
- **Solution**: Add `text width=Xcm, align=center` to node style

**Issue**: Compilation slow
- **Solution**: Use `\tikzexternalize` or compile diagrams separately

## Quick Reference: Common Commands

```latex
% Shapes
\node[draw, rectangle] {Text};
\node[draw, circle] {Text};
\node[draw, diamond] {Text};
\node[draw, ellipse] {Text};

% Positioning
\node[right=of A] (B) {B};
\node[below=2cm of A] (C) {C};
\node[above right=of A] (D) {D};

% Arrows
\draw[-Stealth] (A) -- (B);
\draw[-Stealth] (A) to[bend left] (B);
\draw[-Stealth] (A) -| (B);

% Styling
\node[fill=blue!20, draw=blue!80, thick] {Styled};
\draw[thick, dashed, red] (A) -- (B);

% Loops
\foreach \x in {0,1,2,3} { \node at (\x,0) {\x}; }
```

## Further Resources

- **TikZ & PGF Manual**: https://pgf-tikz.github.io/pgf/pgfmanual.pdf
- **TeXample.net**: http://www.texample.net/tikz/
- **CircuitikZ Manual**: https://ctan.org/pkg/circuitikz
- **TikZ Tutorial**: https://cremeronline.com/LaTeX/minimaltikz.pdf

This guide provides the foundation for creating scientific diagrams with TikZ. Combine these techniques with the templates in the `assets/` directory for publication-ready figures.

