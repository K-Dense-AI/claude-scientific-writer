#!/usr/bin/env python3
"""
Compile TikZ diagrams to PDF and PNG.

This script provides a convenient interface for compiling standalone TikZ
files to various output formats, with options for preview and cleanup.

Requirements:
    - pdflatex (from TeX distribution)
    - convert (ImageMagick, for PNG output)

Usage:
    python compile_tikz.py diagram.tex
    python compile_tikz.py diagram.tex --png --dpi 300
    python compile_tikz.py diagram.tex --preview
"""

import argparse
import os
import subprocess
import sys
import tempfile
import shutil
from pathlib import Path
from typing import Optional, List


class TikZCompiler:
    """Compile TikZ diagrams to various formats."""
    
    def __init__(self, verbose: bool = False):
        """
        Initialize compiler.
        
        Args:
            verbose: Print detailed output
        """
        self.verbose = verbose
        
    def _run_command(self, cmd: List[str], cwd: Optional[str] = None) -> bool:
        """Run a command and return success status."""
        if self.verbose:
            print(f"Running: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd, 
                cwd=cwd,
                stdout=subprocess.PIPE if not self.verbose else None,
                stderr=subprocess.PIPE if not self.verbose else None,
                text=True
            )
            
            if result.returncode != 0:
                if not self.verbose and result.stderr:
                    print(f"Error: {result.stderr}")
                return False
            return True
            
        except FileNotFoundError:
            print(f"Error: Command not found: {cmd[0]}")
            return False
        except Exception as e:
            print(f"Error running command: {e}")
            return False
    
    def compile_to_pdf(self, tex_file: str, output: Optional[str] = None,
                      cleanup: bool = True) -> Optional[str]:
        """
        Compile TikZ file to PDF.
        
        Args:
            tex_file: Input .tex file
            output: Output .pdf filename (default: same as input)
            cleanup: Remove auxiliary files
            
        Returns:
            Path to output PDF if successful, None otherwise
        """
        tex_path = Path(tex_file).resolve()
        
        if not tex_path.exists():
            print(f"Error: File not found: {tex_file}")
            return None
        
        # Determine output path
        if output:
            pdf_path = Path(output).resolve()
        else:
            pdf_path = tex_path.with_suffix('.pdf')
        
        # Create temporary directory for compilation
        with tempfile.TemporaryDirectory() as tmpdir:
            # Copy tex file to temp directory
            temp_tex = Path(tmpdir) / tex_path.name
            shutil.copy(tex_path, temp_tex)
            
            # Copy any additional files (tikz_styles.tex, etc.)
            for aux_file in tex_path.parent.glob('*.tex'):
                if aux_file != tex_path:
                    shutil.copy(aux_file, tmpdir)
            
            # Compile with pdflatex
            print(f"Compiling {tex_path.name} to PDF...")
            
            # Run pdflatex (may need to run twice for references)
            for i in range(2):
                success = self._run_command(
                    ['pdflatex', '-interaction=nonstopmode', temp_tex.name],
                    cwd=tmpdir
                )
                
                if not success:
                    print(f"Compilation failed (pass {i+1}/2)")
                    if i == 1:  # Only fail on second pass
                        return None
            
            # Copy PDF to output location
            temp_pdf = temp_tex.with_suffix('.pdf')
            if temp_pdf.exists():
                shutil.copy(temp_pdf, pdf_path)
                print(f"✓ PDF created: {pdf_path}")
                return str(pdf_path)
            else:
                print("Error: PDF not created")
                return None
    
    def pdf_to_png(self, pdf_file: str, output: Optional[str] = None,
                   dpi: int = 300) -> Optional[str]:
        """
        Convert PDF to PNG using ImageMagick.
        
        Args:
            pdf_file: Input PDF file
            output: Output PNG filename (default: same as input)
            dpi: Resolution in DPI
            
        Returns:
            Path to output PNG if successful, None otherwise
        """
        pdf_path = Path(pdf_file)
        
        if not pdf_path.exists():
            print(f"Error: PDF not found: {pdf_file}")
            return None
        
        # Determine output path
        if output:
            png_path = Path(output)
        else:
            png_path = pdf_path.with_suffix('.png')
        
        print(f"Converting to PNG ({dpi} DPI)...")
        
        # Use ImageMagick convert
        success = self._run_command([
            'convert',
            '-density', str(dpi),
            '-quality', '100',
            str(pdf_path),
            '-flatten',  # Remove transparency
            str(png_path)
        ])
        
        if success and png_path.exists():
            print(f"✓ PNG created: {png_path}")
            return str(png_path)
        else:
            print("Error: PNG conversion failed")
            print("Hint: Make sure ImageMagick is installed")
            return None
    
    def preview_pdf(self, pdf_file: str) -> bool:
        """
        Open PDF in system viewer.
        
        Args:
            pdf_file: PDF file to preview
            
        Returns:
            True if successful
        """
        pdf_path = Path(pdf_file)
        
        if not pdf_path.exists():
            print(f"Error: PDF not found: {pdf_file}")
            return False
        
        print(f"Opening {pdf_path.name}...")
        
        # Determine system-specific open command
        if sys.platform == 'darwin':  # macOS
            cmd = ['open', str(pdf_path)]
        elif sys.platform.startswith('linux'):  # Linux
            cmd = ['xdg-open', str(pdf_path)]
        elif sys.platform == 'win32':  # Windows
            cmd = ['start', str(pdf_path)]
        else:
            print(f"Error: Unsupported platform: {sys.platform}")
            return False
        
        return self._run_command(cmd)


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description='Compile TikZ diagrams to PDF and PNG',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Compile to PDF
  python compile_tikz.py diagram.tex
  
  # Compile to PDF and PNG
  python compile_tikz.py diagram.tex --png --dpi 300
  
  # Compile and preview
  python compile_tikz.py diagram.tex --preview
  
  # Custom output filenames
  python compile_tikz.py diagram.tex -o my_diagram.pdf
  python compile_tikz.py diagram.tex --png --png-output my_diagram.png
  
  # Verbose output
  python compile_tikz.py diagram.tex --verbose
        """
    )
    
    parser.add_argument('input', help='Input .tex file')
    parser.add_argument('-o', '--output', help='Output PDF filename')
    parser.add_argument('--png', action='store_true', 
                       help='Also generate PNG')
    parser.add_argument('--png-output', help='PNG output filename')
    parser.add_argument('--dpi', type=int, default=300,
                       help='DPI for PNG output (default: 300)')
    parser.add_argument('--preview', action='store_true',
                       help='Open PDF after compilation')
    parser.add_argument('--no-cleanup', action='store_true',
                       help='Keep auxiliary files')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Verbose output')
    
    args = parser.parse_args()
    
    # Check input file
    if not Path(args.input).exists():
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)
    
    if not args.input.endswith('.tex'):
        print("Warning: Input file doesn't have .tex extension")
    
    # Initialize compiler
    compiler = TikZCompiler(verbose=args.verbose)
    
    # Compile to PDF
    pdf_file = compiler.compile_to_pdf(
        args.input,
        output=args.output,
        cleanup=not args.no_cleanup
    )
    
    if not pdf_file:
        print("\n❌ Compilation failed")
        sys.exit(1)
    
    # Convert to PNG if requested
    if args.png:
        png_file = compiler.pdf_to_png(
            pdf_file,
            output=args.png_output,
            dpi=args.dpi
        )
        
        if not png_file:
            print("\n⚠ PDF created but PNG conversion failed")
    
    # Preview if requested
    if args.preview:
        compiler.preview_pdf(pdf_file)
    
    print("\n✓ Done!")
    print(f"\nTo use in LaTeX:")
    print(f"  \\input{{{Path(pdf_file).stem}.tex}}")
    print(f"  or")
    print(f"  \\includegraphics{{{Path(pdf_file).name}}}")


if __name__ == '__main__':
    main()

