# Research Lookup Skill

This skill provides real-time research information lookup using Perplexity's Sonar Pro model through OpenRouter.

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

## Usage

### Command Line Usage

```bash
# Single research query
python scripts/research_lookup.py "Recent advances in CRISPR gene editing 2024"

# Multiple queries with delay
python scripts/research_lookup.py --batch "CRISPR applications" "gene therapy trials" "ethical considerations"

# Claude Code integration (called automatically)
python lookup.py "your research query here"
```

### Claude Code Integration

The research lookup tool is automatically available in Claude Code when you:

1. **Ask research questions:** "Research recent advances in quantum computing"
2. **Request literature reviews:** "Find current studies on climate change impacts"
3. **Need citations:** "What are the latest papers on transformer attention mechanisms?"
4. **Want technical information:** "Standard protocols for flow cytometry"

## Features

- **Academic Focus:** Prioritizes peer-reviewed papers and reputable sources
- **Current Information:** Focuses on recent publications (2020-2024)
- **Complete Citations:** Provides full bibliographic information with DOIs
- **Multiple Formats:** Supports various query types and research needs
- **Cost Effective:** Typically $0.01-0.05 per research query

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
- Batch processing available for multiple queries
- Consider query specificity to optimize token usage

This skill is designed for academic and research purposes, providing high-quality, cited information to support scientific writing and research activities.
