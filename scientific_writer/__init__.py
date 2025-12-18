"""
Scientific Writer - AI-powered scientific writing assistant.

A powerful Python package for generating scientific papers, literature reviews,
and academic documents.

Example:
    Generate a paper programmatically::

        import asyncio
        from scientific_writer import generate_paper

        async def main():
            async for update in generate_paper("Create a Nature paper on CRISPR"):
                if update["type"] == "text":
                    # Live streaming of Scientific-Writer's responses
                    print(update["content"], end="", flush=True)
                elif update["type"] == "progress":
                    # Structured progress updates
                    print(f"\\n[{update['stage']}] {update['message']}")
                elif update["type"] == "result":
                    print(f"\\nPaper created: {update['paper_directory']}")
                    print(f"PDF: {update['files']['pdf_final']}")

        asyncio.run(main())

    Use the CLI::

        $ scientific-writer
        > Create a NeurIPS paper on transformer attention mechanisms
"""

from .api import generate_paper
from .models import ProgressUpdate, TextUpdate, PaperResult, PaperMetadata, PaperFiles, TokenUsage

__version__ = "2.9.6"
__author__ = "K-Dense"
__license__ = "MIT"

__all__ = [
    "generate_paper",
    "ProgressUpdate",
    "TextUpdate",
    "PaperResult",
    "PaperMetadata",
    "PaperFiles",
    "TokenUsage",
]

