#!/usr/bin/env python3
"""
Generate biological pathway diagrams using Matplotlib.

This script creates publication-quality biological pathway diagrams showing
protein interactions, signaling cascades, and molecular processes.

Requirements:
    pip install matplotlib numpy

Usage:
    from pathway_diagram import PathwayGenerator
    
    gen = PathwayGenerator()
    gen.add_node('Receptor', type='protein', position=(1, 5))
    gen.add_node('Kinase', type='protein', position=(3, 5))
    gen.add_edge('Receptor', 'Kinase', interaction='activation')
    gen.save('pathway.pdf')
"""

import argparse
from typing import Dict, List, Tuple, Optional

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
    import numpy as np
except ImportError:
    print("Error: matplotlib not installed. Install with: pip install matplotlib")
    exit(1)


# Okabe-Ito colorblind-safe palette
COLORS = {
    'protein': '#56B4E9',      # Sky blue
    'gene': '#009E73',         # Green
    'metabolite': '#F0E442',   # Yellow
    'complex': '#E69F00',      # Orange
    'enzyme': '#0072B2',       # Blue
    'receptor': '#D55E00',     # Vermillion
    'tf': '#CC79A7',           # Purple (transcription factor)
    'default': '#BBBBBB'       # Gray
}

INTERACTION_STYLES = {
    'activation': {'arrowstyle': '->', 'color': 'black', 'linewidth': 2.5},
    'inhibition': {'arrowstyle': '-|', 'color': '#D55E00', 'linewidth': 2.5},
    'catalysis': {'arrowstyle': '->', 'color': '#0072B2', 'linewidth': 2.0, 'linestyle': 'dashed'},
    'binding': {'arrowstyle': '-', 'color': 'black', 'linewidth': 2.0},
    'transcription': {'arrowstyle': '->', 'color': '#009E73', 'linewidth': 2.5},
}


class PathwayNode:
    """Represents a node in the pathway (protein, gene, metabolite, etc.)."""
    
    def __init__(self, name: str, node_type: str = 'protein', 
                 position: Tuple[float, float] = (0, 0)):
        self.name = name
        self.node_type = node_type
        self.position = position
        
    def get_color(self) -> str:
        """Get color for this node type."""
        return COLORS.get(self.node_type, COLORS['default'])


class PathwayEdge:
    """Represents an interaction between nodes."""
    
    def __init__(self, source: str, target: str, 
                 interaction: str = 'activation'):
        self.source = source
        self.target = target
        self.interaction = interaction
    
    def get_style(self) -> Dict:
        """Get style for this interaction type."""
        return INTERACTION_STYLES.get(self.interaction, 
                                      INTERACTION_STYLES['activation'])


class PathwayGenerator:
    """Generate biological pathway diagrams."""
    
    def __init__(self, figsize: Tuple[float, float] = (10, 8)):
        """
        Initialize pathway generator.
        
        Args:
            figsize: Figure size in inches
        """
        self.figsize = figsize
        self.nodes: Dict[str, PathwayNode] = {}
        self.edges: List[PathwayEdge] = []
        
        # Styling
        self.node_width = 0.8
        self.node_height = 0.5
        self.font_family = 'Arial'
        self.font_size = 10
        
    def add_node(self, name: str, node_type: str = 'protein',
                position: Tuple[float, float] = (0, 0)) -> 'PathwayGenerator':
        """
        Add a node to the pathway.
        
        Args:
            name: Node name/label
            node_type: Type of node (protein, gene, metabolite, enzyme, etc.)
            position: (x, y) position
            
        Returns:
            self for chaining
        """
        self.nodes[name] = PathwayNode(name, node_type, position)
        return self
    
    def add_edge(self, source: str, target: str, 
                interaction: str = 'activation') -> 'PathwayGenerator':
        """
        Add an interaction between nodes.
        
        Args:
            source: Source node name
            target: Target node name
            interaction: Type of interaction (activation, inhibition, etc.)
            
        Returns:
            self for chaining
        """
        if source not in self.nodes:
            raise ValueError(f"Source node '{source}' not found")
        if target not in self.nodes:
            raise ValueError(f"Target node '{target}' not found")
            
        self.edges.append(PathwayEdge(source, target, interaction))
        return self
    
    def add_protein(self, name: str, position: Tuple[float, float]) -> 'PathwayGenerator':
        """Convenience method to add a protein node."""
        return self.add_node(name, 'protein', position)
    
    def add_gene(self, name: str, position: Tuple[float, float]) -> 'PathwayGenerator':
        """Convenience method to add a gene node."""
        return self.add_node(name, 'gene', position)
    
    def add_activation(self, source: str, target: str) -> 'PathwayGenerator':
        """Convenience method to add an activation interaction."""
        return self.add_edge(source, target, 'activation')
    
    def add_inhibition(self, source: str, target: str) -> 'PathwayGenerator':
        """Convenience method to add an inhibition interaction."""
        return self.add_edge(source, target, 'inhibition')
    
    def generate(self) -> Tuple[plt.Figure, plt.Axes]:
        """
        Generate the pathway diagram.
        
        Returns:
            (figure, axes) tuple
        """
        # Set publication quality defaults
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = [self.font_family]
        plt.rcParams['font.size'] = self.font_size
        plt.rcParams['pdf.fonttype'] = 42  # TrueType fonts
        
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Draw edges first (so they appear behind nodes)
        self._draw_edges(ax)
        
        # Draw nodes
        self._draw_nodes(ax)
        
        # Configure axes
        self._configure_axes(ax)
        
        return fig, ax
    
    def _draw_nodes(self, ax: plt.Axes):
        """Draw all nodes."""
        for node in self.nodes.values():
            x, y = node.position
            color = node.get_color()
            
            # Choose shape based on node type
            if node.node_type == 'gene':
                # Genes as rectangles
                box = mpatches.Rectangle(
                    (x - self.node_width/2, y - self.node_height/2),
                    self.node_width, self.node_height,
                    facecolor=color, edgecolor='black', linewidth=2
                )
            elif node.node_type == 'metabolite':
                # Metabolites as circles
                box = Circle((x, y), self.node_height/2,
                           facecolor=color, edgecolor='black', linewidth=2)
            else:
                # Proteins and others as rounded rectangles
                box = FancyBboxPatch(
                    (x - self.node_width/2, y - self.node_height/2),
                    self.node_width, self.node_height,
                    boxstyle="round,pad=0.05",
                    facecolor=color, edgecolor='black', linewidth=2
                )
            
            ax.add_patch(box)
            
            # Add label
            ax.text(x, y, node.name, ha='center', va='center',
                   fontsize=self.font_size, fontweight='bold',
                   fontfamily=self.font_family)
    
    def _draw_edges(self, ax: plt.Axes):
        """Draw all edges (interactions)."""
        for edge in self.edges:
            source_node = self.nodes[edge.source]
            target_node = self.nodes[edge.target]
            
            x1, y1 = source_node.position
            x2, y2 = target_node.position
            
            # Calculate arrow start and end points (at node boundaries)
            start, end = self._calculate_arrow_points(
                (x1, y1), (x2, y2), self.node_width, self.node_height
            )
            
            # Get interaction style
            style = edge.get_style()
            
            # Create arrow
            arrow = FancyArrowPatch(
                start, end,
                arrowstyle=style['arrowstyle'],
                color=style['color'],
                linewidth=style.get('linewidth', 2.0),
                linestyle=style.get('linestyle', 'solid'),
                mutation_scale=20,
                zorder=1  # Behind nodes
            )
            
            ax.add_patch(arrow)
    
    def _calculate_arrow_points(self, start: Tuple[float, float], 
                                end: Tuple[float, float],
                                box_width: float, box_height: float
                               ) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        """Calculate arrow start and end points at box boundaries."""
        x1, y1 = start
        x2, y2 = end
        
        # Direction vector
        dx = x2 - x1
        dy = y2 - y1
        length = np.sqrt(dx**2 + dy**2)
        
        if length == 0:
            return start, end
        
        # Normalize
        dx /= length
        dy /= length
        
        # Offset from box centers
        offset = box_width / 2
        
        # Calculate start and end points
        start_point = (x1 + dx * offset, y1 + dy * offset)
        end_point = (x2 - dx * offset, y2 - dy * offset)
        
        return start_point, end_point
    
    def _configure_axes(self, ax: plt.Axes):
        """Configure axes appearance."""
        # Calculate bounds
        if self.nodes:
            xs = [node.position[0] for node in self.nodes.values()]
            ys = [node.position[1] for node in self.nodes.values()]
            
            margin = 1.0
            ax.set_xlim(min(xs) - margin, max(xs) + margin)
            ax.set_ylim(min(ys) - margin, max(ys) + margin)
        
        ax.set_aspect('equal')
        ax.axis('off')
    
    def save(self, filename: str, dpi: int = 300):
        """
        Save pathway diagram.
        
        Args:
            filename: Output filename (.pdf, .svg, .png)
            dpi: Resolution for raster outputs
        """
        fig, ax = self.generate()
        
        plt.tight_layout()
        fig.savefig(filename, dpi=dpi, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        plt.close(fig)
        
        print(f"Pathway diagram saved to {filename}")
    
    def show(self):
        """Display pathway diagram (for interactive use)."""
        fig, ax = self.generate()
        plt.tight_layout()
        plt.show()


def create_mapk_pathway(output: str = 'mapk_pathway.pdf'):
    """Create a MAPK signaling pathway diagram."""
    gen = PathwayGenerator(figsize=(10, 6))
    
    # Add nodes
    gen.add_protein('Growth\\nFactor', (1, 5))
    gen.add_protein('Receptor', (2.5, 5))
    gen.add_protein('RAS', (4, 5))
    gen.add_protein('RAF', (5.5, 5))
    gen.add_protein('MEK', (7, 5))
    gen.add_protein('ERK', (8.5, 5))
    gen.add_node('TF', 'tf', (8.5, 3.5))
    gen.add_gene('Target\\nGene', (8.5, 2))
    
    # Add interactions
    gen.add_activation('Growth\\nFactor', 'Receptor')
    gen.add_activation('Receptor', 'RAS')
    gen.add_activation('RAS', 'RAF')
    gen.add_activation('RAF', 'MEK')
    gen.add_activation('MEK', 'ERK')
    gen.add_activation('ERK', 'TF')
    gen.add_activation('TF', 'Target\\nGene')
    
    gen.save(output)
    return gen


def create_simple_pathway(output: str = 'simple_pathway.pdf'):
    """Create a simple 3-node pathway."""
    gen = PathwayGenerator(figsize=(8, 4))
    
    # Linear pathway
    gen.add_protein('Protein A', (2, 3))
    gen.add_protein('Protein B', (5, 3))
    gen.add_protein('Protein C', (8, 3))
    
    gen.add_activation('Protein A', 'Protein B')
    gen.add_activation('Protein B', 'Protein C')
    
    gen.save(output)
    return gen


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description='Generate biological pathway diagrams',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate example pathways
  python pathway_diagram.py --example mapk
  python pathway_diagram.py --example simple
  
  # Custom output
  python pathway_diagram.py --example mapk -o my_pathway.pdf
        """
    )
    
    parser.add_argument('--example',
                       choices=['mapk', 'simple'],
                       help='Generate example pathway')
    parser.add_argument('-o', '--output',
                       help='Output filename (default: based on example)')
    parser.add_argument('--dpi', type=int, default=300,
                       help='DPI for raster output (default: 300)')
    
    args = parser.parse_args()
    
    if not args.example:
        parser.print_help()
        return
    
    # Determine output filename
    if args.output:
        output = args.output
    else:
        output = f"{args.example}_pathway.pdf"
    
    # Generate pathway
    if args.example == 'mapk':
        create_mapk_pathway(output)
    elif args.example == 'simple':
        create_simple_pathway(output)
    
    print(f"\nPathway diagram saved to: {output}")
    print("\nTo use in LaTeX:")
    print(f"  \\includegraphics[width=0.8\\textwidth]{{{output}}}")


if __name__ == '__main__':
    main()

