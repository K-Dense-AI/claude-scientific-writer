# Research Lookup Skill

Provides real-time research information lookup with intelligent backend routing: **parallel-cli search** (primary, fast) and the **Parallel Chat API** (deep research only).

## Setup

1. **Install parallel-cli** (primary backend — required):
   ```bash
   curl -fsSL https://parallel.ai/install.sh | bash
   # Or:
   uv tool install "parallel-web-tools[cli]"
   ```

2. **Authenticate:**
   ```bash
   parallel-cli auth
   # Or set directly:
   export PARALLEL_API_KEY="your_parallel_api_key"
   ```

3. **Test Setup:**
   ```bash
   parallel-cli search "test query" --json --max-results 3
   ```

## Usage

### Command Line Usage

```bash
# General research (parallel-cli search — fast, default)
parallel-cli search "Recent advances in CRISPR gene editing 2025" \
  --json --max-results 10 --excerpt-max-chars-total 27000 \
  -o sources/research_crispr.json

# Academic-focused search (include scholarly domains)
parallel-cli search "find papers on CRISPR off-target effects" \
  --json --max-results 10 \
  --include-domains "scholar.google.com,arxiv.org,pubmed.ncbi.nlm.nih.gov,nature.com,science.org,cell.com,pnas.org,nih.gov" \
  -o sources/research_crispr-academic.json

# Deep research via research_lookup.py (Parallel Chat API — slow)
python scripts/research_lookup.py "comprehensive review of mRNA vaccines" --force-backend parallel-chat

# Auto-routed research (detects academic vs general)
python scripts/research_lookup.py "your research query" -o sources/research_topic.md
```

### Integration

The research lookup tool is automatically available when you:

1. **Ask research questions:** "Research recent advances in quantum computing"
2. **Request literature reviews:** "Find current studies on climate change impacts"
3. **Need citations:** "What are the latest papers on transformer attention mechanisms?"
4. **Want technical information:** "Standard protocols for flow cytometry"

## Backend Routing

| Query Type | Backend | Speed |
|------------|---------|-------|
| General research | parallel-cli search | Fast (2-10s) |
| Academic paper queries (contains: "find papers", "doi", "peer-reviewed", etc.) | parallel-cli search + academic domains | Fast (2-10s) |
| Deep/exhaustive research (explicit request) | Parallel Chat API | Slow (60s-5min) |

## Paper Quality Prioritization

When searching for papers, prioritize by:

### Venue Quality Tiers

- **Tier 1 (Highest):** Nature, Science, Cell, NEJM, Lancet, JAMA, PNAS
- **Tier 2 (High):** High-impact journals (IF>10), top conferences (NeurIPS, ICML, ICLR)
- **Tier 3 (Good):** Respected specialized journals (IF 5-10)

### Citation-Based Ranking

| Paper Age | Citation Threshold | Classification |
|-----------|-------------------|----------------|
| 0-3 years | 20+ citations | Noteworthy |
| 0-3 years | 100+ citations | Highly Influential |
| 3-7 years | 100+ citations | Significant |
| 7+ years | 500+ citations | Seminal/Foundational |

## Troubleshooting

**"parallel-cli not found"**
- Install: `curl -fsSL https://parallel.ai/install.sh | bash`

**"Authentication error"**
- Run `parallel-cli auth` or set `PARALLEL_API_KEY`

**"No relevant results"**
- Try more specific queries or add `-q "keyword"` flags
- Include time frames (e.g., `--after-date 2024-01-01`)
- Use `--include-domains` to restrict to high-quality sources

**"Rate limit exceeded"**
- Add delays between requests
- Check your Parallel account limits

## Integration with Scientific Writing

1. **Literature Reviews:** Current research for introduction sections
2. **Methods Validation:** Verify protocols against current standards
3. **Results Context:** Compare findings with recent similar studies
4. **Discussion Support:** Latest evidence for arguments
5. **Citation Management:** Properly formatted references

Always save results to `sources/` for reproducibility and to avoid duplicate queries.
