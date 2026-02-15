---
name: research-lookup
description: "Look up current research information using Parallel Deep Research (primary) or Perplexity sonar-pro-search (academic paper searches). Automatically routes queries to the best backend. Use for finding papers, gathering research data, and verifying scientific information."
allowed-tools: [Read, Write, Edit, Bash]
---

# Research Information Lookup

## Overview

This skill provides real-time research information lookup with **intelligent backend routing**:

- **Parallel Deep Research** (`pro-fast`): Default backend for all general research queries. Provides comprehensive, multi-source intelligence reports with inline citations.
- **Perplexity sonar-pro-search** (via OpenRouter): Used only for academic-specific paper searches where scholarly database access is critical.

The skill automatically detects query type and routes to the optimal backend.

## When to Use This Skill

Use this skill when you need:

- **Current Research Information**: Latest studies, papers, and findings
- **Literature Verification**: Check facts, statistics, or claims against current research
- **Background Research**: Gather context and supporting evidence for scientific writing
- **Citation Sources**: Find relevant papers and studies to cite
- **Technical Documentation**: Look up specifications, protocols, or methodologies
- **Market/Industry Data**: Current statistics, trends, competitive intelligence
- **Recent Developments**: Emerging trends, breakthroughs, announcements

## Visual Enhancement with Scientific Schematics

**When creating documents with this skill, always consider adding scientific diagrams and schematics to enhance visual communication.**

If your document does not already contain schematics or diagrams:
- Use the **scientific-schematics** skill to generate AI-powered publication-quality diagrams
- Simply describe your desired diagram in natural language

```bash
python scripts/generate_schematic.py "your diagram description" -o figures/output.png
```

---

## Automatic Backend Selection

The skill automatically routes queries to the best backend based on content:

### Routing Logic

```
Query arrives
    |
    +-- Contains academic keywords? (papers, DOI, journal, peer-reviewed, etc.)
    |       YES --> Perplexity sonar-pro-search (academic search mode)
    |
    +-- Everything else (general research, market data, technical info, analysis)
            --> Parallel Deep Research (pro-fast processor)
```

### Academic Keywords (Routes to Perplexity)

Queries containing these terms are routed to Perplexity for academic-focused search:

- Paper finding: `find papers`, `find articles`, `research papers on`, `published studies`
- Citations: `cite`, `citation`, `doi`, `pubmed`, `pmid`
- Academic sources: `peer-reviewed`, `journal article`, `scholarly`, `arxiv`, `preprint`
- Review types: `systematic review`, `meta-analysis`, `literature search`
- Paper quality: `foundational papers`, `seminal papers`, `landmark papers`, `highly cited`

### Everything Else (Routes to Parallel)

All other queries go to Parallel Deep Research, including:

- General research questions
- Market and industry analysis
- Technical information and documentation
- Current events and recent developments
- Comparative analysis
- Statistical data retrieval
- Complex analytical queries

### Manual Override

You can force a specific backend:

```bash
# Force Parallel Deep Research
python research_lookup.py "your query" --force-backend parallel

# Force Perplexity academic search
python research_lookup.py "your query" --force-backend perplexity
```

---

## Core Capabilities

### 1. General Research Queries (Parallel Deep Research)

**Default backend.** Provides comprehensive, multi-source research with citations.

```
Query Examples:
- "Recent advances in CRISPR gene editing 2025"
- "Compare mRNA vaccines vs traditional vaccines for cancer treatment"
- "AI adoption in healthcare industry statistics"
- "Global renewable energy market trends and projections"
- "Explain the mechanism underlying gut microbiome and depression"
```

**Response includes:**
- Comprehensive research report in markdown
- Inline citations from authoritative web sources
- Structured sections with key findings
- Multiple perspectives and data points
- Source URLs for verification

### 2. Academic Paper Search (Perplexity sonar-pro-search)

**Used for academic-specific queries.** Prioritizes scholarly databases and peer-reviewed sources.

```
Query Examples:
- "Find papers on transformer attention mechanisms in NeurIPS 2024"
- "Foundational papers on quantum error correction"
- "Systematic review of immunotherapy in non-small cell lung cancer"
- "Cite the original BERT paper and its most influential follow-ups"
- "Published studies on CRISPR off-target effects in clinical trials"
```

**Response includes:**
- Summary of key findings from academic literature
- 5-8 high-quality citations with authors, titles, journals, years, DOIs
- Citation counts and venue tier indicators
- Key statistics and methodology highlights
- Research gaps and future directions

### 3. Technical and Methodological Information

```
Query Examples:
- "Western blot protocol for protein detection"
- "Statistical power analysis for clinical trials"
- "Machine learning model evaluation metrics comparison"
```

### 4. Statistical and Market Data

```
Query Examples:
- "Prevalence of diabetes in US population 2025"
- "Global AI market size and growth projections"
- "COVID-19 vaccination rates by country"
```

---

## Paper Quality and Popularity Prioritization

**CRITICAL**: When searching for papers, ALWAYS prioritize high-quality, influential papers.

### Citation-Based Ranking

| Paper Age | Citation Threshold | Classification |
|-----------|-------------------|----------------|
| 0-3 years | 20+ citations | Noteworthy |
| 0-3 years | 100+ citations | Highly Influential |
| 3-7 years | 100+ citations | Significant |
| 3-7 years | 500+ citations | Landmark Paper |
| 7+ years | 500+ citations | Seminal Work |
| 7+ years | 1000+ citations | Foundational |

### Venue Quality Tiers

**Tier 1 - Premier Venues** (Always prefer):
- **General Science**: Nature, Science, Cell, PNAS
- **Medicine**: NEJM, Lancet, JAMA, BMJ
- **Field-Specific**: Nature Medicine, Nature Biotechnology, Nature Methods
- **Top CS/AI**: NeurIPS, ICML, ICLR, ACL, CVPR

**Tier 2 - High-Impact Specialized** (Strong preference):
- Journals with Impact Factor > 10
- Top conferences in subfields (EMNLP, NAACL, ECCV, MICCAI)

**Tier 3 - Respected Specialized** (Include when relevant):
- Journals with Impact Factor 5-10

---

## Technical Integration

### Environment Variables

```bash
# Primary backend (Parallel Deep Research) - REQUIRED
export PARALLEL_API_KEY="your_parallel_api_key"

# Academic search backend (Perplexity) - REQUIRED for academic queries
export OPENROUTER_API_KEY="your_openrouter_api_key"
```

### API Specifications

**Parallel Deep Research:**
- Processor: `pro-fast` (30s-5min latency)
- Output: Markdown text with inline citations
- Citations: URL-based with excerpts and confidence levels
- Rate limits: Varies by processor tier

**Perplexity sonar-pro-search:**
- Model: `perplexity/sonar-pro-search` (via OpenRouter)
- Search mode: Academic (prioritizes peer-reviewed sources)
- Search context: High (comprehensive research)
- Response time: 5-15 seconds

### Command-Line Usage

```bash
# Auto-routed research (recommended)
python research_lookup.py "your query"

# Force specific backend
python research_lookup.py "your query" --force-backend parallel
python research_lookup.py "your query" --force-backend perplexity

# Save to file
python research_lookup.py "your query" -o results.txt

# JSON output
python research_lookup.py "your query" --json -o results.json

# Batch queries
python research_lookup.py --batch "query 1" "query 2" "query 3"
```

---

## Integration with Scientific Writing

This skill enhances scientific writing by providing:

1. **Literature Review Support**: Gather current research for introduction and discussion
2. **Methods Validation**: Verify protocols against current standards
3. **Results Contextualization**: Compare findings with recent similar studies
4. **Discussion Enhancement**: Support arguments with latest evidence
5. **Citation Management**: Provide properly formatted citations

## Complementary Tools

| Task | Tool |
|------|------|
| General web search | `parallel-web` skill (`parallel_web.py search`) |
| Extract URL content | `parallel-web` skill (`parallel_web.py extract`) |
| Deep research (any topic) | `research-lookup` or `parallel-web` skill |
| Academic paper search | `research-lookup` (auto-routes to Perplexity) |
| Google Scholar search | `citation-management` skill |
| PubMed search | `citation-management` skill |
| DOI to BibTeX | `citation-management` skill |
| Metadata verification | `parallel-web` skill (`parallel_web.py search` or `extract`) |

---

## Error Handling and Limitations

**Known Limitations:**
- Parallel Deep Research: 15,000 character input limit, may take up to 5 minutes
- Perplexity: Information cutoff, may not access full text behind paywalls
- Both: Cannot access proprietary or restricted databases

**Fallback Behavior:**
- If the selected backend's API key is missing, tries the other backend
- If both backends fail, returns structured error response
- Rephrase queries for better results if initial response is insufficient

---

## Usage Examples

### Example 1: General Research (Routes to Parallel)

**Query**: "Recent advances in transformer attention mechanisms 2025"

**Backend**: Parallel Deep Research (pro-fast)

**Response**: Comprehensive markdown report with citations from authoritative sources, covering recent papers, key innovations, and performance benchmarks.

### Example 2: Academic Paper Search (Routes to Perplexity)

**Query**: "Find papers on CRISPR off-target effects in clinical trials"

**Backend**: Perplexity sonar-pro-search (academic mode)

**Response**: Curated list of 5-8 high-impact papers with full citations, DOIs, citation counts, and venue tier indicators.

### Example 3: Comparative Analysis (Routes to Parallel)

**Query**: "Compare and contrast mRNA vaccines vs traditional vaccines for cancer treatment"

**Backend**: Parallel Deep Research (pro-fast)

**Response**: Detailed comparative report with data from multiple sources, structured analysis, and cited evidence.

### Example 4: Market Data (Routes to Parallel)

**Query**: "Global AI adoption in healthcare statistics 2025"

**Backend**: Parallel Deep Research (pro-fast)

**Response**: Current market data, adoption rates, growth projections, and regional analysis with source citations.

---

## Summary

This skill serves as the primary research interface with intelligent dual-backend routing:

- **Parallel Deep Research** (default): Comprehensive, multi-source research for any topic
- **Perplexity sonar-pro-search**: Academic-specific paper searches only
- **Automatic routing**: Detects academic queries and routes appropriately
- **Manual override**: Force any backend when needed
- **Complementary**: Works alongside `parallel-web` skill for web search and URL extraction
