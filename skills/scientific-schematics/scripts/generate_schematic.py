#!/usr/bin/env python3
"""
Scientific schematic generation using Nano Banana Pro.

Generate any scientific diagram by describing it in natural language.
Nano Banana Pro handles everything automatically with iterative refinement.

Usage:
    # Generate any diagram
    python generate_schematic.py "CONSORT flowchart" -o flowchart.png
    
    # Neural network architecture
    python generate_schematic.py "Transformer architecture" -o transformer.png
    
    # Biological pathway
    python generate_schematic.py "MAPK signaling pathway" -o pathway.png
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description="Generate scientific schematics using AI with iterative refinement",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
How it works:
  Simply describe your diagram in natural language
  Nano Banana Pro generates it automatically with:
  - Iterative refinement (3 rounds by default)
  - Automatic quality review and improvement
  - Publication-ready output

Examples:
  # Generate any diagram
  python generate_schematic.py "CONSORT participant flow" -o flowchart.png
  
  # Custom iterations for complex diagrams
  python generate_schematic.py "Transformer architecture" -o arch.png --iterations 5
  
  # Verbose output
  python generate_schematic.py "Circuit diagram" -o circuit.png -v

Environment Variables:
  OPENROUTER_API_KEY    Required for AI generation
        """
    )
    
    parser.add_argument("prompt", 
                       help="Description of the diagram to generate")
    parser.add_argument("-o", "--output", required=True,
                       help="Output file path")
    parser.add_argument("--iterations", type=int, default=3,
                       help="Number of AI refinement iterations (default: 3)")
    parser.add_argument("--api-key", 
                       help="OpenRouter API key (or use OPENROUTER_API_KEY env var)")
    parser.add_argument("-v", "--verbose", action="store_true",
                       help="Verbose output")
    
    args = parser.parse_args()
    
    # Check for API key
    api_key = args.api_key or os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("Error: OPENROUTER_API_KEY environment variable not set")
        print("\nFor AI generation, you need an OpenRouter API key.")
        print("Get one at: https://openrouter.ai/keys")
        print("\nSet it with:")
        print("  export OPENROUTER_API_KEY='your_api_key'")
        print("\nOr use --api-key flag")
        sys.exit(1)
    
    # Find AI generation script
    script_dir = Path(__file__).parent
    ai_script = script_dir / "generate_schematic_ai.py"
    
    if not ai_script.exists():
        print(f"Error: AI generation script not found: {ai_script}")
        sys.exit(1)
    
    # Build command
    cmd = [sys.executable, str(ai_script), args.prompt, "-o", args.output]
    
    if args.iterations != 3:
        cmd.extend(["--iterations", str(args.iterations)])
    
    if api_key:
        cmd.extend(["--api-key", api_key])
    
    if args.verbose:
        cmd.append("-v")
    
    # Execute
    try:
        result = subprocess.run(cmd, check=False)
        sys.exit(result.returncode)
    except Exception as e:
        print(f"Error executing AI generation: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

