---
name: parallel-web
description: "Search the web, extract URL content, and run deep research using Parallel Web Systems APIs. Use for ALL web searches, URL extraction, and general research queries. Provides LLM-optimized results with citations."
allowed-tools: [Read, Write, Edit, Bash]
---

# Parallel Web Systems API

## Overview

This skill provides access to **Parallel Web Systems** APIs for web search, content extraction, and deep research. It is the **primary tool for all web-related operations** in the scientific writer workflow, replacing generic web search tools with purpose-built, LLM-optimized APIs.

**API Documentation:** https://docs.parallel.ai
**API Key:** https://platform.parallel.ai
**Environment Variable:** `PARALLEL_API_KEY`

## When to Use This Skill

Use this skill for **ALL** of the following:

- **Web Search**: Any query that requires searching the internet for information
- **URL Content Extraction**: Reading and extracting content from any public URL
- **Deep Research**: Comprehensive research reports on any topic
- **Market Research**: Industry analysis, competitive intelligence, market data
- **Current Events**: News, recent developments, announcements
- **Technical Information**: Documentation, specifications, product details
- **Metadata Verification**: DOI lookups, citation verification, publication details
- **General Information**: Company profiles, statistics, facts

**Do NOT use this skill for:**
- Academic-specific paper searches (use `research-lookup` which routes to Perplexity for purely academic queries)
- Google Scholar / PubMed database searches (use `citation-management` skill)

---

## Three Capabilities

### 1. Web Search (`ParallelSearch`)

Search the web with natural language objectives and get LLM-optimized excerpts.

**Best for:** General web searches, current events, fact-finding, technical lookups, news.

```bash
# Basic search
python scripts/parallel_web.py search "latest advances in quantum computing 2025"

# Search with additional keyword queries
python scripts/parallel_web.py search "EV market trends" --queries "electric vehicle sales 2025" "EV battery technology"

# Save results to file
python scripts/parallel_web.py search "renewable energy policy updates" -o results.txt

# JSON output for programmatic use
python scripts/parallel_web.py search "AI regulation landscape" --json -o results.json
```

**Key Parameters:**
- `objective`: Natural language description of what you want to find (max 5000 chars)
- `--queries`: Optional keyword queries to supplement the objective
- `--max-results`: Number of results (1-20, default 10)
- `-o`: Output file path
- `--json`: Output as JSON

**Response includes:** URLs, titles, publication dates, focused excerpts optimized for LLM consumption.

### 2. URL Content Extraction (`ParallelExtract`)

Convert any public URL into clean, LLM-optimized markdown. Handles JavaScript-heavy pages and PDFs.

**Best for:** Reading specific web pages, extracting content from known URLs, getting clean text from complex pages.

```bash
# Extract with objective focus
python scripts/parallel_web.py extract "https://example.com/article" --objective "key findings and conclusions"

# Extract multiple URLs
python scripts/parallel_web.py extract "https://url1.com" "https://url2.com" --objective "comparison data"

# Get full page content
python scripts/parallel_web.py extract "https://docs.example.com/api" --full-content

# Save extraction to file
python scripts/parallel_web.py extract "https://paper-url.com" --objective "methodology" -o extracted.md
```

**Key Parameters:**
- `urls`: One or more URLs to extract
- `--objective`: Focus extraction on specific information
- `--full-content`: Return full page content (not just excerpts)
- `-o`: Output file path
- `--json`: Output as JSON

### 3. Deep Research (`ParallelDeepResearch`)

Run comprehensive multi-step web research that produces intelligence reports with inline citations. This is the **primary research engine** for all non-academic queries.

**Best for:** Market research, comprehensive analysis, competitive intelligence, technology surveys, industry reports, any research question requiring synthesis of multiple sources.

```bash
# Default deep research (pro-fast processor, text output)
python scripts/parallel_web.py research "comprehensive analysis of the global EV battery market"

# Save research report to file
python scripts/parallel_web.py research "AI adoption in healthcare 2025" -o report.md

# Use ultra-fast for deeper research
python scripts/parallel_web.py research "compare mRNA vs protein subunit vaccines efficacy and safety" --processor ultra-fast

# Structured JSON output (auto-schema)
python scripts/parallel_web.py research "renewable energy storage market in Europe" --structured --json -o data.json
```

**Key Parameters:**
- `query`: Research question or topic (max 15,000 chars)
- `--processor`: Processing tier (default `pro-fast`)
- `--structured`: Return structured JSON instead of markdown text
- `--timeout`: Max wait time in seconds (default 3600)
- `-o`: Output file path
- `--json`: Output as JSON

---

## Processor Selection Guide

Processors determine the depth, speed, and cost of deep research. Use `pro-fast` by default.

### Standard Processors

| Processor | Latency | Strengths | Use When |
|-----------|---------|-----------|----------|
| `lite` | 10s-60s | Basic metadata | Simple fact lookups |
| `base` | 15s-100s | Standard enrichments | Straightforward questions |
| `core` | 1-5min | Cross-referenced outputs | Moderate complexity |
| `pro` | 2-10min | Exploratory web research | Most research queries |
| `ultra` | 5-25min | Advanced deep research | Comprehensive reports |

### Fast Processors (Recommended)

| Processor | Latency | Strengths | Use When |
|-----------|---------|-----------|----------|
| `lite-fast` | 10-20s | Basic metadata, fastest | Quick lookups |
| `base-fast` | 15-50s | Standard enrichments | Simple questions |
| `core-fast` | 15s-100s | Cross-referenced | Moderate queries |
| **`pro-fast`** | **30s-5min** | **Exploratory research** | **Default for most queries** |
| `ultra-fast` | 1-10min | Deep multi-source | Comprehensive analysis |

**Default recommendation:** Use `pro-fast` for almost all research queries. It provides the best balance of speed, depth, and cost. Use `ultra-fast` only when you need maximum depth and can wait longer.

### Standard vs Fast Trade-off

- **Fast processors** (`-fast` suffix): 2-5x faster, very fresh data, ideal for interactive use
- **Standard processors**: Highest data freshness, better for background/async jobs

Both maintain high accuracy. The difference is in how they prioritize when retrieving data.

---

## Python API Usage

### Search

```python
from parallel_web import ParallelSearch

searcher = ParallelSearch()
result = searcher.search(
    objective="Find latest information about transformer architectures in NLP",
    search_queries=["transformer attention mechanism 2025", "LLM architecture advances"],
    max_results=10,
)

if result["success"]:
    for r in result["results"]:
        print(f"{r['title']}: {r['url']}")
```

### Extract

```python
from parallel_web import ParallelExtract

extractor = ParallelExtract()
result = extractor.extract(
    urls=["https://docs.example.com/api-reference"],
    objective="API authentication methods and rate limits",
)

if result["success"]:
    for r in result["results"]:
        print(r["excerpts"])
```

### Deep Research

```python
from parallel_web import ParallelDeepResearch

researcher = ParallelDeepResearch()

# Text report (markdown with citations)
result = researcher.research(
    query="Comprehensive analysis of AI regulation in the EU and US, focusing on recent policy changes",
    processor="pro-fast",
)

if result["success"]:
    print(result["output"])  # Markdown report
    print(f"Citations: {result['citation_count']}")

# Structured JSON output
result = researcher.research_structured(
    query="Top 5 companies in the cloud computing market with revenue and market share",
    processor="pro-fast",
)

if result["success"]:
    print(result["content"])  # Structured data
    for basis in result["basis"]:
        print(f"Field: {basis['field']}, Confidence: {basis['confidence']}")
```

---

## Integration with Scientific Writer

### Routing Table

| Task | Tool | Command |
|------|------|---------|
| Web search (any) | `parallel_web.py search` | `python scripts/parallel_web.py search "query"` |
| Extract URL content | `parallel_web.py extract` | `python scripts/parallel_web.py extract "url"` |
| Deep research | `parallel_web.py research` | `python scripts/parallel_web.py research "query"` |
| Academic paper search | `research_lookup.py` | Routes to Perplexity sonar-pro-search |
| DOI/metadata lookup | `parallel_web.py search` or `extract` | Search or extract from DOI URLs |
| Current events/news | `parallel_web.py search` | `python scripts/parallel_web.py search "news query"` |

### When Writing Scientific Documents

1. **Before writing any section**, use deep research to gather background information
2. **For academic citations**, use `research-lookup` (which routes academic queries to Perplexity)
3. **For metadata verification** (DOIs, journal names, page numbers), use `parallel_web.py search` or `extract`
4. **For current market/industry data**, use `parallel_web.py research --processor pro-fast`
5. **For reading specific papers/URLs**, use `parallel_web.py extract`

---

## Environment Setup

```bash
# Required: Set your Parallel API key
export PARALLEL_API_KEY="your_api_key_here"

# Install the Python SDK
pip install parallel-web
```

Get your API key at https://platform.parallel.ai

---

## Cost Reference

| API | Cost (per 1,000) | Notes |
|-----|-------------------|-------|
| Search | $5 | Per 1,000 requests (10 results each) |
| Extract | $1 | Per 1,000 URLs |
| Task (pro-fast) | $100 | Per 1,000 task runs |
| Task (ultra-fast) | $300 | Per 1,000 task runs |
| Task (core-fast) | $25 | Per 1,000 task runs |
| Task (base-fast) | $10 | Per 1,000 task runs |

Fast processors have the same pricing as their standard counterparts.

---

## Error Handling

The script handles errors gracefully and returns structured error responses:

```json
{
  "success": false,
  "error": "Error description",
  "timestamp": "2025-02-14 12:00:00"
}
```

**Common issues:**
- `PARALLEL_API_KEY not set`: Set the environment variable
- `parallel-web not installed`: Run `pip install parallel-web`
- `Rate limit exceeded`: Wait and retry (default limits: 600 req/min for Search/Extract, varies for Task)
- `Task timeout`: Increase `--timeout` or use a faster processor

---

## Complementary Skills

| Skill | Use For |
|-------|---------|
| `research-lookup` | Academic paper searches (routes to Perplexity for scholarly queries) |
| `citation-management` | Google Scholar, PubMed, CrossRef database searches |
| `literature-review` | Systematic literature reviews across academic databases |
| `scientific-schematics` | Generate diagrams from research findings |
