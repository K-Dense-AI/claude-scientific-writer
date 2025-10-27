---
name: research-lookup
description: "Look up current research information using Perplexity's Sonar Pro model through OpenRouter. Search academic papers, recent studies, technical documentation, and general research information with citations."
---

# Research Information Lookup

## Overview

This skill enables real-time research information lookup using Perplexity's Sonar Pro model through OpenRouter. It provides access to current academic literature, recent studies, technical documentation, and general research information with proper citations and source attribution.

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

## Technical Integration

### OpenRouter API Configuration

This skill integrates with OpenRouter (openrouter.ai) to access Perplexity's Sonar Pro model:

**Model Specifications**:
- **Model**: `perplexity/sonar-pro-online` (online search enabled)
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

### 1. Specific and Focused Queries

**Good Queries**:
- "Randomized controlled trials of mRNA vaccines for cancer treatment 2023-2024"
- "Machine learning applications in medical diagnosis systematic review"
- "Climate change impacts on agricultural productivity meta-analysis"

**Poor Queries**:
- "Tell me about AI" (too broad)
- "Cancer research" (lacks specificity)
- "Latest news" (too vague)

### 2. Structured Query Format

**Recommended Structure**:
```
[Topic] + [Specific Aspect] + [Time Frame] + [Type of Information]
```

**Examples**:
- "CRISPR gene editing + off-target effects + 2024 + clinical trials"
- "Quantum computing + error correction + recent advances + review papers"
- "Renewable energy + solar efficiency + 2023-2024 + statistical data"

### 3. Follow-up Queries

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

### Example 1: Literature Search for Manuscript

**Query**: "Recent advances in transformer attention mechanisms 2024"

**Response Includes**:
- Summary of 5 key papers from 2024
- Complete citations with DOIs
- Key innovations and improvements
- Performance benchmarks
- Future research directions

### Example 2: Method Verification

**Query**: "Standard protocols for flow cytometry analysis"

**Response Includes**:
- Step-by-step protocol from recent review
- Required controls and calibrations
- Common pitfalls and troubleshooting
- Reference to definitive methodology paper
- Alternative approaches with pros/cons

### Example 3: Statistical Data

**Query**: "Global AI adoption in healthcare statistics 2024"

**Response Includes**:
- Current adoption rates by region
- Market size and growth projections
- Survey methodology and sample size
- Comparison with previous years
- Citations to market research reports

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

This skill serves as a powerful research assistant, enabling comprehensive literature reviews and current information gathering to support high-quality scientific writing.
