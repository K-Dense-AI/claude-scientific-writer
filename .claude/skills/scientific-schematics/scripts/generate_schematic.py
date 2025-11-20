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


def generate_ai(prompt: str, output: str, iterations: int = 3, 
               api_key: str = None, verbose: bool = False) -> int:
    """
    Generate schematic using AI method.
    
    Args:
        prompt: Description of diagram
        output: Output file path
        iterations: Number of refinement iterations
        api_key: OpenRouter API key
        verbose: Verbose output
        
    Returns:
        Exit code (0 for success)
    """
    script_dir = Path(__file__).parent
    ai_script = script_dir / "generate_schematic_ai.py"
    
    if not ai_script.exists():
        print(f"Error: AI generation script not found: {ai_script}")
        return 1
    
    # Build command
    cmd = [sys.executable, str(ai_script), prompt, "-o", output]
    
    if iterations != 3:
        cmd.extend(["--iterations", str(iterations)])
    
    if api_key:
        cmd.extend(["--api-key", api_key])
    
    if verbose:
        cmd.append("-v")
    
    # Execute
    try:
        result = subprocess.run(cmd, check=False)
        return result.returncode
    except Exception as e:
        print(f"Error executing AI generation: {e}")
        return 1


def generate_code(prompt: str, output: str, diagram_type: str = "tikz",
                 verbose: bool = False) -> int:
    """
    Generate schematic using code-based method (TikZ compilation).
    
    Note: Code-based generation is now limited. For most use cases,
    use AI generation instead (--method ai).
    
    Args:
        prompt: TikZ code or file path
        output: Output file path
        diagram_type: Type of diagram (currently only 'tikz' supported)
        verbose: Verbose output
        
    Returns:
        Exit code (0 for success)
    """
    print("Note: Code-based generation has been simplified.")
    print("For diagram generation, use --method ai (default)")
    print("")
    print("If you have TikZ code to compile, use:")
    print("  python scripts/compile_tikz.py your_file.tex -o output.pdf")
    print("")
    print("For AI generation:")
    print("  python scripts/generate_schematic.py 'diagram description' -o output.png")
    return 1


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description="Generate scientific schematics using AI or code-based methods",
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
  OPENROUTER_API_KEY    Required for AI method
        """
    )
    
    parser.add_argument("prompt", 
                       help="Description or content of the diagram")
    parser.add_argument("-o", "--output", required=True,
                       help="Output file path")
    parser.add_argument("--method", choices=["ai", "code"], default="ai",
                       help="Generation method (default: ai)")
    parser.add_argument("--iterations", type=int, default=3,
                       help="Number of AI refinement iterations (default: 3)")
    parser.add_argument("--api-key", 
                       help="OpenRouter API key for AI method")
    parser.add_argument("-v", "--verbose", action="store_true",
                       help="Verbose output")
    
    args = parser.parse_args()
    
    # Route to appropriate method
    if args.method == "ai":
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
        
        exit_code = generate_ai(
            prompt=args.prompt,
            output=args.output,
            iterations=args.iterations,
            api_key=api_key,
            verbose=args.verbose
        )
    else:  # code method (deprecated)
        exit_code = generate_code(
            prompt=args.prompt,
            output=args.output,
            verbose=args.verbose
        )
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()

