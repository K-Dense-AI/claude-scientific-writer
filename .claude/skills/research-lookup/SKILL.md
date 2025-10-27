---
name: research-lookup
description: "Look up current research information using Perplexity's Sonar Pro or Sonar Reasoning Pro models through OpenRouter. Automatically selects the best model based on query complexity. Search academic papers, recent studies, technical documentation, and general research information with citations."
---

# Research Information Lookup

## Overview

This skill enables real-time research information lookup using Perplexity's Sonar models through OpenRouter. It intelligently selects between **Sonar Pro** (fast, efficient lookup) and **Sonar Reasoning Pro** (deep analytical reasoning) based on query complexity. The skill provides access to current academic literature, recent studies, technical documentation, and general research information with proper citations and source attribution.

## When to Use This Skill

Use this skill when you need:

- **Current Research Information**: Latest studies, papers, and findings in a specific field
- **Literature Verification**: Check facts, statistics, or claims against current research
- **Background Research**: Gather context and supporting evidence for scientific writing
- **Citation Sources**: Find relevant papers and studies to cite in manuscripts
- **Technical Documentation**: Look up specifications, protocols, or methodologies
- **Recent Developments**: Stay current with emerging trends and breakthroughs
- **Statistical Data**: Find recent statistics, survey results, or research findings
- **Expert Opinions**: Access insights from recent interviews, reviews, or commentary

## Core Capabilities

### 1. Academic Research Queries

**Search Academic Literature**: Query for recent papers, studies, and reviews in specific domains:

```
Query Examples:
- "Recent advances in CRISPR gene editing 2024"
- "Latest clinical trials for Alzheimer's disease treatment"
- "Machine learning applications in drug discovery systematic review"
- "Climate change impacts on biodiversity meta-analysis"
```

**Expected Response Format**:
- Summary of key findings from recent literature
- Citation of 3-5 most relevant papers with authors, titles, journals, and years
- Key statistics or findings highlighted
- Identification of research gaps or controversies
- Links to full papers when available

### 2. Technical and Methodological Information

**Protocol and Method Lookups**: Find detailed procedures, specifications, and methodologies:

```
Query Examples:
- "Western blot protocol for protein detection"
- "RNA sequencing library preparation methods"
- "Statistical power analysis for clinical trials"
- "Machine learning model evaluation metrics"
```

**Expected Response Format**:
- Step-by-step procedures or protocols
- Required materials and equipment
- Critical parameters and considerations
- Troubleshooting common issues
- References to standard protocols or seminal papers

### 3. Statistical and Data Information

**Research Statistics**: Look up current statistics, survey results, and research data:

```
Query Examples:
- "Prevalence of diabetes in US population 2024"
- "Global renewable energy adoption statistics"
- "COVID-19 vaccination rates by country"
- "AI adoption in healthcare industry survey"
```

**Expected Response Format**:
- Current statistics with dates and sources
- Methodology of data collection
- Confidence intervals or margins of error when available
- Comparison with previous years or benchmarks
- Citations to original surveys or studies

### 4. Citation and Reference Assistance

**Citation Finding**: Locate relevant papers and studies for citation in manuscripts:

```
Query Examples:
- "Foundational papers on transformer architecture"
- "Seminal works in quantum computing"
- "Key studies on climate change mitigation"
- "Landmark trials in cancer immunotherapy"
```

**Expected Response Format**:
- 5-10 most influential or relevant papers
- Complete citation information (authors, title, journal, year, DOI)
- Brief description of each paper's contribution
- Citation impact metrics when available (h-index, citation count)
- Journal impact factors and rankings

## Automatic Model Selection

This skill features **intelligent model selection** based on query complexity:

### Model Types

**1. Sonar Pro** (`perplexity/sonar-pro`)
- **Use Case**: Straightforward information lookup
- **Best For**: 
  - Simple fact-finding queries
  - Recent publication searches
  - Basic protocol lookups
  - Statistical data retrieval
- **Speed**: Fast responses
- **Cost**: Lower cost per query

**2. Sonar Reasoning Pro** (`perplexity/sonar-reasoning-pro`)
- **Use Case**: Complex analytical queries requiring deep reasoning
- **Best For**:
  - Comparative analysis ("compare X vs Y")
  - Synthesis of multiple studies
  - Evaluating trade-offs or controversies
  - Explaining mechanisms or relationships
  - Critical analysis and interpretation
- **Speed**: Slower but more thorough
- **Cost**: Higher cost per query, but provides deeper insights

### Complexity Assessment

The skill automatically detects query complexity using these indicators:

**Reasoning Keywords** (triggers Sonar Reasoning Pro):
- Analytical: `compare`, `contrast`, `analyze`, `analysis`, `evaluate`, `critique`
- Comparative: `versus`, `vs`, `vs.`, `compared to`, `differences between`, `similarities`
- Synthesis: `meta-analysis`, `systematic review`, `synthesis`, `integrate`
- Causal: `mechanism`, `why`, `how does`, `how do`, `explain`, `relationship`, `causal relationship`, `underlying mechanism`
- Theoretical: `theoretical framework`, `implications`, `interpret`, `reasoning`
- Debate: `controversy`, `conflicting`, `paradox`, `debate`, `reconcile`
- Trade-offs: `pros and cons`, `advantages and disadvantages`, `trade-off`, `tradeoff`, `trade offs`
- Complexity: `multifaceted`, `complex interaction`, `critical analysis`

**Complexity Scoring**:
- Reasoning keywords: 3 points each (heavily weighted)
- Multiple questions: 2 points per question mark
- Complex sentence structures: 1.5 points per clause indicator (and, or, but, however, whereas, although)
- Very long queries: 1 point if >150 characters
- **Threshold**: Queries scoring ≥3 points trigger Sonar Reasoning Pro

**Practical Result**: Even a single strong reasoning keyword (compare, explain, analyze, etc.) will trigger the more powerful Sonar Reasoning Pro model, ensuring you get deep analysis when needed.

**Example Query Classification**:

✅ **Sonar Pro** (straightforward lookup):
- "Recent advances in CRISPR gene editing 2024"
- "Prevalence of diabetes in US population"
- "Western blot protocol for protein detection"

✅ **Sonar Reasoning Pro** (complex analysis):
- "Compare and contrast mRNA vaccines vs traditional vaccines for cancer treatment"
- "Explain the mechanism underlying the relationship between gut microbiome and depression"
- "Analyze the controversy surrounding AI in medical diagnosis and evaluate trade-offs"

### Manual Override

You can force a specific model using the `force_model` parameter:

```python
# Force Sonar Pro for fast lookup
research = ResearchLookup(force_model='pro')

# Force Sonar Reasoning Pro for deep analysis
research = ResearchLookup(force_model='reasoning')

# Automatic selection (default)
research = ResearchLookup()
```

Command-line usage:
```bash
# Force Sonar Pro
python research_lookup.py "your query" --force-model pro

# Force Sonar Reasoning Pro
python research_lookup.py "your query" --force-model reasoning

# Automatic (no flag)
python research_lookup.py "your query"
```

## Technical Integration

### OpenRouter API Configuration

This skill integrates with OpenRouter (openrouter.ai) to access Perplexity's Sonar models:

**Model Specifications**:
- **Models**: 
  - `perplexity/sonar-pro-online` (fast lookup)
  - `perplexity/sonar-reasoning-pro-online` (deep analysis)
- **Search Mode**: Academic/scholarly mode (prioritizes peer-reviewed sources)
- **Context Window**: 200K+ tokens for comprehensive research
- **Capabilities**: Academic paper search, citation generation, scholarly analysis
- **Output**: Rich responses with citations and source links from academic databases

**API Requirements**:
- OpenRouter API key (set as `OPENROUTER_API_KEY` environment variable)
- Account with sufficient credits for research queries
- Proper attribution and citation of sources

**Academic Mode Configuration**:
- System message configured to prioritize scholarly sources
- Search focused on peer-reviewed journals and academic publications
- Enhanced citation extraction for academic references
- Preference for recent academic literature (2020-2024)
- Direct access to academic databases and repositories

### Response Quality and Reliability

**Source Verification**: The skill prioritizes:
- Peer-reviewed academic papers and journals
- Reputable institutional sources (universities, government agencies, NGOs)
- Recent publications (within last 2-3 years preferred)
- High-impact journals and conferences
- Primary research over secondary sources

**Citation Standards**: All responses include:
- Complete bibliographic information
- DOI or stable URLs when available
- Access dates for web sources
- Clear attribution of direct quotes or data

## Query Best Practices

### 1. Model Selection Strategy

**For Simple Lookups (Sonar Pro)**:
- Recent papers on a specific topic
- Statistical data or prevalence rates
- Standard protocols or methodologies
- Citation finding for specific papers
- Factual information retrieval

**For Complex Analysis (Sonar Reasoning Pro)**:
- Comparative studies and synthesis
- Mechanism explanations
- Controversy evaluation
- Trade-off analysis
- Theoretical frameworks
- Multi-faceted relationships

**Pro Tip**: The automatic selection is optimized for most use cases. Only use `force_model` if you have specific requirements or know the query needs deeper reasoning than detected.

### 2. Specific and Focused Queries

**Good Queries** (will trigger appropriate model):
- "Randomized controlled trials of mRNA vaccines for cancer treatment 2023-2024" → Sonar Pro
- "Compare the efficacy and safety of mRNA vaccines vs traditional vaccines for cancer treatment" → Sonar Reasoning Pro
- "Explain the mechanism by which CRISPR off-target effects occur and strategies to minimize them" → Sonar Reasoning Pro

**Poor Queries**:
- "Tell me about AI" (too broad)
- "Cancer research" (lacks specificity)
- "Latest news" (too vague)

### 3. Structured Query Format

**Recommended Structure**:
```
[Topic] + [Specific Aspect] + [Time Frame] + [Type of Information]
```

**Examples**:
- "CRISPR gene editing + off-target effects + 2024 + clinical trials"
- "Quantum computing + error correction + recent advances + review papers"
- "Renewable energy + solar efficiency + 2023-2024 + statistical data"

### 4. Follow-up Queries

**Effective Follow-ups**:
- "Show me the full citation for the Smith et al. 2024 paper"
- "What are the limitations of this methodology?"
- "Find similar studies using different approaches"
- "What controversies exist in this research area?"

## Integration with Scientific Writing

This skill enhances scientific writing by providing:

1. **Literature Review Support**: Gather current research for introduction and discussion sections
2. **Methods Validation**: Verify protocols and procedures against current standards
3. **Results Contextualization**: Compare findings with recent similar studies
4. **Discussion Enhancement**: Support arguments with latest evidence
5. **Citation Management**: Provide properly formatted citations in multiple styles

## Error Handling and Limitations

**Known Limitations**:
- Information cutoff: Responses limited to training data (typically 2023-2024)
- Paywall content: May not access full text behind paywalls
- Emerging research: May miss very recent papers not yet indexed
- Specialized databases: Cannot access proprietary or restricted databases

**Error Conditions**:
- API rate limits or quota exceeded
- Network connectivity issues
- Malformed or ambiguous queries
- Model unavailability or maintenance

**Fallback Strategies**:
- Rephrase queries for better clarity
- Break complex queries into simpler components
- Use broader time frames if recent data unavailable
- Cross-reference with multiple query variations

## Usage Examples

### Example 1: Simple Literature Search (Sonar Pro)

**Query**: "Recent advances in transformer attention mechanisms 2024"

**Model Selected**: Sonar Pro (straightforward lookup)

**Response Includes**:
- Summary of 5 key papers from 2024
- Complete citations with DOIs
- Key innovations and improvements
- Performance benchmarks
- Future research directions

### Example 2: Comparative Analysis (Sonar Reasoning Pro)

**Query**: "Compare and contrast the advantages and limitations of transformer-based models versus traditional RNNs for sequence modeling"

**Model Selected**: Sonar Reasoning Pro (complex analysis required)

**Response Includes**:
- Detailed comparison across multiple dimensions
- Analysis of architectural differences
- Trade-offs in computational efficiency vs performance
- Use case recommendations
- Synthesis of evidence from multiple studies
- Discussion of ongoing debates in the field

### Example 3: Method Verification (Sonar Pro)

**Query**: "Standard protocols for flow cytometry analysis"

**Model Selected**: Sonar Pro (protocol lookup)

**Response Includes**:
- Step-by-step protocol from recent review
- Required controls and calibrations
- Common pitfalls and troubleshooting
- Reference to definitive methodology paper
- Alternative approaches with pros/cons

### Example 4: Mechanism Explanation (Sonar Reasoning Pro)

**Query**: "Explain the underlying mechanism of how mRNA vaccines trigger immune responses and why they differ from traditional vaccines"

**Model Selected**: Sonar Reasoning Pro (requires causal reasoning)

**Response Includes**:
- Detailed mechanistic explanation
- Step-by-step biological processes
- Comparative analysis with traditional vaccines
- Molecular-level interactions
- Integration of immunology and pharmacology concepts
- Evidence from recent research

### Example 5: Statistical Data (Sonar Pro)

**Query**: "Global AI adoption in healthcare statistics 2024"

**Model Selected**: Sonar Pro (data lookup)

**Response Includes**:
- Current adoption rates by region
- Market size and growth projections
- Survey methodology and sample size
- Comparison with previous years
- Citations to market research reports

## Performance and Cost Considerations

### Response Times

**Sonar Pro**:
- Typical response time: 5-15 seconds
- Best for rapid information gathering
- Suitable for batch queries

**Sonar Reasoning Pro**:
- Typical response time: 15-45 seconds
- Worth the wait for complex analytical queries
- Provides more thorough reasoning and synthesis

### Cost Optimization

**Automatic Selection Benefits**:
- Saves costs by using Sonar Pro for straightforward queries
- Reserves Sonar Reasoning Pro for queries that truly benefit from deeper analysis
- Optimizes the balance between cost and quality

**Manual Override Use Cases**:
- Force Sonar Pro when budget is constrained and speed is priority
- Force Sonar Reasoning Pro when working on critical research requiring maximum depth
- Use for specific sections of papers (e.g., Pro for methods, Reasoning for discussion)

**Best Practices**:
1. Trust the automatic selection for most use cases
2. Review query results - if Sonar Pro doesn't provide sufficient depth, rephrase with reasoning keywords
3. Use batch queries strategically - combine simple lookups to minimize total query count
4. For literature reviews, start with Sonar Pro for breadth, then use Sonar Reasoning Pro for synthesis

## Security and Ethical Considerations

**Responsible Use**:
- Verify all information against primary sources when possible
- Clearly attribute all data and quotes to original sources
- Avoid presenting AI-generated summaries as original research
- Respect copyright and licensing restrictions
- Use for research assistance, not to bypass paywalls or subscriptions

**Academic Integrity**:
- Always cite original sources, not the AI tool
- Use as a starting point for literature searches
- Follow institutional guidelines for AI tool usage
- Maintain transparency about research methods

## Summary

This skill serves as a powerful research assistant with intelligent dual-model selection:

- **Automatic Intelligence**: Analyzes query complexity and selects the optimal model (Sonar Pro or Sonar Reasoning Pro)
- **Cost-Effective**: Uses faster, cheaper Sonar Pro for straightforward lookups
- **Deep Analysis**: Automatically engages Sonar Reasoning Pro for complex comparative, analytical, and theoretical queries
- **Flexible Control**: Manual override available when you know exactly what level of analysis you need
- **Academic Focus**: Both models configured to prioritize peer-reviewed sources and scholarly literature

Whether you need quick fact-finding or deep analytical synthesis, this skill automatically adapts to deliver the right level of research support for your scientific writing needs.
