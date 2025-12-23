# Scientific Writer API

**Scientific Writer is a deep research and writing tool** that combines AI-driven deep research with well-formatted written outputs. This API lets you programmatically generate publication-ready documents backed by real-time literature search and verified citations.

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
            print(f"[{update['stage']}] {update['message']}")
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
    track_token_usage: bool = False,
) -> AsyncGenerator[Dict[str, Any], None]
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | `str` | Yes | - | The paper generation request (e.g., "Create a Nature paper on CRISPR") |
| `output_dir` | `str` | No | `None` | Custom output directory. Defaults to `cwd/writing_outputs` |
| `api_key` | `str` | No | `None` | Anthropic API key. Defaults to `ANTHROPIC_API_KEY` env var |
| `model` | `str` | No | `"claude-sonnet-4-20250514"` | Claude model to use |
| `data_files` | `List[str]` | No | `None` | List of file paths to include in the paper |
| `cwd` | `str` | No | `None` | Working directory. Defaults to package parent directory |
| `track_token_usage` | `bool` | No | `False` | If True, track and return token usage in the final result |

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
    "details": dict | None # Optional additional context (tool name, files, etc.)
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
    "errors": List[str],              # Any error messages
    "token_usage": TokenUsage | None  # Token usage (when track_token_usage=True)
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

### `TokenUsage`

Token usage statistics. Only present when `track_token_usage=True`.

**Fields:**
```python
{
    "input_tokens": int,                  # Total input tokens consumed
    "output_tokens": int,                 # Total output tokens generated
    "total_tokens": int,                  # Sum of input + output tokens
    "cache_creation_input_tokens": int,   # Tokens used for cache creation
    "cache_read_input_tokens": int        # Tokens read from cache
}
```

**Example:**
```python
async for update in generate_paper("Create a paper", track_token_usage=True):
    if update["type"] == "result":
        if "token_usage" in update:
            usage = update["token_usage"]
            print(f"Input: {usage['input_tokens']:,} tokens")
            print(f"Output: {usage['output_tokens']:,} tokens")
            print(f"Total: {usage['total_tokens']:,} tokens")
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

### Progress Tracking with Stages

```python
async def track_progress():
    async for update in generate_paper("Create a paper on ML"):
        if update["type"] == "progress":
            # Show stage-based progress
            stage_icons = {
                "initialization": "🔧",
                "research": "🔍",
                "writing": "✍️",
                "compilation": "📦",
                "complete": "✅"
            }
            icon = stage_icons.get(update["stage"], "⏳")
            print(f"{icon} [{update['stage']:12}] {update['message']}")
        else:
            print(f"\n✅ Complete! PDF: {update['files']['pdf_final']}")
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
| `ANTHROPIC_API_KEY` | Yes* | Your Anthropic API key for Scientific-Writer |
| `OPENROUTER_API_KEY` | No | For real-time research lookup via Perplexity Sonar Pro Search |

\* Can be overridden by passing `api_key` parameter to `generate_paper()`

### Research Lookup

When `OPENROUTER_API_KEY` is set, the system gains access to real-time research capabilities:

- **Live internet search** during paper generation
- **Recent publications** from 2024-2025
- **Fact verification** with current data
- **Citation discovery** for latest research

The research lookup is automatically invoked when needed - you don't need to explicitly request it.

### Native Web Search

In addition to research lookup, the system includes Claude's native **WebSearch** tool for:

- **Current events** and general information
- **Non-academic sources** (news, blogs, documentation)
- **Real-time information** that may not be in academic databases
- **Fact-checking** and verification from diverse sources

Both tools work together: use research-lookup for scholarly/academic content, and WebSearch for broader web information.

**Setup:**
```bash
# Add to your .env file
echo "OPENROUTER_API_KEY=your_key_here" >> .env
```

**Example usage:**
```python
# Will automatically use research lookup to find recent papers
async for update in generate_paper(
    "Create a paper on recent advances in quantum computing (2024)"
):
    pass
```

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

## Advanced Features

### Data File Processing

The API automatically processes data files and organizes them appropriately:

```python
async for update in generate_paper(
    query="Analyze experimental results",
    data_files=[
        "./results.csv",           # → copied to data/
        "./performance_plot.png",  # → copied to figures/
        "./supplementary.json"     # → copied to data/
    ]
):
    if update["type"] == "result":
        # Files are available in the paper directory
        data_files = update["files"]["data"]
        figures = update["files"]["figures"]
```

**Note:** When using the API, original files are preserved (not deleted). In CLI mode, they are deleted after copying.

### Intelligent Paper Detection (CLI Only)

The CLI automatically detects references to existing papers:

```bash
# CLI automatically tracks context
> Create a Nature paper on CRISPR
# Creates new paper

> Add a methods section
# Continues editing the CRISPR paper

> Find the acoustics paper
# Switches to the acoustics paper

> new paper on quantum computing
# Explicitly starts a new paper
```

This feature is CLI-specific because the API is stateless. Each `generate_paper()` call creates a new paper.

### Custom Output Organization

Control where papers are saved:

```python
# Custom output directory
async for update in generate_paper(
    query="Create a paper",
    output_dir="~/my_research/papers"
):
    pass

# Custom working directory
async for update in generate_paper(
    query="Create a paper",
    cwd="/path/to/project",
    output_dir="./outputs"
):
    pass
```

### Model Selection

Choose different Claude models (though Sonnet 4.5 is recommended):

```python
async for update in generate_paper(
    query="Create a paper",
    model="claude-sonnet-4-20250514"  # Latest Sonnet 4.5
):
    pass
```

### Token Usage Tracking

Track token consumption for cost monitoring and usage analysis:

```python
async for update in generate_paper(
    query="Create a paper on quantum computing",
    track_token_usage=True
):
    if update["type"] == "result":
        if "token_usage" in update:
            usage = update["token_usage"]
            print(f"Token Usage Summary:")
            print(f"  Input tokens:  {usage['input_tokens']:,}")
            print(f"  Output tokens: {usage['output_tokens']:,}")
            print(f"  Total tokens:  {usage['total_tokens']:,}")
            
            # Cache statistics (if applicable)
            if usage.get('cache_read_input_tokens', 0) > 0:
                print(f"  Cache reads:   {usage['cache_read_input_tokens']:,}")
```

**Notes:**
- Token usage is returned silently (not printed to terminal)
- Available in the final result as a dictionary
- Also included in error results when tracking is enabled
- Useful for cost estimation and monitoring API usage

### Metadata Extraction

The API automatically extracts metadata from generated papers:

```python
async for update in generate_paper(query):
    if update["type"] == "result":
        # Extracted metadata
        title = update["metadata"]["title"]        # From \title{} in LaTeX
        word_count = update["metadata"]["word_count"]  # Estimated from TeX
        created_at = update["metadata"]["created_at"]  # ISO 8601 timestamp
        topic = update["metadata"]["topic"]        # From directory name
        
        # Citation information
        citation_count = update["citations"]["count"]  # From .bib file
        citation_style = update["citations"]["style"]  # BibTeX style
        bib_file = update["citations"]["file"]     # Path to .bib
```

### Progress Monitoring Patterns

#### Simple Stage Display

```python
def format_stage(stage: str) -> str:
    """Format stage name with icon."""
    icons = {
        "initialization": "🔧",
        "research": "🔍", 
        "writing": "✍️",
        "compilation": "📦",
        "complete": "✅"
    }
    return f"{icons.get(stage, '⏳')} {stage}"

async for update in generate_paper(query):
    if update["type"] == "progress":
        print(f"\r{format_stage(update['stage'])}: {update['message']}", end="")

#### Stage-Based Updates

```python
stage_emojis = {
    "initialization": "🔧",
    "research": "🔍",
    "writing": "✍️",
    "compilation": "📦",
    "complete": "✅"
}

async for update in generate_paper(query):
    if update["type"] == "progress":
        emoji = stage_emojis.get(update["stage"], "⏳")
        print(f"{emoji} [{update['stage']}] {update['message']}")
```

#### Logging to File

```python
import json
from datetime import datetime

log_file = "paper_generation.log"

async for update in generate_paper(query):
    # Log all updates
    with open(log_file, "a") as f:
        f.write(json.dumps(update) + "\n")
    
    if update["type"] == "progress":
        print(f"[{update['stage']}] {update['message']}")
```

### Multiple Papers

Generate multiple papers in sequence or parallel:

```python
import asyncio

# Sequential generation
async def generate_multiple_sequential():
    papers = [
        "Create a paper on quantum computing",
        "Create a paper on machine learning",
        "Create a paper on climate change"
    ]
    
    results = []
    for query in papers:
        async for update in generate_paper(query):
            if update["type"] == "result":
                results.append(update)
    
    return results

# Parallel generation (advanced)
async def generate_multiple_parallel():
    async def generate_one(query):
        async for update in generate_paper(query):
            if update["type"] == "result":
                return update
    
    papers = [
        "Create a paper on quantum computing",
        "Create a paper on machine learning",
        "Create a paper on climate change"
    ]
    
    results = await asyncio.gather(*[generate_one(q) for q in papers])
    return results
```

## See Also

- [README.md](../README.md) - Overview and quick start
- [FEATURES.md](FEATURES.md) - Complete features guide
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Troubleshooting issues
- [example_api_usage.py](../example_api_usage.py) - Complete code examples


