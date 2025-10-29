# Scientific Writer API

Complete reference for the Scientific Writer v2.0 programmatic API. For a quick start, see the README. This page contains full details, examples, and best practices.

## Installation

```bash
# Install with uv (recommended)
uv sync

# Or install in your current environment
uv pip install -e .
```

## Quick Start

```python
import asyncio
from scientific_writer import generate_paper

async def main():
    async for update in generate_paper("Create a Nature paper on CRISPR"):
        if update["type"] == "progress":
            print(f"[{update['percentage']}%] {update['message']}")
        else:
            print(f"PDF: {update['files']['pdf_final']}")

asyncio.run(main())
```

## API Functions

### `generate_paper()`

Asynchronous generator that creates a scientific paper and yields progress updates.

**Signature:**
```python
from typing import AsyncGenerator, Dict, Any, Optional, List

async def generate_paper(
    query: str,
    output_dir: Optional[str] = None,
    api_key: Optional[str] = None,
    model: str = "claude-sonnet-4-20250514",
    data_files: Optional[List[str]] = None,
    cwd: Optional[str] = None,
) -> AsyncGenerator[Dict[str, Any], None]
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | `str` | Yes | - | The paper generation request (e.g., "Create a Nature paper on CRISPR") |
| `output_dir` | `str` | No | `None` | Custom output directory. Defaults to `cwd/paper_outputs` |
| `api_key` | `str` | No | `None` | Anthropic API key. Defaults to `ANTHROPIC_API_KEY` env var |
| `model` | `str` | No | `"claude-sonnet-4-20250514"` | Claude model to use |
| `data_files` | `List[str]` | No | `None` | List of file paths to include in the paper |
| `cwd` | `str` | No | `None` | Working directory. Defaults to package parent directory |

**Returns:**

An async generator that yields:
1. Progress updates (type="progress") during execution
2. Final result (type="result") with comprehensive paper information

**Example:**
```python
import asyncio
from scientific_writer import generate_paper

async def example():
    async for update in generate_paper(
        query="Create a NeurIPS paper on transformers",
        output_dir="./my_papers",
        data_files=["results.csv", "figure.png"],
    ):
        if update["type"] == "progress":
            print(f"[{update['stage']}] {update['message']}")
        else:
            print(f"Done! PDF: {update['files']['pdf_final']}")

asyncio.run(example())
```

## Data Models

### `ProgressUpdate`

Progress information yielded during paper generation.

**Fields:**
```python
{
    "type": "progress",
    "timestamp": str,      # ISO 8601 timestamp
    "message": str,        # Progress message
    "stage": str,          # Current stage (see stages below)
    "percentage": int      # Completion percentage (0-100)
}
```

**Stages:**
- `initialization` - Setting up paper generation
- `research` - Conducting literature research
- `writing` - Writing paper sections
- `compilation` - Compiling LaTeX to PDF
- `complete` - Finalizing and scanning results

### `PaperResult`

Comprehensive final result with all paper information.

**Fields:**
```python
{
    "type": "result",
    "status": str,                    # "success" | "partial" | "failed"
    "paper_directory": str,           # Full path to paper directory
    "paper_name": str,                # Paper directory name
    "metadata": PaperMetadata,        # Paper metadata
    "files": PaperFiles,              # All generated files
    "citations": dict,                # Citation information
    "figures_count": int,             # Number of figures
    "compilation_success": bool,      # Whether PDF was generated
    "errors": List[str]               # Any error messages
}
```

**Status Values:**
- `success` - Paper fully generated with PDF
- `partial` - TeX created but PDF compilation failed
- `failed` - Generation failed (see `errors` field)

### `PaperMetadata`

Metadata about the generated paper.

**Fields:**
```python
{
    "title": Optional[str],      # Extracted paper title
    "created_at": str,           # ISO 8601 timestamp
    "topic": str,                # Topic extracted from directory name
    "word_count": Optional[int]  # Estimated word count
}
```

### `PaperFiles`

Paths to all generated paper files.

**Fields:**
```python
{
    "pdf_final": Optional[str],      # Final PDF path
    "tex_final": Optional[str],      # Final TeX source path
    "pdf_drafts": List[str],         # List of draft PDF paths
    "tex_drafts": List[str],         # List of draft TeX paths
    "bibliography": Optional[str],   # BibTeX file path
    "figures": List[str],            # List of figure file paths
    "data": List[str],               # List of data file paths
    "progress_log": Optional[str],   # progress.md path
    "summary": Optional[str]         # SUMMARY.md path
}
```

## Usage Patterns

### Basic Paper Generation

```python
import asyncio
from scientific_writer import generate_paper

async def create_paper():
    query = "Create a Nature paper on quantum computing"
    
    async for update in generate_paper(query):
        if update["type"] == "progress":
            print(f"Progress: {update['message']}")
        else:
            if update["status"] == "success":
                print(f"Success! PDF: {update['files']['pdf_final']}")
            else:
                print(f"Failed: {update['errors']}")

asyncio.run(create_paper())
```

### Progress Tracking with Percentages

```python
async def track_progress():
    async for update in generate_paper("Create a paper on ML"):
        if update["type"] == "progress":
            # Show progress bar
            bar_length = 50
            filled = int(bar_length * update["percentage"] / 100)
            bar = "█" * filled + "░" * (bar_length - filled)
            print(f"\r[{bar}] {update['percentage']}% - {update['message']}", end="")
        else:
            print(f"\n\nComplete! PDF: {update['files']['pdf_final']}")
```

### Custom Output Directory

```python
async def custom_directory():
    async for update in generate_paper(
        "Create a conference paper",
        output_dir="./my_research/papers"
    ):
        if update["type"] == "result":
            print(f"Paper saved to: {update['paper_directory']}")
```

### Including Data Files

```python
async def with_data_files():
    data_files = [
        "./experiment_results.csv",
        "./figures/performance_graph.png",
        "./appendix_data.json"
    ]
    
    async for update in generate_paper(
        "Create a paper analyzing the experimental results",
        data_files=data_files
    ):
        if update["type"] == "result":
            print(f"Included {len(data_files)} data files")
            print(f"Result has {update['figures_count']} figures")
```

### Save Complete Result to JSON

```python
import json

async def save_to_json():
    result = None
    
    async for update in generate_paper("Create a paper"):
        if update["type"] == "result":
            result = update
    
    if result:
        with open("paper_result.json", "w") as f:
            json.dump(result, f, indent=2)
        print("Result saved to paper_result.json")
```

### Error Handling

```python
async def with_error_handling():
    try:
        async for update in generate_paper("Create a paper"):
            if update["type"] == "progress":
                print(f"[{update['stage']}] {update['message']}")
            else:
                if update["status"] == "failed":
                    print("Generation failed!")
                    for error in update["errors"]:
                        print(f"  Error: {error}")
                elif update["status"] == "partial":
                    print("Partial success")
                    print(f"  TeX file: {update['files']['tex_final']}")
                    print("  PDF compilation failed")
                else:
                    print("Success!")
    except ValueError as e:
        print(f"Configuration error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
```

### Custom API Key

```python
async def with_custom_api_key():
    # Override ANTHROPIC_API_KEY environment variable
    async for update in generate_paper(
        "Create a paper",
        api_key="sk-ant-your-api-key-here"
    ):
        # Process updates...
        pass
```

### Accessing All Generated Files

```python
async def list_all_files():
    async for update in generate_paper("Create a paper"):
        if update["type"] == "result":
            files = update["files"]
            
            print("Generated files:")
            print(f"  PDF: {files['pdf_final']}")
            print(f"  TeX: {files['tex_final']}")
            print(f"  Bibliography: {files['bibliography']}")
            
            print(f"\nDrafts ({len(files['pdf_drafts'])} versions):")
            for draft in files['pdf_drafts']:
                print(f"  - {draft}")
            
            print(f"\nFigures ({len(files['figures'])} files):")
            for fig in files['figures']:
                print(f"  - {fig}")
            
            print(f"\nData files ({len(files['data'])} files):")
            for data in files['data']:
                print(f"  - {data}")
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | Yes* | Your Anthropic API key |
| `OPENROUTER_API_KEY` | No | For research lookup (Perplexity Sonar Pro) |

\* Can be overridden by passing `api_key` parameter to `generate_paper()`

## Error Handling

The API handles errors gracefully:

1. Configuration errors (missing API key): yields a result with `status="failed"`
2. Generation errors: captured in the `errors` field of the result
3. Partial failures: TeX created but PDF failed -> `status="partial"`

## Best Practices

1. Always check update type:
   ```python
   if update["type"] == "progress":
       # Handle progress
   else:  # type == "result"
       # Handle final result
   ```

2. Check status before accessing files:
   ```python
   if update["status"] == "success":
       pdf_path = update["files"]["pdf_final"]
   ```

3. Handle both success and failure:
   ```python
   if update["status"] == "failed":
       print(f"Errors: {update['errors']}")
   elif update["status"] == "partial":
       print("TeX created but PDF failed")
   else:
       print("Success!")
   ```

4. Use async context properly:
   ```python
   import asyncio
   asyncio.run(main())  # For scripts
   ```

5. Save important results:
   ```python
   import json
   with open("result.json", "w") as f:
       json.dump(update, f, indent=2)
   ```

## See Also

- README.md - Overview and quick start
- Docs/TROUBLESHOOTING.md - Troubleshooting issues
- example_api_usage.py - Complete code examples


