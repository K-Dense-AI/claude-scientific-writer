# Scientific-Writing Skill Improvement Plan

> Implementation strategy for audit fixes
> Created: 2025-12-25
> Target: Improve health score from 52% to 85%+

## Executive Summary

The scientific-writing skill audit identified 4 high-priority issues causing a 52% health score. This plan outlines a phased approach to fix these issues while preserving the skill's excellent content quality.

**Key Metrics**:
| Metric | Current | Target |
|--------|---------|--------|
| Health Score | 52% | 85%+ |
| SKILL.md Tokens | ~8,428 | <2,500 |
| Broken References | 10 | 0 |
| Missing Frontmatter | 2 fields | 0 |

---

## Phase 1: Frontmatter Fixes (Quick Wins)

**Estimated effort**: 5 minutes
**Impact**: +8 points (Frontmatter: 12 → 20)

### Step 1.1: Add Version Field

**File**: `skills/scientific-writing/SKILL.md`
**Location**: Lines 1-5 (frontmatter block)

**Action**: Add `version: 1.0.0` to frontmatter

**Before**:
```yaml
---
name: scientific-writing
description: "Core skill for..."
allowed-tools: [Read, Write, Edit, Bash]
---
```

**After**:
```yaml
---
name: scientific-writing
version: 1.0.0
description: "Core skill for..."
allowed-tools: [Read, Write, Edit, Bash]
---
```

### Step 1.2: Improve Description with Trigger Phrases

**File**: `skills/scientific-writing/SKILL.md`
**Location**: Line 3 (description field)

**Action**: Rewrite description to include explicit "Use when..." triggers

**Before** (328 chars):
```yaml
description: "Core skill for the deep research and writing tool. Write scientific manuscripts in full paragraphs (never bullet points). Use two-stage process: (1) create section outlines with key points using research-lookup, (2) convert to flowing prose. IMRAD structure, citations (APA/AMA/Vancouver), figures/tables, reporting guidelines (CONSORT/STROBE/PRISMA), for research papers and journal submissions."
```

**After** (~350 chars):
```yaml
description: "Core scientific manuscript writing skill using IMRAD structure, citations (APA/AMA/Vancouver), and reporting guidelines (CONSORT/STROBE/PRISMA). Use when writing research papers, journal submissions, abstracts, or any scientific document requiring structured prose with proper citations. Integrates with research-lookup for literature and venue-templates for journal-specific formatting."
```

### Step 1.3: Fix Allowed-Tools Format

**File**: `skills/scientific-writing/SKILL.md`
**Location**: Line 4

**Action**: Change array syntax to space-separated format

**Before**:
```yaml
allowed-tools: [Read, Write, Edit, Bash]
```

**After**:
```yaml
allowed-tools: Read, Write, Edit, Bash
```

### Validation (Phase 1)

Run validation script after changes:
```bash
uv run python ~/.claude/skills/skill-reviewer/scripts/validate_frontmatter.py "skills/scientific-writing/SKILL.md"
```

**Expected**: No frontmatter-related errors

---

## Phase 2: Fix Broken References (Critical)

**Estimated effort**: 15 minutes
**Impact**: +5 points (File Structure: 3 → 8), removes 10 HIGH severity issues

### Step 2.1: Fix Script Path References

The skill references scripts that belong to OTHER skills. These need to be rewritten as skill invocations.

**File**: `skills/scientific-writing/SKILL.md`

#### Location A: Lines 67-69 (Graphical Abstract section)

**Before**:
```markdown
**Generate the graphical abstract FIRST:**
```bash
python scripts/generate_schematic.py "Graphical abstract for [paper title]: [brief description showing workflow from input → methods → key findings → conclusions]" -o figures/graphical_abstract.png
```
```

**After**:
```markdown
**Generate the graphical abstract FIRST:**

Use the `scientific-schematics` skill with a prompt describing your graphical abstract:
> "Graphical abstract for [paper title]: workflow showing input → methods → key findings → conclusions"

The skill will generate and save the image to your figures/ directory.
```

#### Location B: Lines 97-99 (Additional Figures section)

**Before**:
```markdown
**Use scientific-schematics EXTENSIVELY for technical diagrams:**
```bash
python scripts/generate_schematic.py "your diagram description" -o figures/output.png
```
```

**After**:
```markdown
**Use the `scientific-schematics` skill for technical diagrams:**

Invoke the skill with a description of your needed diagram. Suitable for:
```

#### Location C: Lines 113-115 (generate-image section)

**Before**:
```markdown
**Use generate-image EXTENSIVELY for visual content:**
```bash
python scripts/generate_image.py "your image description" -o figures/output.png
```
```

**After**:
```markdown
**Use the `generate-image` skill for visual content:**

Invoke the skill with a description of your needed image. Suitable for:
```

### Step 2.2: Fix Venue-Templates Cross-References

**File**: `skills/scientific-writing/SKILL.md`
**Location**: Lines 639-656 (Integration section)

**Before**:
```markdown
The venue-templates skill provides:
- `venue_writing_styles.md`: Master style comparison
- Venue-specific guides: `nature_science_style.md`, `cell_press_style.md`, `medical_journal_styles.md`, `ml_conference_style.md`, `cs_conference_style.md`
- `reviewer_expectations.md`: What reviewers look for at each venue
- Writing examples in `assets/examples/`
```

**After**:
```markdown
**Consult the `venue-templates` skill** for venue-specific resources. That skill provides:
- Master style comparison across venues
- Venue-specific writing guides (Nature/Science, Cell Press, medical journals, ML/CS conferences)
- Reviewer expectation documentation
- Writing examples organized by venue type

Note: These resources are in the venue-templates skill directory, not this skill.
```

### Validation (Phase 2)

Run validation script:
```bash
uv run python ~/.claude/skills/skill-reviewer/scripts/validate_frontmatter.py "skills/scientific-writing/SKILL.md"
```

**Expected**: No "Referenced file does not exist" errors

---

## Phase 3: Token Reduction (Major Refactor)

**Estimated effort**: 30-45 minutes
**Impact**: +16 points (Context Efficiency: 4 → 16, Determinism: 15 → 19)

**Strategy**: Extract 3 large sections to new reference files, keeping summaries in SKILL.md.

### Step 3.1: Create Field Terminology Reference

**New file**: `skills/scientific-writing/references/field_terminology.md`

**Action**:
1. Copy lines 449-538 from SKILL.md (Section 9: Field-Specific Language)
2. Create new reference file with this content
3. Replace in SKILL.md with summary + reference pointer

**New file content structure**:
```markdown
# Field-Specific Language and Terminology

> Reference guide for discipline-specific writing conventions
> Load this file when adapting writing for specific scientific fields

## Overview

[Keep the intro paragraph about adapting language]

## Biomedical and Clinical Sciences
[Full content from lines 461-466]

## Molecular Biology and Genetics
[Full content from lines 468-474]

## Chemistry and Pharmaceutical Sciences
[Full content from lines 476-482]

## Ecology and Environmental Sciences
[Full content from lines 484-489]

## Physics and Engineering
[Full content from lines 491-496]

## Neuroscience
[Full content from lines 498-503]

## Social and Behavioral Sciences
[Full content from lines 505-510]

## General Principles
[Full content from lines 512-538]
```

**SKILL.md replacement** (lines 449-538 become ~15 lines):
```markdown
### 9. Field-Specific Language and Terminology

Adapt language, terminology, and conventions to match the target scientific discipline. Each field has established vocabulary, preferred phrasings, and domain-specific conventions.

**Key principles**:
- Match audience expertise level (specialized vs. broad-impact journals)
- Define technical terms strategically (at first use, appropriate for audience)
- Maintain terminology consistency throughout the manuscript
- Avoid field-mixing errors (don't import terms incorrectly from adjacent fields)

For detailed discipline-specific guides covering Biomedical, Chemistry, Ecology, Physics, Neuroscience, and Social Sciences, see `references/field_terminology.md`.
```

**Token savings**: ~900 tokens

### Step 3.2: Create Writing Process Reference

**New file**: `skills/scientific-writing/references/writing_process.md`

**Action**:
1. Copy lines 332-439 from SKILL.md (Section 7: Writing Process)
2. Create new reference file with this content
3. Replace in SKILL.md with summary + reference pointer

**New file content structure**:
```markdown
# Writing Process: From Outline to Full Paragraphs

> Detailed guide for the two-stage scientific writing process
> Load this file when drafting manuscript sections

## Critical Rule

Always write in full paragraphs, never submit bullet points in scientific papers.

## Stage 1: Create Section Outlines
[Full content from lines 339-360]

## Stage 2: Convert to Full Paragraphs
[Full content from lines 362-393]

## Key Differences: Outlines vs Final Text
[Table from lines 395-403]

## Common Mistakes to Avoid
[Content from lines 405-420]

## When Lists ARE Acceptable
[Content from lines 414-425]

## Integration with Research Lookup
[Content from lines 427-439]
```

**SKILL.md replacement** (lines 332-439 become ~20 lines):
```markdown
### 7. Writing Process: From Outline to Full Paragraphs

**CRITICAL: Always write in full paragraphs, never submit bullet points in scientific papers.**

Use the two-stage writing process:

**Stage 1: Create Section Outlines**
- Use research-lookup to gather relevant literature
- Create structured outlines with bullet points marking main arguments, key studies, data points
- These bullets are scaffolding, NOT the final manuscript

**Stage 2: Convert to Full Paragraphs**
- Transform bullet points into complete sentences
- Add transitions between ideas (however, moreover, subsequently)
- Integrate citations naturally within sentences
- Ensure logical flow from sentence to sentence

For detailed examples, the outline-to-prose conversion guide, common mistakes, and when lists are acceptable, see `references/writing_process.md`.
```

**Token savings**: ~1,200 tokens

### Step 3.3: Reduce Visual Enhancement Section

**File**: `skills/scientific-writing/SKILL.md`
**Location**: Lines 49-139 (Visual Enhancement section)

**Action**: This section duplicates content from scientific-schematics and generate-image skills. Reduce to essential cross-references.

**Before**: ~90 lines of detailed figure requirements and instructions

**After** (~25 lines):
```markdown
## Visual Enhancement with Scientific Schematics

**Every scientific paper should include visual elements.** Use the `scientific-schematics` and `generate-image` skills to create figures.

### Minimum Figure Requirements

| Document Type | Minimum | Recommended |
|--------------|---------|-------------|
| Research Papers | 5 | 6-8 |
| Literature Reviews | 4 | 5-7 |
| Posters | 6 | 8-10 |

### Figure Types by Skill

**Use `scientific-schematics` for**:
- Graphical abstracts (required for every paper)
- Study design flowcharts (CONSORT, PRISMA, STROBE)
- Conceptual frameworks and methodology diagrams
- Biological pathways, system architectures

**Use `generate-image` for**:
- Photorealistic illustrations
- Medical/anatomical visualizations
- Cover images and infographics

For detailed figure creation instructions, consult the respective skill documentation.
```

**Token savings**: ~800 tokens

### Step 3.4: Verify Token Count

After all extractions, verify new token count:
```bash
wc -w skills/scientific-writing/SKILL.md
# Multiply by 1.3 for approximate tokens
# Target: < 2500 tokens (< 1900 words)
```

### Validation (Phase 3)

1. Run validation script:
```bash
uv run python ~/.claude/skills/skill-reviewer/scripts/validate_frontmatter.py "skills/scientific-writing/SKILL.md"
```

2. Verify new reference files exist:
```bash
ls -la skills/scientific-writing/references/
```

3. Check all internal references resolve:
```bash
grep -o 'references/[a-z_]*\.md' skills/scientific-writing/SKILL.md | sort -u | while read f; do
  [ -f "skills/scientific-writing/$f" ] && echo "OK: $f" || echo "MISSING: $f"
done
```

---

## Phase 4: Final Validation & Documentation

**Estimated effort**: 10 minutes
**Impact**: Confirms improvements, updates changelog

### Step 4.1: Run Full Validation

```bash
uv run python ~/.claude/skills/skill-reviewer/scripts/validate_frontmatter.py "skills/scientific-writing/SKILL.md"
```

**Expected output**:
- Health Score: 85%+
- Star Rating: 4/5 or higher
- Critical issues: 0
- High issues: 0

### Step 4.2: Manual Review Checklist

- [ ] SKILL.md loads correctly (read first 50 lines, verify structure)
- [ ] All 7 reference files exist and are non-empty
- [ ] Cross-skill references are clearly marked as external
- [ ] No orphaned content (nothing accidentally deleted)
- [ ] Frontmatter parses correctly

### Step 4.3: Update CHANGELOG.md

Add entry to CHANGELOG.md:
```markdown
## [Unreleased]

### Changed
- **scientific-writing skill**: Refactored for token efficiency (8428 → ~2400 tokens)
  - Added version field (1.0.0) and improved description triggers
  - Fixed cross-skill references to venue-templates, scientific-schematics, generate-image
  - Extracted field terminology guide to `references/field_terminology.md`
  - Extracted writing process guide to `references/writing_process.md`
  - Reduced visual enhancement section (delegates to other skills)
  - Health score improved from 52% to 85%+
```

### Step 4.4: Commit Changes

```bash
git add skills/scientific-writing/
git commit -m "refactor: improve scientific-writing skill health score (52% → 85%+)

- Add version field and improve description with trigger phrases
- Fix broken script references (now reference skills properly)
- Extract field_terminology.md and writing_process.md to references/
- Reduce token count from ~8428 to ~2400 tokens
- Clarify cross-skill references to venue-templates

Addresses audit findings from skill-reviewer analysis.

Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Implementation Order Summary

| Phase | Steps | Time | Cumulative Score |
|-------|-------|------|------------------|
| 1. Frontmatter | 1.1, 1.2, 1.3 | 5 min | 60% |
| 2. References | 2.1, 2.2 | 15 min | 70% |
| 3. Token Reduction | 3.1, 3.2, 3.3, 3.4 | 30-45 min | 85%+ |
| 4. Validation | 4.1, 4.2, 4.3, 4.4 | 10 min | Final |

**Total estimated time**: 60-75 minutes

---

## Files to Create

| File | Content Source | Estimated Size |
|------|----------------|----------------|
| `references/field_terminology.md` | SKILL.md lines 449-538 | ~3KB |
| `references/writing_process.md` | SKILL.md lines 332-439 | ~4KB |

## Files to Modify

| File | Changes |
|------|---------|
| `SKILL.md` | Frontmatter fixes, section extractions, reference fixes |
| `CHANGELOG.md` | Add refactor entry |

---

## Rollback Plan

If issues arise after implementation:

1. **Git reset** (before commit):
   ```bash
   git checkout -- skills/scientific-writing/
   ```

2. **Git revert** (after commit):
   ```bash
   git revert HEAD
   ```

3. **Manual restore**: Original content preserved in this plan document's "Before" sections.

---

## Success Criteria

- [ ] Health score >= 85%
- [ ] Zero critical or high severity issues
- [ ] SKILL.md < 2,500 tokens
- [ ] All reference files exist and are properly linked
- [ ] Validation script passes with no errors
- [ ] Skill functionality unchanged (content preserved, just reorganized)
