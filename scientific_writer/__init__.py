"""
Scientific Writer - AI-powered scientific writing assistant.

A powerful Python package for generating scientific papers, literature reviews,
and academic documents using Claude Sonnet 4.5.

Example:
    Generate a paper programmatically::

        import asyncio
        from scientific_writer import generate_paper

        async def main():
            async for update in generate_paper("Create a Nature paper on CRISPR"):
                if update["type"] == "progress":
                    print(f"[{update['percentage']}%] {update['message']}")
                else:
                    print(f"Paper created: {update['paper_directory']}")
                    print(f"PDF: {update['files']['pdf_final']}")

        asyncio.run(main())

    Use the CLI::

        $ scientific-writer
        > Create a NeurIPS paper on transformer attention mechanisms
"""

from .api import generate_paper
from .models import ProgressUpdate, PaperResult, PaperMetadata, PaperFiles

__version__ = "2.7.0"
__author__ = "K-Dense"
__license__ = "MIT"

__all__ = [
    "generate_paper",
    "ProgressUpdate",
    "PaperResult",
    "PaperMetadata",
    "PaperFiles",
]

