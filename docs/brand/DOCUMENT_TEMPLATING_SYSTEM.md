# Document Templating System Design

**Status:** Design Phase
**Created:** December 19, 2025
**Project:** Oligon Branded PDF Generation

---

## 1. Problem Statement

### The Challenge

Converting varied markdown documents to professionally branded PDFs requires:
1. **Intelligent parsing** - Understanding document structure from markdown
2. **Component mapping** - Translating markdown elements to visual components
3. **Determinism** - Consistent, predictable output regardless of input variation

### Why This Is Hard

The same markdown syntax can have different semantic meanings:
- A table could be "results", "methods", or "comparison"
- A blockquote could be "warning", "info", or emphasis
- Numbered lists could be "findings", "steps", or "questions"

Pure heuristic parsing leads to inconsistent results.

### The Solution

**Template-driven parsing**: Define markdown templates for each document type. Authors use templates, parser knows what to expect, output is deterministic.

```
Template → Author in Markdown → Parse (deterministic) → Branded PDF
```

---

## 2. Design Decisions

### 2.1 Input Format: Markdown

**Decision:** All input documents will be authored in Markdown format.

**Rationale:**
- Already the primary authoring format in this workflow
- Human-readable and version-controllable
- Widely supported by editors and tools
- Can embed semantic hints without breaking rendering

### 2.2 Template Contract System

**Decision:** Each document type has a defined template that specifies:
- Required and optional sections
- Expected content patterns within sections
- Component mappings for PDF generation

**Rationale:**
- Makes parsing deterministic (parser knows what to expect)
- Provides authoring guidance (templates are fill-in-the-blank)
- Enables validation (can check document against template)

### 2.3 Semantic Hints via HTML Comments

**Decision:** Use HTML comments for optional semantic markers that don't affect markdown rendering.

```markdown
<!-- @section: methods -->
## 2. Methods

<!-- @callout: warning -->
> **Important:** This is critical context...

<!-- @table: ranking -->
| Rank | Model | Score |
```

**Rationale:**
- Valid markdown (renders normally in any viewer)
- Invisible in rendered output
- Provides explicit hints where structure is ambiguous
- Optional - templates reduce need for hints

### 2.4 Confirmation Step

**Decision:** Before generating PDF, show detected structure and allow adjustment.

**Rationale:**
- Catches parsing errors before generation
- Gives user control over edge cases
- Builds trust in the system

---

## 3. Document Category Taxonomy

Based on analysis of markdown document patterns across projects, documents fall into **4 major categories** with **12 distinct types**:

### 3.1 Category Overview

| Category | Types | Primary Use |
|----------|-------|-------------|
| **Scientific Documents** | 3 | Research workflows, analysis, and results |
| **Project Management** | 3 | Status tracking, meetings, and coordination |
| **Development Documents** | 4 | Specifications, tasks, and engineering standards |
| **Reference Documents** | 2 | Entry points and method guides |

### 3.2 Document Type Matrix

| Type | Category | Avg Lines | Key Characteristics |
|------|----------|-----------|---------------------|
| `analysis-report` | Scientific | 400-800 | Objective → Methods → Results → Discussion; optional PASS/FAIL assessment mode |
| `phase-plan` | Scientific | 300-500 | Hypotheses, metrics, acceptance criteria |
| `data-report` | Scientific | 100-650 | Metrics, rankings, recommendations; supports auto-generation |
| `project-status` | Project Mgmt | 100-200 | Progress, blockers, milestones |
| `meeting-notes` | Project Mgmt | 50-150 | Agenda, decisions, action items |
| `literature-review` | Project Mgmt | 200-400 | Paper summaries, synthesis |
| `technical-spec` | Development | 500-1050 | Goal → Scope → Requirements → Design |
| `task-list` | Development | 150-920 | Checkbox format, phases, dependencies |
| `standards-guide` | Development | 100-400 | Conventions, code examples, DO/DON'T |
| `agent-definition` | Development | 50-320 | YAML frontmatter, role, workflow |
| `readme` | Reference | 50-450 | Overview, quick start, architecture |
| `method-guide` | Reference | 200-600 | Tool-specific usage, examples, caveats |

**Consolidation Notes:**
- `analysis-report` absorbs former `phase-results` via `assessment: pass-fail` frontmatter option
- `data-report` consolidates former `data-summary` and `generated-report` types; use `generated: true` for auto-generated reports

### 3.3 Category Selection Guide

```
Is this document about scientific research or analysis?
├── YES: Is it planning future work or reporting past work?
│   ├── Planning → phase-plan
│   └── Reporting → Is it narrative analysis or data-driven metrics?
│       ├── Narrative (methods, discussion) → analysis-report
│       └── Data-driven (rankings, scores) → data-report
└── NO: Is it about project coordination?
    ├── YES: meeting-notes, project-status, or literature-review
    └── NO: Is it about software development?
        ├── YES: technical-spec, task-list, standards-guide, or agent-definition
        └── NO: readme or method-guide
```

---

## 4. Document Type Templates

### Category A: Scientific Documents

#### 4.1 Analysis Report

**Use Case:** Phase-style analysis documents with objective, methods, results, discussion. Supports optional PASS/FAIL assessment mode for phase results.

**Template Structure:**
```markdown
---
type: analysis-report
title: [Report Title]
date: [Date]
project: [Project Name]
phase: [Phase Number] (optional)
focus: [Analysis Focus]
assessment: none | pass-fail  # Optional: enables PASS/FAIL status tables
---

## 1. Objective

[Problem statement and goals]

### Key Questions

1. [Question 1]
2. [Question 2]

### Critical Context

> **[Context Type]:** [Important framing or caveats]

---

## 2. Methods

### 2.1 [Method Category]

| Parameter | Value | Description |
|-----------|-------|-------------|
| ... | ... | ... |

### 2.2 [Procedure Name]

**What:** [Brief description]
**Why:** [Rationale]
**How:**
```[language]
[code or commands]
```

---

## 3. Results: [Subject Name]

### 3.1 What We Did
[Description]

### 3.2 Why
[Rationale]

### 3.3 How
```[language]
[commands/code]
```

### 3.4 Results

| Metric | Value | Result |
|--------|-------|--------|
| ... | ... | ✓/✗ |

### 3.5 Interpretation
[Analysis of results]

---

## 4. Summary

### 4.1 Consolidated Results

| Model | Metric 1 | Metric 2 | Overall |
|-------|----------|----------|---------|
| ... | ... | ... | ... |

### 4.2 Key Findings

#### Finding 1: [Title]
[Description]

#### Finding 2: [Title]
[Description]

---

## 5. Discussion

### 5.1 [Discussion Topic]
[Analysis and interpretation]

### 5.2 Implications

| Capability | Validated? | Evidence |
|------------|------------|----------|
| ... | ... | ... |

### 5.3 Limitations
1. [Limitation 1]
2. [Limitation 2]

---

## 6. Recommendations

### 6.1 [Recommendation Category]

- [ ] [Action item 1]
- [ ] [Action item 2]

### 6.2 Next Steps

| Step | Action | Priority |
|------|--------|----------|
| 1 | ... | High/Medium/Low |

---

## 7. Files and Outputs

| File | Location | Description |
|------|----------|-------------|
| ... | ... | ... |

---

*[Document Title]*
*Version [X.Y] | [Date]*
```

**Component Mappings:**
| Template Element | PDF Component |
|-----------------|---------------|
| YAML frontmatter | Cover page metadata |
| `## N. Title` | Section divider |
| `> **Type:**` blockquotes | Callout box |
| `#### Finding N:` | Finding card (highlighted) |
| Tables with ✓/✗ or ✅/❌ | Status table (color-coded) |
| `- [ ]` checklists | Checklist component |
| Code blocks | Method code block |
| PASS/FAIL summary tables | Status badge row (when `assessment: pass-fail`) |
| Rankings table | Ranked list with medals/badges |

---

#### 4.2 Data Report

**Use Case:** Data-driven reports with metrics, rankings, and recommendations. Consolidates former `data-summary` and `generated-report` types.

**Template Structure:**
```markdown
---
type: data-report
title: [Report Title]
date: [Date]
subject: [Target/Gene/Entity] (optional)
total_records: [N]
generated: true | false  # true for auto-generated reports
pipeline_version: [Version] (if generated)
---

# [Report Title]

**Subject:** [subject]
**Generated:** [timestamp]
**Total Records:** [count]

---

## Navigation (optional, for longer reports)

| Section | Description |
|---------|-------------|
| [Executive Summary](#executive-summary) | Key findings overview |
| [Results](#results) | Detailed data tables |
| [Recommendations](#recommendations) | Actionable guidance |

---

## Executive Summary

**Status:** [STATUS INDICATOR]

| Metric | Value | Interpretation |
|--------|-------|----------------|
| ... | ... | ... |

---

## 1. Overview

[Context and purpose]

### Objectives Analyzed

| # | Objective | Goal | Description |
|---|-----------|------|-------------|
| 1 | ... | Maximize/Minimize | ... |

---

## 2. Results Summary

### 2.1 [Category Name]

| ID | Metric 1 | Metric 2 | Score | Tier |
|----|----------|----------|-------|------|
| ... | ... | ... | ... | ... |

### 2.2 Quality Assessment

<!-- @callout: warning/info/success -->
> **[Assessment]:** [Interpretation and implications]

---

## 3. Detailed Analysis

### 3.1 [Analysis Category]

| Metric | Group A | Group B | Delta |
|--------|---------|---------|-------|
| ... | ... | ... | ... |

### 3.2 Pattern Analysis

[Description of patterns observed]

---

## 4. Recommendations

### 4.1 [Use Case 1]

| Rank | ID | Key Metric | Recommendation |
|------|----|------------|----------------|
| 1 | [ID] | [Value] | [Guidance] |
| 2 | ... | ... | ... |

### 4.2 [Use Case 2]

[Guidance text]

---

## 5. Technical Details

| Parameter | Value |
|-----------|-------|
| Input File | ... |
| Algorithm | ... |
| Version | ... |

---

*[Report Title]*
*Generated: [Timestamp]*
```

**Component Mappings:**
| Template Element | PDF Component |
|-----------------|---------------|
| Navigation table | Clickable TOC (for longer reports) |
| Status indicator | Status badge (colored) |
| Executive Summary metrics | Metric card row |
| Tier/Score tables | Graded table (color bands) |
| Embedded images | Figure with caption |
| Recommendations | Recommendation cards |
| Technical details | Compact metadata table |
| Pipeline metadata | Footer metadata |

---

#### 4.3 Phase Plan

**Use Case:** Scientific workflow planning with hypotheses, metrics, and acceptance criteria.

**Examples:** `Phase1_PSMA_Protein_Fidelity_Analysis_Plan.md`, `Phase2_Aptamer_Structure_Fidelity_Analysis_Plan.md`

**Template Structure:**
```markdown
---
type: phase-plan
project: [Project Name]
phase: [Phase Number]
title: [Phase Title]
version: [X.Y]
status: Draft/Approved/In Progress/Complete
date: [Date]
---

## Executive Summary

[1-2 paragraph overview of what this phase will accomplish]

---

## 1. Key Questions / Hypotheses

| # | Question | Hypothesis | Test Approach |
|---|----------|------------|---------------|
| 1 | [Question] | [Hypothesis] | [How to test] |
| 2 | ... | ... | ... |

---

## 2. Structures Under Analysis

### 2.1 Reference Structures

| Structure | Source | Resolution | Purpose |
|-----------|--------|------------|---------|
| [Name] | [PDB/File] | [Å] | [Role in analysis] |

### 2.2 Predicted/Test Structures

| Model | Method | Date Generated | Notes |
|-------|--------|----------------|-------|
| [Name] | [Tool] | [Date] | [Context] |

---

## 3. Analysis Framework

### 3.1 [Analysis Category]

**Objective:** [What this analysis measures]

**Method:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Tools:**
```bash
[commands or scripts]
```

### 3.2 [Analysis Category]

[Repeat structure]

---

## 4. Metrics & Acceptance Criteria

| Metric | Threshold | Pass Condition | Rationale |
|--------|-----------|----------------|-----------|
| [Metric 1] | [Value] | [Condition] | [Why this threshold] |
| [Metric 2] | ... | ... | ... |

---

## 5. Output Directory Structure

```
[project]/
├── [phase]/
│   ├── data/
│   │   └── [data files]
│   ├── results/
│   │   └── [output files]
│   └── figures/
│       └── [visualizations]
```

---

## 6. Dependencies

### 6.1 Prior Phase Dependencies

| Dependency | Source Phase | Required Output |
|------------|--------------|-----------------|
| [Item] | Phase [N] | [What's needed] |

### 6.2 External Dependencies

- [Tool/data requirement 1]
- [Tool/data requirement 2]

---

## 7. Timeline

| Milestone | Target Date | Status |
|-----------|-------------|--------|
| Setup complete | [Date] | ⬜/🔄/✅ |
| Analysis complete | [Date] | ⬜/🔄/✅ |
| Report drafted | [Date] | ⬜/🔄/✅ |

---

*[Phase Title]*
*Version [X.Y] | [Date]*
```

**Component Mappings:**
| Template Element | PDF Component |
|-----------------|---------------|
| Executive Summary | Highlighted summary box |
| Questions/Hypotheses table | Numbered question cards |
| Metrics table | Threshold table with indicators |
| Directory structure | Code block with tree styling |
| Timeline | Timeline component with status |

---

### Category B: Project Management Documents

#### 4.4 Literature Review

**Use Case:** Paper summaries, comparisons, and synthesis.

**Template Structure:**
```markdown
---
type: literature-review
title: [Review Title]
topic: [Topic Area]
date: [Date]
papers_reviewed: [N]
---

## 1. Scope

[What this review covers]

### Research Questions

1. [Question 1]
2. [Question 2]

### Search Strategy

| Database | Query | Results |
|----------|-------|---------|
| ... | ... | ... |

---

## 2. Paper Summaries

### 2.1 [Author et al., Year]

**Title:** [Full title]
**Journal:** [Journal name]
**DOI:** [DOI]

#### Key Findings

- [Finding 1]
- [Finding 2]

#### Methods

[Brief methods description]

#### Relevance

> [How this relates to your work]

---

### 2.2 [Author et al., Year]

[Same structure repeats]

---

## 3. Comparative Analysis

### 3.1 Methods Comparison

| Paper | Method | Sample Size | Key Difference |
|-------|--------|-------------|----------------|
| ... | ... | ... | ... |

### 3.2 Results Comparison

| Finding | Paper A | Paper B | Paper C |
|---------|---------|---------|---------|
| ... | ... | ... | ... |

---

## 4. Synthesis

### 4.1 Consensus Findings

[What papers agree on]

### 4.2 Contradictions

[Where papers disagree]

### 4.3 Gaps

[What remains unknown]

---

## 5. Implications for Current Work

[How this informs your research]

---

## 6. References

1. [Full citation 1]
2. [Full citation 2]

---

*[Review Title]*
*[Date]*
```

---

#### 4.5 Meeting Notes

**Template Structure:**
```markdown
---
type: meeting-notes
title: [Meeting Title]
date: [Date]
attendees: [List]
facilitator: [Name]
---

## Agenda

1. [Topic 1]
2. [Topic 2]
3. [Topic 3]

---

## Discussion

### [Topic 1]

[Discussion summary]

**Decision:** [If applicable]

### [Topic 2]

[Discussion summary]

---

## Decisions

| Decision | Owner | Date |
|----------|-------|------|
| ... | ... | ... |

---

## Action Items

| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| ... | ... | ... | ⬜/🔄/✅ |

---

## Next Meeting

**Date:** [Date]
**Topics:**
- [ ] [Topic 1]
- [ ] [Topic 2]

---

*[Meeting Title]*
*[Date]*
```

---

#### 4.6 Project Status

**Template Structure:**
```markdown
---
type: project-status
title: [Project Name] Status Update
date: [Date]
period: [Week/Sprint/Month]
overall_status: On Track/At Risk/Blocked
---

## Summary

[Brief status overview]

| Metric | Value |
|--------|-------|
| Completion | X% |
| On Track | Y/Z tasks |
| Blocked | N items |

---

## Progress This Period

### Completed

- [x] [Task 1]
- [x] [Task 2]

### In Progress

- [ ] [Task 1] - [Status/Notes]
- [ ] [Task 2] - [Status/Notes]

---

## Milestones

| Milestone | Target Date | Status |
|-----------|-------------|--------|
| ... | ... | ✅/🔄/⬜ |

---

## Blockers

### [Blocker 1]

**Impact:** [Description]
**Owner:** [Name]
**Resolution:** [Plan]

---

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| ... | High/Med/Low | High/Med/Low | ... |

---

## Next Period

| Priority | Task | Owner |
|----------|------|-------|
| 1 | ... | ... |
| 2 | ... | ... |

---

*[Project Name] Status*
*Period: [Date Range]*
```

---

### Category C: Development Documents

#### 4.7 Technical Specification

**Template Structure:**
```markdown
---
type: technical-spec
title: [Feature/System Name]
version: [X.Y]
date: [Date]
author: [Name]
status: Draft/Review/Approved
---

## 1. Overview

[What this specification covers]

### Goals

- [Goal 1]
- [Goal 2]

### Non-Goals

- [Non-goal 1]

---

## 2. Background

[Context and motivation]

### Current State

[How things work now]

### Problem

[What needs to change]

---

## 3. Requirements

### 3.1 Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1 | ... | Must/Should/Could |
| FR-2 | ... | ... |

### 3.2 Non-Functional Requirements

| ID | Requirement | Metric |
|----|-------------|--------|
| NFR-1 | Performance | < X ms |
| NFR-2 | Availability | 99.X% |

---

## 4. Design

### 4.1 Architecture

[Architecture description]

```
[ASCII diagram or description]
```

### 4.2 Components

| Component | Responsibility |
|-----------|----------------|
| ... | ... |

### 4.3 Interfaces

| Interface | Input | Output |
|-----------|-------|--------|
| ... | ... | ... |

---

## 5. Implementation

### 5.1 Approach

[Implementation strategy]

### 5.2 Dependencies

| Dependency | Version | Purpose |
|------------|---------|---------|
| ... | ... | ... |

### 5.3 Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| ... | ... | ... |

---

## 6. Testing

### 6.1 Test Cases

| ID | Scenario | Expected Result |
|----|----------|-----------------|
| TC-1 | ... | ... |

### 6.2 Acceptance Criteria

- [ ] [Criterion 1]
- [ ] [Criterion 2]

---

## 7. Rollout

### 7.1 Phases

| Phase | Scope | Timeline |
|-------|-------|----------|
| 1 | ... | ... |

### 7.2 Rollback Plan

[How to revert if needed]

---

## 8. Open Questions

- [ ] [Question 1]
- [ ] [Question 2]

---

*[Specification Title]*
*Version [X.Y] | [Date]*
*Status: [Draft/Review/Approved]*
```

---

#### 4.8 Task List

**Use Case:** Checkbox-based task tracking with phases, dependencies, and acceptance criteria.

**Examples:** `tasks.md` files in spec directories

**Template Structure:**
```markdown
---
type: task-list
title: Task List: [Feature Name]
spec: [Related Spec]
date: [Date]
status: Not Started/In Progress/Complete
---

## Overview

**Total Tasks:** [N] phases with [M] task groups

| Phase | Task Groups | Description | Status |
|-------|-------------|-------------|--------|
| Phase 1 | [N] | [Description] | ⏳/🔄/✅ |
| Phase 2 | [N] | [Description] | ⏳ |

**Performance Targets:**
- Phase 1: [target metric] ✅/🔴/⏳
- Phase 2: [target metric]

---

## Execution Sequence

**Completed:**
- ✅ Task Groups [X-Y]: [Summary]

**Current Task:**
- 🔄 Task Group [Z]: [Description]

**Remaining:**
```
Task Group [A]
├── Subtask 1
├── Subtask 2
└── Subtask 3
```

---

## Task List

### Phase [N]: [Name] ([time estimate])

#### Task Group [X]: [Name]

**Dependencies:** [None / Task Group Y]
**Goal:** [What this task group accomplishes]

- [ ] [X.0] Complete [main task]
  - [ ] [X.1] [Subtask 1]
  - [ ] [X.2] [Subtask 2]
  - [x] [X.3] [Completed subtask]

**Acceptance Criteria:**
- [Measurable criterion 1]
- [Measurable criterion 2]

---

#### Task Group [Y]: [Name]

[Repeat structure]

---

## Completion Summary

| Task Group | Status | Notes |
|------------|--------|-------|
| [X] | ✅ Complete | [Summary] |
| [Y] | 🔄 In Progress | [Current state] |

---

*[Task List Title]*
*Last Updated: [Date]*
```

**Component Mappings:**
| Template Element | PDF Component |
|-----------------|---------------|
| Overview table | Summary metrics box |
| Execution sequence tree | Progress tree diagram |
| Checkbox items | Styled checklist with status |
| Dependencies | Dependency badge |
| Acceptance criteria | Criteria checklist |

---

#### 4.9 Standards Guide

**Use Case:** Coding conventions, best practices, and DO/DON'T patterns.

**Examples:** `agent-os/standards/backend/api.md`, `coding-style.md`

**Template Structure:**
```markdown
---
type: standards-guide
title: [Domain] Standards
category: backend/frontend/global/testing
version: [X.Y]
last_updated: [Date]
---

## Overview

[Brief statement of what these standards govern]

---

## 1. [Category Name]

### 1.1 [Standard/Principle]

**Rule:** [Clear, actionable statement]

**Rationale:** [Why this matters]

**Examples:**

```python
# ✅ Good
[correct pattern]

# ❌ Bad
[anti-pattern]
```

### 1.2 [Standard/Principle]

[Repeat structure]

---

## 2. [Category Name]

### Conventions Table

| Type | Convention | Example |
|------|------------|---------|
| [Type 1] | [Rule] | [Example] |
| [Type 2] | ... | ... |

---

## 3. Common Patterns

### 3.1 [Pattern Name]

**When to use:** [Context]

**Implementation:**

```python
[code example]
```

**Variations:**
- [Variation 1]: [When to use]
- [Variation 2]: [When to use]

---

## 4. Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| [Name] | [Why it's bad] | [Better approach] |

---

## 5. Exceptions

| Exception | When Allowed | Approval |
|-----------|--------------|----------|
| [Exception] | [Specific context] | [Who approves] |

---

## References

- [Link to related standard]
- [External reference]

---

*[Domain] Standards*
*Version [X.Y] | [Date]*
```

**Component Mappings:**
| Template Element | PDF Component |
|-----------------|---------------|
| ✅/❌ code blocks | Side-by-side comparison boxes |
| Conventions table | Styled reference table |
| Anti-patterns | Warning-styled callout |
| Exceptions | Exception note box |

---

#### 4.10 Agent Definition

**Use Case:** AI agent role definitions with capabilities and workflows.

**Examples:** `.claude/agents/agent-os/implementer.md`

**Template Structure:**
```markdown
---
type: agent-definition
name: [agent-name]
description: [One-line description]
tools: [Tool1, Tool2, ...]
color: [color]
model: inherit/sonnet/opus
---

# [Agent Name]

## Role

[Detailed description of what this agent does and when to use it]

---

## Core Responsibilities

1. [Responsibility 1]
2. [Responsibility 2]
3. [Responsibility 3]

---

## Workflow

### Step 1: [Action]

[Detailed instructions]

**Commands:**
```bash
[example commands]
```

### Step 2: [Action]

[Instructions]

**Output Format:**
```
[expected output structure]
```

### Step 3: [Action]

[Instructions]

---

## Input Requirements

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| [Input 1] | [Type] | Yes/No | [What it is] |
| [Input 2] | ... | ... | ... |

---

## Output Deliverables

| Output | Format | Description |
|--------|--------|-------------|
| [Output 1] | [Format] | [What it contains] |
| [Output 2] | ... | ... |

---

## Important Constraints

- **MUST:** [Required behavior]
- **MUST NOT:** [Prohibited behavior]
- **SHOULD:** [Recommended behavior]

---

## Integration Points

| Integrates With | Purpose |
|-----------------|---------|
| [Agent/Command] | [How they work together] |

---

## User Standards Compliance

[Reference to standards files this agent follows]

---

*[Agent Name]*
*Version [X.Y]*
```

**Component Mappings:**
| Template Element | PDF Component |
|-----------------|---------------|
| YAML frontmatter | Agent header card |
| Core Responsibilities | Numbered capability list |
| Workflow steps | Process flow diagram |
| Constraints | Constraint callout boxes |

---

### Category D: Reference Documents

#### 4.11 README

**Use Case:** Project entry point with overview, setup, and architecture.

**Template Structure:**
```markdown
---
type: readme
project: [Project Name]
version: [X.Y]
last_updated: [Date]
---

# [Project Name]

[One-line description]

---

## Overview

[2-3 sentence explanation of what this project does]

**Key Technologies:**
- [Technology 1]
- [Technology 2]

---

## Quick Start

### Prerequisites

- [Requirement 1]
- [Requirement 2]

### Installation

```bash
[installation commands]
```

### First Use

```bash
[example commands]
```

---

## Architecture

```
[project]/
├── [dir1]/
│   └── [description]
├── [dir2]/
│   └── [description]
└── [file]
```

---

## Usage

### [Command/Feature 1]

```bash
[command example]
```

[Description]

### [Command/Feature 2]

[Description]

---

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| [Param 1] | [Value] | [What it does] |

---

## Contributing

[Guidelines for contributors]

---

## License

[License information]

---

*[Project Name]*
*Version [X.Y] | [Date]*
```

**Component Mappings:**
| Template Element | PDF Component |
|-----------------|---------------|
| Project title | Cover page |
| Quick Start | Highlighted quick-reference box |
| Architecture tree | Directory diagram |
| Configuration table | Reference table |

---

#### 4.12 Method Guide

**Use Case:** Tool-specific documentation with usage, examples, and caveats.

**Examples:** `Boltz2 Notes.md`, `ViennaRNA_Migration_Analysis.md`

**Template Structure:**
```markdown
---
type: method-guide
title: [Tool/Method Name]
category: [Category]
version: [Tool Version]
last_updated: [Date]
tags: [tag1, tag2]
---

# [Tool/Method Name]

## Quick Summary

[2-3 sentence TL;DR of what this tool does and when to use it]

---

## 1. Installation

### Requirements

- [Requirement 1]
- [Requirement 2]

### Setup

```bash
[installation commands]
```

### Verification

```bash
[verification command]
# Expected output: [expected]
```

---

## 2. Basic Usage

### [Use Case 1]

**Purpose:** [What this accomplishes]

**Command:**
```bash
[command]
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| [--param1] | [type] | [description] |

**Example:**
```bash
[example with real values]
```

### [Use Case 2]

[Repeat structure]

---

## 3. Advanced Usage

### [Advanced Feature]

[Description and examples]

---

## 4. Comparison with Alternatives

| Feature | [This Tool] | [Alternative 1] | [Alternative 2] |
|---------|-------------|-----------------|-----------------|
| [Feature 1] | ✅ | ❌ | ✅ |
| [Feature 2] | ... | ... | ... |

---

## 5. Caveats & Limitations

> **Warning:** [Important limitation to be aware of]

### Known Issues

| Issue | Workaround |
|-------|------------|
| [Issue 1] | [How to handle] |

### Edge Cases

- [Edge case 1]: [How to handle]
- [Edge case 2]: [How to handle]

---

## 6. Troubleshooting

### [Problem 1]

**Symptom:** [What you see]

**Cause:** [Why it happens]

**Solution:**
```bash
[fix commands]
```

---

## 7. References

1. [Official documentation](URL)
2. [Paper/publication](DOI)
3. [Related resource](URL)

---

*[Tool/Method Name] Guide*
*Tool Version [X.Y] | Guide Updated [Date]*
```

**Component Mappings:**
| Template Element | PDF Component |
|-----------------|---------------|
| Quick Summary | Highlight box |
| Comparison table | Feature matrix |
| Warning blockquotes | Warning callout |
| Troubleshooting sections | Problem/solution cards |

---

## 5. Implementation Strategy

### 5.1 Access Method Options

| Option | Pros | Cons | Recommendation |
|--------|------|------|----------------|
| **Claude Skill** | Rich context, multi-step workflow, can ask questions | Requires skill infrastructure | **Primary** |
| **Slash Command** | Quick invocation, simple interface | Limited interactivity | Secondary (for simple cases) |
| **Embedded in Existing Skill** | Leverages existing PDF skill | Couples concerns | Not recommended |
| **Python CLI** | Direct, scriptable | No AI assistance in parsing | Utility tool |

### 5.2 Recommended Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Workflow                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. /new-doc <type>     → Creates markdown from template    │
│  2. Author document     → User fills in template            │
│  3. /doc-to-pdf <file>  → Converts to branded PDF           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│               markdown-to-pdf Skill                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Phase 1: Template Detection                                 │
│  ├── Read YAML frontmatter (type: analysis-report)          │
│  ├── Load corresponding template schema                      │
│  └── Validate document structure                             │
│                                                              │
│  Phase 2: Structure Parsing                                  │
│  ├── Parse sections according to template                    │
│  ├── Detect semantic elements (callouts, tables, findings)   │
│  └── Build document tree                                     │
│                                                              │
│  Phase 3: Confirmation (Interactive)                         │
│  ├── Show detected structure to user                         │
│  ├── Allow adjustments                                       │
│  └── Confirm before generation                               │
│                                                              │
│  Phase 4: PDF Generation                                     │
│  ├── Map elements to Oligon components                       │
│  ├── Apply brand styling                                     │
│  └── Generate PDF via ReportGenerator                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 5.3 Skill Design

**Skill Name:** `markdown-to-pdf` (or `branded-doc`)

**Triggers:**
- `/doc-to-pdf <filepath>` - Convert existing markdown to PDF
- `/new-doc <type>` - Create new document from template
- `/list-templates` - Show available document templates

**Workflow:**

```
User: /doc-to-pdf Phase3_Analysis.md

Skill:
1. Read file
2. Detect type from frontmatter (or ask if missing)
3. Parse structure using template schema
4. Display:

   "Detected Structure:
   ├── Type: analysis-report
   ├── Sections: 15
   │   ├── 1. Objective (with 2 callouts)
   │   ├── 2. Methods (4 tables, 2 code blocks)
   │   ├── 3-7. Results (5 subsections, 12 tables)
   │   ├── 8. Summary (2 finding cards)
   │   └── ...
   └── Output: Phase3_Analysis.pdf

   Proceed? [Y/adjust/cancel]"

5. Generate PDF with Oligon branding
6. Return file path
```

### 5.4 Component Implementation

The skill will use the existing `oligon_reports` package, extended with:

```python
# New components needed
class FindingCard(Flowable):
    """Highlighted finding box with number badge"""

class StatusTable(Table):
    """Table with ✓/✗ color coding"""

class GradedTable(Table):
    """Table with grade-based color bands"""

class MethodBlock(Flowable):
    """What/Why/How structured block"""

class MetadataHeader(Flowable):
    """Document header with key-value pairs"""

# Template-aware parser
class TemplateParser:
    """Parse markdown according to template schema"""

    def __init__(self, template_type: str):
        self.schema = load_template_schema(template_type)

    def parse(self, markdown: str) -> DocumentTree:
        """Parse markdown into structured document tree"""

    def validate(self) -> list[ValidationError]:
        """Check document against template requirements"""

# Document tree to PDF converter
class DocumentConverter:
    """Convert parsed document tree to PDF"""

    def convert(self, tree: DocumentTree, output: str) -> Path:
        """Generate branded PDF from document tree"""
```

---

## 6. File Organization

```
template_project/
├── src/
│   └── oligon_reports/
│       ├── __init__.py
│       ├── brand_colors.py      # Existing
│       ├── components.py        # Existing + new components
│       ├── report_generator.py  # Existing
│       ├── templates/           # NEW
│       │   ├── __init__.py
│       │   ├── schemas/         # Template schemas (YAML)
│       │   │   ├── # Category A: Scientific Documents (3)
│       │   │   ├── analysis-report.yaml
│       │   │   ├── phase-plan.yaml
│       │   │   ├── data-report.yaml
│       │   │   ├── # Category B: Project Management (3)
│       │   │   ├── literature-review.yaml
│       │   │   ├── meeting-notes.yaml
│       │   │   ├── project-status.yaml
│       │   │   ├── # Category C: Development Documents (4)
│       │   │   ├── technical-spec.yaml
│       │   │   ├── task-list.yaml
│       │   │   ├── standards-guide.yaml
│       │   │   ├── agent-definition.yaml
│       │   │   ├── # Category D: Reference Documents (2)
│       │   │   ├── readme.yaml
│       │   │   └── method-guide.yaml
│       │   ├── markdown/        # Markdown templates
│       │   │   ├── analysis-report.md
│       │   │   ├── phase-plan.md
│       │   │   ├── data-report.md
│       │   │   ├── literature-review.md
│       │   │   ├── meeting-notes.md
│       │   │   ├── project-status.md
│       │   │   ├── technical-spec.md
│       │   │   ├── task-list.md
│       │   │   ├── standards-guide.md
│       │   │   ├── agent-definition.md
│       │   │   ├── readme.md
│       │   │   └── method-guide.md
│       │   └── parser.py        # Template-aware parser
│       └── converter.py         # Document tree to PDF
├── .claude/
│   └── skills/
│       └── markdown-to-pdf/
│           └── SKILL.md         # Skill definition
├── templates/                   # User-facing template copies
│   ├── scientific/
│   │   ├── analysis-report.md
│   │   ├── phase-plan.md
│   │   └── data-report.md
│   ├── project-management/
│   │   ├── literature-review.md
│   │   ├── meeting-notes.md
│   │   └── project-status.md
│   ├── development/
│   │   ├── technical-spec.md
│   │   ├── task-list.md
│   │   ├── standards-guide.md
│   │   └── agent-definition.md
│   └── reference/
│       ├── readme.md
│       └── method-guide.md
└── DOCUMENT_TEMPLATING_SYSTEM.md  # This file
```

---

## 7. Implementation Phases

### Phase 1: Foundation (Current Sprint)

- [x] Design document (this file)
- [x] Define document category taxonomy (4 categories, 12 types)
- [ ] Define template schemas for all 12 types
- [ ] Create markdown template files
- [ ] Extend components.py with new components

### Phase 2: Parser

- [ ] Implement TemplateParser class
- [ ] YAML frontmatter detection
- [ ] Section parsing according to schema
- [ ] Semantic element detection (callouts, findings, etc.)
- [ ] Validation against template requirements

### Phase 3: Converter

- [ ] Implement DocumentConverter class
- [ ] Map all template elements to PDF components
- [ ] Handle edge cases and fallbacks
- [ ] Test with existing documents (Phase3, Pareto)

### Phase 4: Skill Integration

- [ ] Create markdown-to-pdf skill
- [ ] Implement /doc-to-pdf command
- [ ] Implement /new-doc command
- [ ] Add confirmation workflow
- [ ] Test end-to-end

### Phase 5: Polish

- [ ] Error handling and user-friendly messages
- [ ] Template customization options
- [ ] Documentation
- [ ] Example outputs

---

## 8. Open Questions

1. **Template inheritance**: Should templates support inheritance (e.g., all templates share common footer)?

2. **Custom templates**: Should users be able to define their own templates?

3. **Partial documents**: How to handle documents that don't fill all template sections?

4. **Multiple outputs**: Should one markdown generate multiple PDFs (e.g., full report + executive summary)?

5. **Version tracking**: How to handle template version changes over time?

---

## 9. Success Criteria

1. **Determinism**: Same input always produces same output
2. **Fidelity**: PDF accurately represents markdown content
3. **Efficiency**: Conversion takes < 5 seconds for typical documents
4. **Flexibility**: Handles 90%+ of typical documents without manual adjustment
5. **Usability**: User can convert a document in < 3 interactions

---

*Document Templating System Design*
*Version 2.1 | December 21, 2025*
*Updated: Consolidated from 15 to 12 document types (merged phase-results→analysis-report, data-summary+generated-report→data-report, removed experiment-plan)*
