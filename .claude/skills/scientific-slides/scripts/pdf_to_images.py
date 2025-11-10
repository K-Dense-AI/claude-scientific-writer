#!/usr/bin/env python3
"""
PDF to Images Converter for Presentations

Converts presentation PDFs to images for visual inspection and review.
Supports multiple output formats and resolutions.
"""

import sys
import os
import argparse
import subprocess
from pathlib import Path
from typing import Optional, List

# Try to import pdf2image
try:
    from pdf2image import convert_from_path
    HAS_PDF2IMAGE = True
except ImportError:
    HAS_PDF2IMAGE = False


class PDFToImagesConverter:
    """Converts PDF presentations to images."""
    
    def __init__(
        self,
        pdf_path: str,
        output_prefix: str,
        dpi: int = 150,
        format: str = 'jpg',
        first_page: Optional[int] = None,
        last_page: Optional[int] = None
    ):
        self.pdf_path = Path(pdf_path)
        self.output_prefix = output_prefix
        self.dpi = dpi
        self.format = format.lower()
        self.first_page = first_page
        self.last_page = last_page
        
        # Validate format
        if self.format not in ['jpg', 'jpeg', 'png']:
            raise ValueError(f"Unsupported format: {format}. Use jpg or png.")
    
    def convert(self) -> List[Path]:
        """Convert PDF to images using available method."""
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {self.pdf_path}")
        
        print(f"Converting: {self.pdf_path.name}")
        print(f"Output prefix: {self.output_prefix}")
        print(f"DPI: {self.dpi}")
        print(f"Format: {self.format}")
        
        # Try methods in order of preference
        if HAS_PDF2IMAGE:
            return self._convert_with_pdf2image()
        elif self._has_pdftoppm():
            return self._convert_with_pdftoppm()
        elif self._has_imagemagick():
            return self._convert_with_imagemagick()
        else:
            raise RuntimeError(
                "No conversion tool found. Install one of:\n"
                "  - pdf2image: pip install pdf2image\n"
                "  - poppler-utils (pdftoppm): apt/brew install poppler-utils\n"
                "  - ImageMagick: apt/brew install imagemagick"
            )
    
    def _convert_with_pdf2image(self) -> List[Path]:
        """Convert using pdf2image library."""
        print("Using pdf2image library...")
        
        images = convert_from_path(
            self.pdf_path,
            dpi=self.dpi,
            fmt=self.format,
            first_page=self.first_page,
            last_page=self.last_page
        )
        
        output_files = []
        output_dir = Path(self.output_prefix).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for i, image in enumerate(images, start=1):
            output_path = Path(f"{self.output_prefix}-{i:03d}.{self.format}")
            image.save(output_path, self.format.upper())
            output_files.append(output_path)
            print(f"  Created: {output_path.name}")
        
        return output_files
    
    def _convert_with_pdftoppm(self) -> List[Path]:
        """Convert using pdftoppm command-line tool."""
        print("Using pdftoppm...")
        
        # Build command
        cmd = [
            'pdftoppm',
            '-r', str(self.dpi)
        ]
        
        # Add format flag
        if self.format in ['jpg', 'jpeg']:
            cmd.append('-jpeg')
        else:
            cmd.append('-png')
        
        # Add page range if specified
        if self.first_page:
            cmd.extend(['-f', str(self.first_page)])
        if self.last_page:
            cmd.extend(['-l', str(self.last_page)])
        
        # Add input and output
        cmd.extend([str(self.pdf_path), self.output_prefix])
        
        # Run command
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            # Find generated files
            output_dir = Path(self.output_prefix).parent
            pattern = f"{Path(self.output_prefix).name}-*.{self.format}"
            output_files = sorted(output_dir.glob(pattern))
            
            for f in output_files:
                print(f"  Created: {f.name}")
            
            return output_files
            
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"pdftoppm failed: {e.stderr}")
    
    def _convert_with_imagemagick(self) -> List[Path]:
        """Convert using ImageMagick convert command."""
        print("Using ImageMagick...")
        
        # Build command
        cmd = [
            'convert',
            '-density', str(self.dpi)
        ]
        
        # Add page range if specified
        if self.first_page and self.last_page:
            page_range = f"[{self.first_page-1}-{self.last_page-1}]"
            cmd.append(str(self.pdf_path) + page_range)
        elif self.first_page:
            cmd.append(str(self.pdf_path) + f"[{self.first_page-1}-]")
        elif self.last_page:
            cmd.append(str(self.pdf_path) + f"[0-{self.last_page-1}]")
        else:
            cmd.append(str(self.pdf_path))
        
        # Output path
        output_path = f"{self.output_prefix}-%03d.{self.format}"
        cmd.append(output_path)
        
        # Run command
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            # Find generated files
            output_dir = Path(self.output_prefix).parent
            pattern = f"{Path(self.output_prefix).name}-*.{self.format}"
            output_files = sorted(output_dir.glob(pattern))
            
            for f in output_files:
                print(f"  Created: {f.name}")
            
            return output_files
            
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"ImageMagick failed: {e.stderr}")
    
    def _has_pdftoppm(self) -> bool:
        """Check if pdftoppm is available."""
        try:
            subprocess.run(
                ['pdftoppm', '-v'],
                capture_output=True,
                check=True
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def _has_imagemagick(self) -> bool:
        """Check if ImageMagick is available."""
        try:
            subprocess.run(
                ['convert', '-version'],
                capture_output=True,
                check=True
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False


def main():
    parser = argparse.ArgumentParser(
        description='Convert presentation PDFs to images',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s presentation.pdf slides
    → Creates slides-001.jpg, slides-002.jpg, ...
  
  %(prog)s presentation.pdf output/slide --dpi 300 --format png
    → Creates output/slide-001.png, slide-002.png, ... at high resolution
  
  %(prog)s presentation.pdf review/s --first 5 --last 10
    → Converts only slides 5-10

Output:
  Images are named: PREFIX-001.FORMAT, PREFIX-002.FORMAT, etc.
  
Resolution:
  - 150 DPI: Good for screen review (default)
  - 200 DPI: Higher quality for detailed inspection
  - 300 DPI: Print quality (larger files)

Requirements:
  Install one of these tools:
  - pdf2image: pip install pdf2image (recommended)
  - poppler-utils: apt/brew install poppler-utils
  - ImageMagick: apt/brew install imagemagick
        """
    )
    
    parser.add_argument(
        'pdf_path',
        help='Path to PDF presentation'
    )
    
    parser.add_argument(
        'output_prefix',
        help='Output filename prefix (e.g., "slides" or "output/slide")'
    )
    
    parser.add_argument(
        '--dpi', '-r',
        type=int,
        default=150,
        help='Resolution in DPI (default: 150)'
    )
    
    parser.add_argument(
        '--format', '-f',
        choices=['jpg', 'jpeg', 'png'],
        default='jpg',
        help='Output format (default: jpg)'
    )
    
    parser.add_argument(
        '--first',
        type=int,
        help='First page to convert (1-indexed)'
    )
    
    parser.add_argument(
        '--last',
        type=int,
        help='Last page to convert (1-indexed)'
    )
    
    args = parser.parse_args()
    
    # Create output directory if needed
    output_dir = Path(args.output_prefix).parent
    if output_dir != Path('.'):
        output_dir.mkdir(parents=True, exist_ok=True)
    
    # Convert
    try:
        converter = PDFToImagesConverter(
            pdf_path=args.pdf_path,
            output_prefix=args.output_prefix,
            dpi=args.dpi,
            format=args.format,
            first_page=args.first,
            last_page=args.last
        )
        
        output_files = converter.convert()
        
        print()
        print("=" * 60)
        print(f"✅ Success! Created {len(output_files)} image(s)")
        print("=" * 60)
        
        if output_files:
            print(f"\nFirst image: {output_files[0]}")
            print(f"Last image: {output_files[-1]}")
            
            # Calculate total size
            total_size = sum(f.stat().st_size for f in output_files)
            size_mb = total_size / (1024 * 1024)
            print(f"Total size: {size_mb:.2f} MB")
            
            print("\nNext steps:")
            print("  1. Review images for layout issues")
            print("  2. Check for text overflow or element overlap")
            print("  3. Verify readability from distance")
            print("  4. Document issues with slide numbers")
        
        sys.exit(0)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

