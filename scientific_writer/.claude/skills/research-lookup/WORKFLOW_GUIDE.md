# Parallel Research Workflow - Visual Guide

## 🎯 Overview

This guide shows the complete parallel research workflow with visual diagrams.

## 📊 Workflow Diagrams

### Traditional Sequential Workflow (Before)

```
Input Text
    ↓
Manual Topic Extraction (slow)
    ↓
Query 1 → API → Wait → Result 1
    ↓
Query 2 → API → Wait → Result 2
    ↓
Query 3 → API → Wait → Result 3
    ↓
...
    ↓
Manual Compilation
    ↓
Results

⏱️  Total Time: N × ~12 seconds per query
```

### New Parallel Workflow (After)

```
Input Text
    ↓
AI Topic Identification (fast, automatic)
    ↓
topics.txt (reviewable, editable)
    ↓
┌─────────────────────────────────────┐
│     Parallel Execution Engine       │
├─────────────────────────────────────┤
│ Query 1 → API ──┐                  │
│ Query 2 → API ──┤                  │
│ Query 3 → API ──┼→ Results (JSON)  │
│ Query 4 → API ──┤                  │
│ Query N → API ──┘                  │
└─────────────────────────────────────┘
    ↓
results.json (structured, complete)

⏱️  Total Time: ~15-20 seconds (regardless of N, up to worker limit)
```

## 🚀 Three Usage Patterns

### Pattern 1: Quick & Automated (One Command)

**Use Case:** You have text and want results ASAP

```
┌─────────────────────────────────────────────────────────────┐
│  python research_lookup.py --identify input.txt             │
│         --topics-file topics.txt                            │
│         --parallel --max-workers 10                         │
│         --output results.json                               │
└─────────────────────────────────────────────────────────────┘
                            ↓
        ┌───────────────────────────────────────┐
        │  Automatic Workflow                   │
        │  1. Identify topics (AI)              │
        │  2. Save to topics.txt                │
        │  3. Research in parallel (10 workers) │
        │  4. Export to results.json            │
        └───────────────────────────────────────┘
                            ↓
        ✅ Complete results in < 1 minute
```

**When to use:**
- ✅ Quick research needed
- ✅ Trust AI topic identification
- ✅ Don't need to review topics

### Pattern 2: Review & Refine (Two Steps)

**Use Case:** You want to review/edit topics before research

```
STEP 1: Identify Topics
┌─────────────────────────────────────────────────────────────┐
│  python research_lookup.py --identify input.txt             │
│         --topics-file topics.txt                            │
└─────────────────────────────────────────────────────────────┘
                            ↓
                    topics.txt created
                            ↓
            👤 HUMAN REVIEW & EDIT 👤
            (add, remove, refine topics)
                            ↓
STEP 2: Research in Parallel
┌─────────────────────────────────────────────────────────────┐
│  python research_lookup.py --topics-file topics.txt         │
│         --parallel --max-workers 10                         │
│         --output results.json                               │
└─────────────────────────────────────────────────────────────┘
                            ↓
        ✅ Refined results in < 1 minute
```

**When to use:**
- ✅ Want to ensure topic quality
- ✅ Need to add/remove topics
- ✅ Iterative refinement

### Pattern 3: Programmatic (Python API)

**Use Case:** Integration into larger pipeline

```python
from research_lookup import ResearchLookup

# Initialize
research = ResearchLookup()

# Option A: Complete automation
result = research.identify_and_research(
    text=your_text,
    topics_file="topics.txt",
    parallel=True,
    max_workers=10,
    output_file="results.json"
)

# Option B: Step-by-step control
topics = research.identify_research_topics(text, "topics.txt")
# ... process topics ...
results = research.parallel_lookup(topics, max_workers=10)
# ... process results ...
```

**When to use:**
- ✅ Part of automated pipeline
- ✅ Need programmatic control
- ✅ Custom processing needed

## 🎛️ Worker Configuration

```
Workers: 1    2    3    4    5    6    7    8    9    10
         ↓    ↓    ↓    ↓    ↓    ↓    ↓    ↓    ↓    ↓
Time:   100%  50%  35%  28%  22%  18%  16%  14%  13%  12%

Recommendation: 5-10 workers for best balance
- Too few (1-3): Not much speedup
- Optimal (5-10): Great speedup, no rate limits
- Too many (15+): May hit API rate limits
```

## 📈 Performance by Use Case

### Literature Review (10-20 queries)

**Sequential:**
```
[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓] 100% | ~3-4 minutes
```

**Parallel (10 workers):**
```
[▓▓▓▓] 100% | ~30 seconds
```

**Time Saved:** 2.5-3.5 minutes (83% faster)

### Grant Application (5-10 queries)

**Sequential:**
```
[▓▓▓▓▓▓▓▓▓▓] 100% | ~1-2 minutes
```

**Parallel (5 workers):**
```
[▓▓] 100% | ~15-20 seconds
```

**Time Saved:** 45-100 seconds (75-83% faster)

### Manuscript Citations (20-50 queries)

**Sequential:**
```
[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓] 100% | ~5-10 minutes
```

**Parallel (10 workers):**
```
[▓▓▓▓▓] 100% | ~1-1.5 minutes
```

**Time Saved:** 4-8.5 minutes (80-90% faster)

## 🎨 Real-World Example

### Scenario: Research Proposal

**Input Text (proposal.txt):**
```
We propose investigating CRISPR-Cas9 for treating sickle cell disease.
Research areas include: clinical trials, delivery methods, off-target
effects, comparison with traditional treatments, and regulatory approval.
```

**Step 1: Identify Topics**
```bash
$ python research_lookup.py --identify proposal.txt --topics-file topics.txt

[Research] Identifying research topics...
[Research] Identified 5 research topics
[Research] Saved 5 topics to topics.txt
```

**Generated topics.txt:**
```
1. CRISPR-Cas9 clinical trials for sickle cell disease
2. Delivery methods for CRISPR in hematopoietic stem cells
3. Off-target effects of CRISPR-Cas9 gene editing
4. Comparison of CRISPR vs bone marrow transplantation for sickle cell
5. Regulatory approval pathways for CRISPR therapeutics
```

**Step 2: Review & Edit**
```bash
# Open topics.txt and refine (optional)
# Add: "6. Cost-effectiveness of CRISPR therapy"
```

**Step 3: Parallel Research**
```bash
$ python research_lookup.py --topics-file topics.txt --parallel --max-workers 5 --output results.json

[Research] Loaded 6 topics from topics.txt
[Research] Starting parallel lookup for 6 queries with 5 workers...
[Research] ✓ Completed 1/6: CRISPR-Cas9 clinical trials for sickle cell...
[Research] ✓ Completed 2/6: Delivery methods for CRISPR in hematopoiet...
[Research] ✓ Completed 3/6: Off-target effects of CRISPR-Cas9 gene edi...
[Research] ✓ Completed 4/6: Comparison of CRISPR vs bone marrow transpl...
[Research] ✓ Completed 5/6: Regulatory approval pathways for CRISPR the...
[Research] ✓ Completed 6/6: Cost-effectiveness of CRISPR therapy...
[Research] Parallel lookup complete. 6/6 successful

SUMMARY: 6/6 queries completed successfully
```

**Total Time:** ~18 seconds (vs ~72 seconds sequential)

**Output (results.json):**
```json
{
  "timestamp": "2024-11-17 10:30:15",
  "total_topics": 6,
  "successful_queries": 6,
  "topics": [...],
  "results": [
    {
      "success": true,
      "query": "CRISPR-Cas9 clinical trials for sickle cell disease",
      "response": "...",
      "citations": [...],
      "model": "perplexity/sonar-pro"
    },
    ...
  ]
}
```

## 🔄 Iterative Refinement

```
Round 1: Initial Research
    ↓
Review Results
    ↓
Identify Gaps
    ↓
Add New Topics to topics.txt
    ↓
Round 2: Targeted Research
    ↓
Review Results
    ↓
Round 3: Deep Dive
    (use --force-model reasoning for analysis)
```

## 💡 Pro Tips

### 1. Start Broad, Then Narrow
```
Round 1: 5 broad topics (Sonar Pro)
  ↓ Identify gaps
Round 2: 3 specific topics (Sonar Reasoning Pro for analysis)
```

### 2. Use Topic Files as Templates
```bash
# Create template for recurring research
cp topics.txt templates/weekly_literature_review.txt

# Modify and run weekly
python research_lookup.py --topics-file templates/weekly_literature_review.txt --parallel
```

### 3. Combine with Scripts
```bash
# Daily automated research
#!/bin/bash
DATE=$(date +%Y%m%d)
python research_lookup.py \
  --topics-file recurring_topics.txt \
  --parallel --max-workers 10 \
  --output "results_${DATE}.json"
```

## 📚 Best Practices Summary

| Queries | Workers | Pattern      | Time Savings |
|---------|---------|--------------|--------------|
| 1-2     | 1       | Sequential   | None         |
| 3-5     | 3-5     | Parallel     | 3-4x faster  |
| 6-10    | 5-8     | Parallel     | 5-6x faster  |
| 11-20   | 8-10    | Parallel     | 6-7x faster  |
| 21+     | 10      | Parallel     | 7-8x faster  |

## 🎯 Decision Tree

```
Do you have 5+ research questions?
    ↓
   Yes → Use parallel workflow
    ↓
Do you have input text or manual topics?
    ↓
Input text → Use --identify
    ↓
Need to review topics?
    ↓
   Yes → Two-step workflow (identify, review, research)
   No  → One-step workflow (identify_and_research)
    ↓
Manual topics → Use --topics-file directly
    ↓
Run parallel research with 5-10 workers
    ↓
✅ Results in < 1 minute
```

## 🚀 Quick Reference

```bash
# Fastest (one command)
python research_lookup.py --identify input.txt --topics-file topics.txt --parallel --output results.json

# Most control (two commands)
python research_lookup.py --identify input.txt --topics-file topics.txt
# ... edit topics.txt ...
python research_lookup.py --topics-file topics.txt --parallel --output results.json

# From existing topics
python research_lookup.py --topics-file my_topics.txt --parallel

# Python API (complete automation)
result = research.identify_and_research(text, parallel=True, max_workers=10)
```

---

**Ready to get started?** Pick a pattern above and try it with your research!

