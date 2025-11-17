# Research Lookup Skill

This skill provides real-time research information lookup using Perplexity's Sonar Pro and Sonar Reasoning Pro models through OpenRouter.

**NEW FEATURES:**
- 🚀 **Parallel Research Execution** - Research multiple topics simultaneously (5-10x faster)
- 🤖 **AI-Powered Topic Identification** - Automatically extract research questions from text
- 📁 **Topic File Management** - Save, edit, and reuse research topics
- ⚡ **Complete Workflow Automation** - One-call solution from text to results

## Setup

1. **Get OpenRouter API Key:**
   - Visit [openrouter.ai](https://openrouter.ai)
   - Create account and generate API key
   - Add credits to your account

2. **Configure Environment:**
   ```bash
   export OPENROUTER_API_KEY="your_api_key_here"
   ```

3. **Test Setup:**
   ```bash
   python scripts/research_lookup.py --model-info
   ```

## Quick Start

### Parallel Research Workflow

```bash
# 1. Identify research topics from text and save to file
python research_lookup.py --identify input.txt --topics-file topics.txt

# 2. Review and edit topics.txt (optional)

# 3. Run parallel research on all topics
python research_lookup.py --topics-file topics.txt --parallel --max-workers 10 --output results.json
```

**Result**: 5-10x faster research with comprehensive results saved to JSON.

## Usage

### Command Line Usage

#### Single Query
```bash
# Simple research query
python research_lookup.py "Recent advances in CRISPR gene editing 2024"

# Force specific model
python research_lookup.py "Compare CRISPR vs traditional gene therapy" --force-model reasoning
```

#### Batch Research
```bash
# Sequential (slower, original behavior)
python research_lookup.py --batch "CRISPR applications" "gene therapy trials" "ethical considerations"

# Parallel (much faster, recommended for 3+ queries)
python research_lookup.py --batch "CRISPR applications" "gene therapy trials" "ethical considerations" --parallel --max-workers 5
```

#### Complete Workflow
```bash
# Identify topics and research in one command
python research_lookup.py --identify proposal.txt --topics-file topics.txt --parallel --max-workers 10 --output results.json
```

### Python API Usage

#### Basic Lookup
```python
from research_lookup import ResearchLookup

research = ResearchLookup()
result = research.lookup("Recent advances in mRNA vaccines 2024")
print(result['response'])
```

#### Parallel Research Workflow
```python
# Complete workflow in one call
result = research.identify_and_research(
    text=your_text,
    topics_file="topics.txt",
    parallel=True,
    max_workers=10,
    output_file="results.json"
)

print(f"Researched {result['total_queries']} topics")
print(f"Success: {result['successful_queries']}/{result['total_queries']}")
```

#### Step-by-Step Workflow
```python
# Step 1: Identify topics
topics = research.identify_research_topics(
    text=your_text,
    output_file="topics.txt"
)

# Step 2: Review/edit topics.txt manually

# Step 3: Load and research in parallel
topics = research.load_topics_from_file("topics.txt")
results = research.parallel_lookup(topics, max_workers=10)

# Process results
for result in results:
    if result['success']:
        print(f"Query: {result['query']}")
        print(f"Response: {result['response']}")
```

### Claude Code Integration

The research lookup tool is automatically available in Claude Code when you:

1. **Ask research questions:** "Research recent advances in quantum computing"
2. **Request literature reviews:** "Find current studies on climate change impacts"
3. **Need citations:** "What are the latest papers on transformer attention mechanisms?"
4. **Want technical information:** "Standard protocols for flow cytometry"

## Features

### Core Capabilities
- **Academic Focus:** Prioritizes peer-reviewed papers and reputable sources
- **Current Information:** Focuses on recent publications (2020-2024)
- **Complete Citations:** Provides full bibliographic information with DOIs
- **Multiple Formats:** Supports various query types and research needs
- **Intelligent Model Selection:** Automatically chooses between Sonar Pro (fast) and Sonar Reasoning Pro (deep analysis)

### New Parallel Research Features
- **🚀 Parallel Execution:** Research multiple topics simultaneously (5-10x faster)
- **🤖 AI Topic Identification:** Automatically extract research questions from text
- **📁 File Management:** Save, load, and reuse research topics
- **⚡ Complete Automation:** One-command workflow from text to results
- **📊 Progress Tracking:** Real-time status updates during parallel execution
- **💾 JSON Export:** Structured results for programmatic processing

### Performance Comparison

| Queries | Sequential Time | Parallel Time (10 workers) | Speedup |
|---------|----------------|---------------------------|---------|
| 5       | ~60 seconds    | ~15 seconds              | 4x      |
| 10      | ~120 seconds   | ~20 seconds              | 6x      |
| 20      | ~240 seconds   | ~35 seconds              | 7x      |
| 50      | ~600 seconds   | ~90 seconds              | 7x      |

**Cost**: $0.01-0.05 per research query (same as sequential)

## Query Examples

### Academic Research
- "Recent systematic reviews on AI in medical diagnosis 2024"
- "Meta-analysis of randomized controlled trials for depression treatment"
- "Current state of quantum computing error correction research"

### Technical Methods
- "Standard protocols for immunohistochemistry in tissue samples"
- "Best practices for machine learning model validation"
- "Statistical methods for analyzing longitudinal data"

### Statistical Data
- "Global renewable energy adoption statistics 2024"
- "Prevalence of diabetes in different populations"
- "Market size for autonomous vehicles industry"

## Response Format

Each research result includes:
- **Summary:** Brief overview of key findings
- **Key Studies:** 3-5 most relevant recent papers
- **Citations:** Complete bibliographic information
- **Usage Stats:** Token usage for cost tracking
- **Timestamp:** When the research was performed

## Integration with Scientific Writing

This skill enhances the scientific writing process by providing:

1. **Literature Reviews:** Current research for introduction sections
2. **Methods Validation:** Verify protocols against current standards
3. **Results Context:** Compare findings with recent similar studies
4. **Discussion Support:** Latest evidence for arguments
5. **Citation Management:** Properly formatted references

## Troubleshooting

**"API key not found"**
- Ensure `OPENROUTER_API_KEY` environment variable is set
- Check that you have credits in your OpenRouter account

**"Model not available"**
- Verify your API key has access to Perplexity models
- Check OpenRouter status page for service issues

**"Rate limit exceeded"**
- Add delays between requests using `--delay` option
- Check your OpenRouter account limits

**"No relevant results"**
- Try more specific or broader queries
- Include time frames (e.g., "2023-2024")
- Use academic keywords and technical terms

## Cost Management

- Monitor usage through OpenRouter dashboard
- Typical costs: $0.01-0.05 per research query
- Parallel execution uses same cost per query, just faster
- Consider query specificity to optimize token usage
- Use `--topics-file` to save and reuse topics (avoid re-identification costs)

## Best Practices

### When to Use Parallel Research
- ✅ **5+ research questions** - Significant time savings
- ✅ **Literature reviews** - Research multiple papers simultaneously  
- ✅ **Grant applications** - Gather supporting evidence quickly
- ✅ **Manuscript drafts** - Citation research for multiple sections
- ❌ **Single queries** - No benefit, use standard lookup
- ❌ **< 3 queries** - Overhead may negate benefits

### Optimizing Performance
1. **Worker Count**: Start with 5-10 workers, increase if no rate limits
2. **Topic Quality**: Review and refine AI-identified topics before researching
3. **File Reuse**: Save topics to file for iterative refinement
4. **Result Processing**: Use JSON output for programmatic analysis
5. **Model Selection**: Let automatic selection choose optimal model (Pro vs Reasoning)

### Workflow Recommendations

**For Quick Research (< 5 queries):**
```bash
python research_lookup.py --batch "query1" "query2" "query3" --parallel
```

**For Comprehensive Research (5-50 queries):**
```bash
# Step 1: Identify
python research_lookup.py --identify input.txt --topics-file topics.txt

# Step 2: Review and edit topics.txt

# Step 3: Research in parallel
python research_lookup.py --topics-file topics.txt --parallel --max-workers 10 --output results.json
```

**For Recurring Research:**
```bash
# Create and maintain a topics file
echo "Recent advances in X" >> recurring_topics.txt
echo "Latest studies on Y" >> recurring_topics.txt

# Run weekly/monthly
python research_lookup.py --topics-file recurring_topics.txt --parallel --output "results_$(date +%Y%m%d).json"
```

## Examples

See the `examples/` directory for comprehensive usage examples:
- `parallel_research_workflow.py` - Complete workflow demonstrations
- `examples/README.md` - Detailed examples documentation

Run all examples:
```bash
cd examples
python parallel_research_workflow.py
```

## Additional Resources

- **Full Documentation**: See `SKILL.md` for comprehensive documentation
- **API Reference**: See docstrings in `research_lookup.py`
- **Examples**: See `examples/` directory for working code
- **Support**: Check troubleshooting section below

This skill is designed for academic and research purposes, providing high-quality, cited information to support scientific writing and research activities.
