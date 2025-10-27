---
name: markitdown
description: "Convert files and office documents to Markdown. Supports PDF, DOCX, PPTX, XLSX, images (with OCR), audio (with transcription), HTML, CSV, JSON, XML, ZIP, YouTube URLs, EPubs and more."
license: MIT
source: https://github.com/microsoft/markitdown
---

# MarkItDown - File to Markdown Conversion

## Overview

MarkItDown is a Python tool developed by Microsoft for converting various file formats to Markdown. It's particularly useful for converting documents into LLM-friendly text format, as Markdown is token-efficient and well-understood by modern language models.

**Key Benefits**:
- Convert documents to clean, structured Markdown
- Token-efficient format for LLM processing
- Supports 15+ file formats
- Optional AI-enhanced image descriptions
- OCR for images and scanned documents
- Speech transcription for audio files

## Supported Formats

| Format | Description | Notes |
|--------|-------------|-------|
| **PDF** | Portable Document Format | Full text extraction |
| **DOCX** | Microsoft Word | Tables, formatting preserved |
| **PPTX** | PowerPoint | Slides with notes |
| **XLSX** | Excel spreadsheets | Tables and data |
| **Images** | JPEG, PNG, GIF, WebP | EXIF metadata + OCR |
| **Audio** | WAV, MP3 | Metadata + transcription |
| **HTML** | Web pages | Clean conversion |
| **CSV** | Comma-separated values | Table format |
| **JSON** | JSON data | Structured representation |
| **XML** | XML documents | Structured format |
| **ZIP** | Archive files | Iterates contents |
| **EPUB** | E-books | Full text extraction |
| **YouTube** | Video URLs | Fetch transcriptions |

## Quick Start

### Installation

```bash
# Install with all features
pip install 'markitdown[all]'

# Or from source
git clone https://github.com/microsoft/markitdown.git
cd markitdown
pip install -e 'packages/markitdown[all]'
```

### Command-Line Usage

```bash
# Basic conversion
markitdown document.pdf > output.md

# Specify output file
markitdown document.pdf -o output.md

# Pipe content
cat document.pdf | markitdown > output.md

# Enable plugins
markitdown --list-plugins  # List available plugins
markitdown --use-plugins document.pdf -o output.md
```

### Python API

```python
from markitdown import MarkItDown

# Basic usage
md = MarkItDown()
result = md.convert("document.pdf")
print(result.text_content)

# Convert from stream
with open("document.pdf", "rb") as f:
    result = md.convert_stream(f, file_extension=".pdf")
    print(result.text_content)
```

## Advanced Features

### 1. AI-Enhanced Image Descriptions

Use LLMs via OpenRouter to generate detailed image descriptions (for PPTX and image files):

```python
from markitdown import MarkItDown
from openai import OpenAI

# Initialize OpenRouter client (OpenAI-compatible API)
client = OpenAI(
    api_key="your-openrouter-api-key",
    base_url="https://openrouter.ai/api/v1"
)

md = MarkItDown(
    llm_client=client,
    llm_model="anthropic/claude-sonnet-4.5",  # recommended for scientific vision
    llm_prompt="Describe this image in detail for scientific documentation"
)

result = md.convert("presentation.pptx")
print(result.text_content)
```

### 2. Azure Document Intelligence

For enhanced PDF conversion with Microsoft Document Intelligence:

```bash
# Command line
markitdown document.pdf -o output.md -d -e "<document_intelligence_endpoint>"
```

```python
# Python API
from markitdown import MarkItDown

md = MarkItDown(docintel_endpoint="<document_intelligence_endpoint>")
result = md.convert("complex_document.pdf")
print(result.text_content)
```

### 3. Plugin System

MarkItDown supports 3rd-party plugins for extending functionality:

```bash
# List installed plugins
markitdown --list-plugins

# Enable plugins
markitdown --use-plugins file.pdf -o output.md
```

Find plugins on GitHub with hashtag: `#markitdown-plugin`

## Optional Dependencies

Control which file formats you support:

```bash
# Install specific formats
pip install 'markitdown[pdf, docx, pptx]'

# All available options:
# [all]                  - All optional dependencies
# [pptx]                 - PowerPoint files
# [docx]                 - Word documents
# [xlsx]                 - Excel spreadsheets
# [xls]                  - Older Excel files
# [pdf]                  - PDF documents
# [outlook]              - Outlook messages
# [az-doc-intel]         - Azure Document Intelligence
# [audio-transcription]  - WAV and MP3 transcription
# [youtube-transcription] - YouTube video transcription
```

## Common Use Cases

### 1. Convert Scientific Papers to Markdown

```python
from markitdown import MarkItDown

md = MarkItDown()

# Convert PDF paper
result = md.convert("research_paper.pdf")
with open("paper.md", "w") as f:
    f.write(result.text_content)
```

### 2. Extract Data from Excel for Analysis

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("data.xlsx")

# Result will be in Markdown table format
print(result.text_content)
```

### 3. Process Multiple Documents

```python
from markitdown import MarkItDown
import os
from pathlib import Path

md = MarkItDown()

# Process all PDFs in a directory
pdf_dir = Path("papers/")
output_dir = Path("markdown_output/")
output_dir.mkdir(exist_ok=True)

for pdf_file in pdf_dir.glob("*.pdf"):
    result = md.convert(str(pdf_file))
    output_file = output_dir / f"{pdf_file.stem}.md"
    output_file.write_text(result.text_content)
    print(f"Converted: {pdf_file.name}")
```

### 4. Convert PowerPoint with AI Descriptions

```python
from markitdown import MarkItDown
from openai import OpenAI

# Use OpenRouter for access to multiple AI models
client = OpenAI(
    api_key="your-openrouter-api-key",
    base_url="https://openrouter.ai/api/v1"
)

md = MarkItDown(
    llm_client=client,
    llm_model="anthropic/claude-sonnet-4.5",  # recommended for presentations
    llm_prompt="Describe this slide image in detail, focusing on key visual elements and data"
)

result = md.convert("presentation.pptx")
with open("presentation.md", "w") as f:
    f.write(result.text_content)
```

### 5. Batch Convert with Different Formats

```python
from markitdown import MarkItDown
from pathlib import Path

md = MarkItDown()

# Files to convert
files = [
    "document.pdf",
    "spreadsheet.xlsx",
    "presentation.pptx",
    "notes.docx"
]

for file in files:
    try:
        result = md.convert(file)
        output = Path(file).stem + ".md"
        with open(output, "w") as f:
            f.write(result.text_content)
        print(f"✓ Converted {file}")
    except Exception as e:
        print(f"✗ Error converting {file}: {e}")
```

### 6. Extract YouTube Video Transcription

```python
from markitdown import MarkItDown

md = MarkItDown()

# Convert YouTube video to transcript
result = md.convert("https://www.youtube.com/watch?v=VIDEO_ID")
print(result.text_content)
```

## Docker Usage

```bash
# Build image
docker build -t markitdown:latest .

# Run conversion
docker run --rm -i markitdown:latest < ~/document.pdf > output.md
```

## Best Practices

### 1. Choose the Right Conversion Method

- **Simple documents**: Use basic `MarkItDown()`
- **Complex PDFs**: Use Azure Document Intelligence
- **Visual content**: Enable AI image descriptions
- **Scanned documents**: Ensure OCR dependencies are installed

### 2. Handle Errors Gracefully

```python
from markitdown import MarkItDown

md = MarkItDown()

try:
    result = md.convert("document.pdf")
    print(result.text_content)
except FileNotFoundError:
    print("File not found")
except Exception as e:
    print(f"Conversion error: {e}")
```

### 3. Process Large Files Efficiently

```python
from markitdown import MarkItDown

md = MarkItDown()

# For large files, use streaming
with open("large_file.pdf", "rb") as f:
    result = md.convert_stream(f, file_extension=".pdf")
    
    # Process in chunks or save directly
    with open("output.md", "w") as out:
        out.write(result.text_content)
```

### 4. Optimize for Token Efficiency

Markdown output is already token-efficient, but you can:
- Remove excessive whitespace
- Consolidate similar sections
- Strip metadata if not needed

```python
from markitdown import MarkItDown
import re

md = MarkItDown()
result = md.convert("document.pdf")

# Clean up extra whitespace
clean_text = re.sub(r'\n{3,}', '\n\n', result.text_content)
clean_text = clean_text.strip()

print(clean_text)
```

## Integration with Scientific Workflows

### Convert Literature for Review

```python
from markitdown import MarkItDown
from pathlib import Path

md = MarkItDown()

# Convert all papers in literature folder
papers_dir = Path("literature/pdfs")
output_dir = Path("literature/markdown")
output_dir.mkdir(exist_ok=True)

for paper in papers_dir.glob("*.pdf"):
    result = md.convert(str(paper))
    
    # Save with metadata
    output_file = output_dir / f"{paper.stem}.md"
    content = f"# {paper.stem}\n\n"
    content += f"**Source**: {paper.name}\n\n"
    content += "---\n\n"
    content += result.text_content
    
    output_file.write_text(content)

# For AI-enhanced conversion with figures
from openai import OpenAI

client = OpenAI(
    api_key="your-openrouter-api-key",
    base_url="https://openrouter.ai/api/v1"
)

md_ai = MarkItDown(
    llm_client=client,
    llm_model="anthropic/claude-sonnet-4.5",
    llm_prompt="Describe scientific figures with technical precision"
)
```

### Extract Tables for Analysis

```python
from markitdown import MarkItDown
import re

md = MarkItDown()
result = md.convert("data_tables.xlsx")

# Markdown tables can be parsed or used directly
print(result.text_content)
```

## Troubleshooting

### Common Issues

1. **Missing dependencies**: Install feature-specific packages
   ```bash
   pip install 'markitdown[pdf]'  # For PDF support
   ```

2. **Binary file errors**: Ensure files are opened in binary mode
   ```python
   with open("file.pdf", "rb") as f:  # Note the "rb"
       result = md.convert_stream(f, file_extension=".pdf")
   ```

3. **OCR not working**: Install tesseract
   ```bash
   # macOS
   brew install tesseract
   
   # Ubuntu
   sudo apt-get install tesseract-ocr
   ```

## Performance Considerations

- **PDF files**: Large PDFs may take time; consider page ranges if supported
- **Image OCR**: OCR processing is CPU-intensive
- **Audio transcription**: Requires additional compute resources
- **AI image descriptions**: Requires API calls (costs may apply)

## Next Steps

- See `references/api_reference.md` for complete API documentation
- Check `references/file_formats.md` for format-specific details
- Review `scripts/batch_convert.py` for automation examples
- Explore `scripts/convert_with_ai.py` for AI-enhanced conversions

## Resources

- **MarkItDown GitHub**: https://github.com/microsoft/markitdown
- **PyPI**: https://pypi.org/project/markitdown/
- **OpenRouter**: https://openrouter.ai (for AI-enhanced conversions)
- **OpenRouter API Keys**: https://openrouter.ai/keys
- **OpenRouter Models**: https://openrouter.ai/models
- **MCP Server**: markitdown-mcp (for Claude Desktop integration)
- **Plugin Development**: See `packages/markitdown-sample-plugin`

