#!/usr/bin/env python3
"""
Generate circuit diagrams using Schemdraw.

This script provides a high-level interface for creating publication-quality
electrical circuit diagrams for scientific papers.

Requirements:
    pip install schemdraw

Usage:
    from circuit_generator import CircuitBuilder
    
    builder = CircuitBuilder()
    builder.add_voltage_source('Vs', '5V')
    builder.add_resistor('R1', '1kΩ')
    builder.add_capacitor('C1', '10µF')
    builder.add_ground()
    builder.save('circuit.pdf')
"""

import argparse
from typing import Optional, Dict, Any

try:
    import schemdraw
    import schemdraw.elements as elm
except ImportError:
    print("Error: schemdraw not installed. Install with: pip install schemdraw")
    exit(1)


class CircuitBuilder:
    """High-level interface for building circuits with Schemdraw."""
    
    def __init__(self, fontsize: int = 10, font: str = 'Arial'):
        """
        Initialize circuit builder.
        
        Args:
            fontsize: Font size for labels
            font: Font family for labels
        """
        self.drawing = schemdraw.Drawing(fontsize=fontsize, font=font)
        self.elements = {}
        self.last_element = None
        
    def add_voltage_source(self, label: str, value: str, 
                          direction: str = 'down') -> 'CircuitBuilder':
        """
        Add a voltage source.
        
        Args:
            label: Element label (e.g., 'Vs')
            value: Voltage value (e.g., '5V')
            direction: up, down, left, right
            
        Returns:
            self for chaining
        """
        element = self.drawing.add(elm.SourceV().label(f'{label}\\n{value}'))
        self.elements[label] = element
        self.last_element = element
        return self
    
    def add_current_source(self, label: str, value: str,
                          direction: str = 'down') -> 'CircuitBuilder':
        """Add a current source."""
        element = self.drawing.add(elm.SourceI().label(f'{label}\\n{value}'))
        self.elements[label] = element
        self.last_element = element
        return self
    
    def add_resistor(self, label: str, value: str, 
                    direction: str = 'right') -> 'CircuitBuilder':
        """
        Add a resistor.
        
        Args:
            label: Element label (e.g., 'R1')
            value: Resistance value (e.g., '1kΩ')
            direction: up, down, left, right
        """
        cmd = getattr(self.drawing.add(elm.Resistor()), direction)
        element = cmd().label(f'{label}\\n{value}')
        self.elements[label] = element
        self.last_element = element
        return self
    
    def add_capacitor(self, label: str, value: str,
                     direction: str = 'down') -> 'CircuitBuilder':
        """Add a capacitor."""
        cmd = getattr(self.drawing.add(elm.Capacitor()), direction)
        element = cmd().label(f'{label}\\n{value}')
        self.elements[label] = element
        self.last_element = element
        return self
    
    def add_inductor(self, label: str, value: str,
                    direction: str = 'right') -> 'CircuitBuilder':
        """Add an inductor."""
        cmd = getattr(self.drawing.add(elm.Inductor()), direction)
        element = cmd().label(f'{label}\\n{value}')
        self.elements[label] = element
        self.last_element = element
        return self
    
    def add_diode(self, label: str, direction: str = 'right') -> 'CircuitBuilder':
        """Add a diode."""
        cmd = getattr(self.drawing.add(elm.Diode()), direction)
        element = cmd().label(label)
        self.elements[label] = element
        self.last_element = element
        return self
    
    def add_led(self, label: str, direction: str = 'right') -> 'CircuitBuilder':
        """Add an LED."""
        cmd = getattr(self.drawing.add(elm.LED()), direction)
        element = cmd().label(label)
        self.elements[label] = element
        self.last_element = element
        return self
    
    def add_opamp(self, label: str) -> 'CircuitBuilder':
        """Add an operational amplifier."""
        element = self.drawing.add(elm.Opamp().label(label))
        self.elements[label] = element
        self.last_element = element
        return self
    
    def add_ground(self) -> 'CircuitBuilder':
        """Add a ground symbol."""
        element = self.drawing.add(elm.Ground())
        self.last_element = element
        return self
    
    def add_line(self, direction: str = 'right', 
                length: Optional[float] = None) -> 'CircuitBuilder':
        """
        Add a connecting wire.
        
        Args:
            direction: up, down, left, right
            length: Optional line length
        """
        line = elm.Line()
        cmd = getattr(line, direction)
        if length:
            element = self.drawing.add(cmd(length))
        else:
            element = self.drawing.add(cmd())
        self.last_element = element
        return self
    
    def add_dot(self, label: Optional[str] = None) -> 'CircuitBuilder':
        """Add a connection dot (for junctions)."""
        element = self.drawing.add(elm.Dot())
        if label:
            element.label(label)
        self.last_element = element
        return self
    
    def push(self) -> 'CircuitBuilder':
        """Save current position (push to stack)."""
        self.drawing.push()
        return self
    
    def pop(self) -> 'CircuitBuilder':
        """Return to saved position (pop from stack)."""
        self.drawing.pop()
        return self
    
    def save(self, filename: str, dpi: int = 300):
        """
        Save circuit diagram.
        
        Args:
            filename: Output filename (.pdf, .svg, .png)
            dpi: Resolution for raster outputs
        """
        if filename.endswith('.png'):
            self.drawing.save(filename, dpi=dpi)
        else:
            self.drawing.save(filename)
        print(f"Circuit saved to {filename}")
    
    def show(self):
        """Display circuit (for interactive use)."""
        self.drawing.draw()


def create_rc_filter(output: str = 'rc_filter.pdf'):
    """Create an RC low-pass filter circuit."""
    builder = CircuitBuilder()
    
    # Input
    builder.add_dot('$V_{in}$')
    builder.add_resistor('R', '1kΩ', 'right')
    
    # Junction
    builder.add_dot()
    builder.push()
    
    # Capacitor to ground
    builder.add_capacitor('C', '10µF', 'down')
    builder.add_ground()
    
    # Output
    builder.pop()
    builder.add_line('right')
    builder.add_dot('$V_{out}$')
    
    builder.save(output)
    return builder


def create_voltage_divider(output: str = 'voltage_divider.pdf'):
    """Create a voltage divider circuit."""
    builder = CircuitBuilder()
    
    # Voltage source
    builder.add_voltage_source('$V_s$', '5V', 'down')
    
    # First resistor
    builder.add_resistor('$R_1$', '1kΩ', 'right')
    
    # Junction and output
    builder.add_dot('$V_{out}$')
    builder.push()
    
    # Second resistor to ground
    builder.add_resistor('$R_2$', '2kΩ', 'down')
    builder.add_line('left')
    builder.add_ground()
    
    builder.save(output)
    return builder


def create_opamp_amplifier(output: str = 'opamp_circuit.pdf'):
    """Create a non-inverting amplifier circuit."""
    builder = CircuitBuilder()
    
    # Input
    builder.add_dot('$V_{in}$')
    builder.add_line('right', 1)
    builder.add_opamp('OA1')
    builder.add_line('right', 1)
    builder.add_dot('$V_{out}$')
    
    builder.save(output)
    return builder


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description='Generate circuit diagrams using Schemdraw',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate example circuits
  python circuit_generator.py --example rc_filter
  python circuit_generator.py --example voltage_divider
  python circuit_generator.py --example opamp
  
  # Custom output
  python circuit_generator.py --example rc_filter -o my_filter.pdf
        """
    )
    
    parser.add_argument('--example', 
                       choices=['rc_filter', 'voltage_divider', 'opamp'],
                       help='Generate example circuit')
    parser.add_argument('-o', '--output', 
                       help='Output filename (default: based on example name)')
    parser.add_argument('--dpi', type=int, default=300,
                       help='DPI for PNG output (default: 300)')
    
    args = parser.parse_args()
    
    if not args.example:
        parser.print_help()
        return
    
    # Determine output filename
    if args.output:
        output = args.output
    else:
        output = f"{args.example}.pdf"
    
    # Generate circuit
    if args.example == 'rc_filter':
        create_rc_filter(output)
    elif args.example == 'voltage_divider':
        create_voltage_divider(output)
    elif args.example == 'opamp':
        create_opamp_amplifier(output)
    
    print(f"\nCircuit diagram saved to: {output}")
    print("\nTo use in LaTeX:")
    print(f"  \\includegraphics{{{output}}}")


if __name__ == '__main__':
    main()

