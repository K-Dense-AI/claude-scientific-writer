# Integration Analysis: Template-Project + Claude Scientific Writer

**Date:** December 23, 2025
**Purpose:** Cross-reference analysis of DOCUMENT_TEMPLATING_SYSTEM.md design with the claude-scientific-writer skill system to inform synthesis strategy.

---

## Executive Summary

The template-project design and the scientific-writer system share significant conceptual overlap but differ in implementation approach. The scientific-writer has a **mature skill architecture** with rich integrations, while the template-project has a **more rigorous type system** and template-driven parsing. The optimal path is to **merge the templating discipline into the scientific-writer's infrastructure**.

---

## 1. Document Type Mapping

| Template-Project (12 types) | Scientific-Writer Skill | Gap Analysis |
|----------------------------------|------------------------|--------------|
| `analysis-report` | `scientific-writing` | ✅ Strong overlap (IMRAD structure) |
| `phase-plan` | — | ⚠️ Needs dedicated skill |
| `data-report` | — | ⚠️ Needs dedicated skill |
| `literature-review` | `literature-review` | ✅ Direct match |
| `meeting-notes` | — | ❌ Missing |
| `project-status` | — | ❌ Missing |
| `technical-spec` | — | ❌ Missing |
| `task-list` | — | ❌ Missing |
| `standards-guide` | — | ❌ Missing |
| `agent-definition` | — | ❌ Missing |
| `readme` | — | ❌ Missing (exists as separate user skill) |
| `method-guide` | — | ❌ Missing |

### Scientific-Writer Has (Template-Project Lacks)

- `latex-posters`, `pptx-posters` (presentation formats)
- `scientific-slides` (presentation builder)

---

## 2. Architectural Comparison

| Aspect | Template-Project | Scientific-Writer |
|--------|----------------------|-------------------|
| **Parsing** | YAML frontmatter → Schema validation → Deterministic | Ad-hoc, skill-guided, AI-interpreted |
| **Template Storage** | `/templates/markdown/*.md` + `/templates/schemas/*.yaml` | Embedded in SKILL.md prose |
| **Confirmation** | Explicit "show detected structure" step | Implicit (skill decides) |
| **PDF Engine** | `oligon_reports` (ReportLab) | Same + LaTeX, Pandoc |
| **Component Library** | Proposed: FindingCard, StatusTable, etc. | Existing: CalloutBox, MetricCardRow, Timeline |
| **Visual Integration** | Not defined | **Mandatory** scientific-schematics |
| **Research Integration** | Not defined | `research-lookup`, `citation-management` |

---

## 3. What to Adopt from Scientific-Writer

### A. Mandatory Visual Enhancement Pattern

Template-project doesn't specify figure generation. Scientific-writer enforces:

```markdown
**⚠️ MANDATORY: Every document MUST include AI-generated figures**
```

This should be added to the component mappings and workflow.

### B. Two-Stage Writing Process

Scientific-writer's key insight:

```
1. Create section outlines with key points (using research-lookup)
2. Convert outlines into flowing prose
```

This should be integrated into the template workflow.

### C. Cross-Skill Integration

Template-project design is self-contained. Scientific-writer skills call each other:

- `scientific-writing` → `research-lookup` → `citation-management`
- All document skills → `scientific-schematics`

The `/doc-to-pdf` skill should similarly invoke supporting skills.

### D. Existing Python Infrastructure

The `oligon_reports` package already exists in this repo:

- `ReportGenerator` class with branded styling
- `CalloutBox`, `MetricCardRow`, `SectionDivider`, `Timeline`, `FigurePlaceholder` components
- Brand colors and typography defined

---

## 4. What Scientific-Writer Should Adopt from Template-Project

### A. YAML Frontmatter Type Detection

Template-project's approach is more robust:

```yaml
---
type: analysis-report
assessment: pass-fail
---
```

Currently, scientific-writer skills don't have explicit type detection from document metadata.

### B. Template Schema Validation

The proposed `TemplateParser.validate()` with schema-based checking would prevent malformed documents.

### C. Explicit Component Mappings

Template-project's table is clearer than the prose-based descriptions in SKILL.md files:

| Template Element | PDF Component |
|-----------------|---------------|
| `#### Finding N:` | Finding card (highlighted) |
| Tables with ✓/✗ | Status table (color-coded) |
| `- [ ]` checklists | Checklist component |
| Code blocks | Method code block |

### D. Confirmation Step

The "show detected structure and allow adjustment" before PDF generation is a user-safety feature scientific-writer lacks.

### E. Project Management Document Types

`meeting-notes`, `project-status`, `task-list` fill a gap - scientific-writer is research-focused but not project-management-aware.

---

## 5. Recommended Integration Strategy

```
┌─────────────────────────────────────────────────────────────────┐
│                    MERGED ARCHITECTURE                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  TEMPLATE-PROJECT CONTRIBUTIONS:                                 │
│  ├── Template schemas (12 types in YAML)                        │
│  ├── Markdown template files (authoring guides)                 │
│  ├── TemplateParser class (frontmatter detection + validation)  │
│  ├── Confirmation workflow                                       │
│  └── Project management document types                          │
│                                                                  │
│  SCIENTIFIC-WRITER CONTRIBUTIONS:                                │
│  ├── Skill infrastructure (.claude/skills/*)                    │
│  ├── oligon_reports package (ReportGenerator, components)       │
│  ├── Scientific schematics integration                          │
│  ├── Research-lookup & citation-management                      │
│  ├── LaTeX/PPTX/DOCX support                                    │
│  └── Poster specialized skills                                   │
│                                                                  │
│  NEW UNIFIED SKILL: markdown-to-pdf                             │
│  ├── /new-doc <type>     → Create from template                 │
│  ├── /doc-to-pdf <file>  → Convert with confirmation            │
│  └── /list-templates     → Show all 12+ types                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 6. Implementation Phases

### Phase 1: Foundation (Template Infrastructure)

- [ ] Create template schema files in `src/oligon_reports/templates/schemas/`
- [ ] Create markdown template files in `src/oligon_reports/templates/markdown/`
- [ ] Implement `TemplateParser` class with YAML frontmatter detection
- [ ] Add document validation against schemas

### Phase 2: Component Extension

- [ ] Add `FindingCard` component to `components.py`
- [ ] Add `StatusTable` with ✓/✗ color coding
- [ ] Add `GradedTable` with tier-based color bands
- [ ] Add `MethodBlock` (What/Why/How structure)
- [ ] Add `MetadataHeader` for document headers

### Phase 3: Skill Creation

- [ ] Create `markdown-to-pdf` skill in `.claude/skills/markdown-to-pdf/SKILL.md`
- [ ] Implement `/new-doc <type>` command
- [ ] Implement `/doc-to-pdf <file>` command with confirmation
- [ ] Implement `/list-templates` command
- [ ] Integrate with `scientific-schematics` for visual enhancement

### Phase 4: Document Type Expansion

- [ ] Add `meeting-notes` skill/template
- [ ] Add `project-status` skill/template
- [ ] Add `task-list` skill/template
- [ ] Add `technical-spec` skill/template
- [ ] Add `standards-guide` skill/template
- [ ] Add `agent-definition` skill/template

### Phase 5: Integration & Polish

- [ ] Cross-skill integration testing
- [ ] Error handling and user-friendly messages
- [ ] Documentation updates
- [ ] Example outputs for each document type

---

## 7. File Organization (Target State)

```
claude-scientific-writer_fork/
├── src/
│   └── oligon_reports/
│       ├── __init__.py
│       ├── brand_colors.py          # Existing
│       ├── components.py            # Existing + new components
│       ├── report_generator.py      # Existing
│       ├── templates/               # NEW
│       │   ├── __init__.py
│       │   ├── schemas/             # YAML validation schemas
│       │   │   ├── analysis-report.yaml
│       │   │   ├── phase-plan.yaml
│       │   │   ├── data-report.yaml
│       │   │   ├── literature-review.yaml
│       │   │   ├── meeting-notes.yaml
│       │   │   ├── project-status.yaml
│       │   │   ├── technical-spec.yaml
│       │   │   ├── task-list.yaml
│       │   │   ├── standards-guide.yaml
│       │   │   ├── agent-definition.yaml
│       │   │   ├── readme.yaml
│       │   │   └── method-guide.yaml
│       │   ├── markdown/            # Authoring templates
│       │   │   └── [same 12 files as .md]
│       │   └── parser.py            # TemplateParser class
│       └── converter.py             # DocumentConverter class
├── .claude/
│   └── skills/
│       ├── markdown-to-pdf/         # NEW unified skill
│       │   └── SKILL.md
│       ├── scientific-writing/      # Existing
│       ├── document-skills/         # Existing (pdf, docx, pptx)
│       └── [other existing skills]
├── templates/                       # User-facing template copies
│   ├── scientific/
│   ├── project-management/
│   ├── development/
│   └── reference/
├── docs/
│   └── template-project/
│       └── brand/
│           └── DOCUMENT_TEMPLATING_SYSTEM.md  # Original design doc
└── INTEGRATION_ANALYSIS.md          # This file
```

---

## 8. Success Criteria

1. **Determinism**: Same markdown input always produces same PDF output
2. **Fidelity**: PDF accurately represents markdown content with brand styling
3. **Efficiency**: Conversion takes < 5 seconds for typical documents
4. **Flexibility**: Handles 90%+ of documents without manual adjustment
5. **Usability**: User can convert a document in < 3 interactions
6. **Integration**: Seamless invocation of research-lookup, scientific-schematics

---

## 9. Key Decisions Required

1. **Template inheritance**: Should templates support inheritance (e.g., shared footer)?
2. **Custom templates**: Should users be able to define their own templates?
3. **Partial documents**: How to handle documents that don't fill all template sections?
4. **Multiple outputs**: Should one markdown generate multiple PDFs (full + executive summary)?
5. **Version tracking**: How to handle template version changes over time?

---

## 10. Completed: Clinical/Business Skill Removal

Prior to implementing the merged architecture, a scope reduction was performed to remove clinical and business-focused skills that are not aligned with the core scientific research writing focus of this fork.

### Skills Removed

| Skill | Rationale |
|-------|-----------|
| `research-grants` | Grant writing outside core scope |
| `clinical-decision-support` | Clinical healthcare focus |
| `clinical-reports` | Clinical healthcare focus |
| `market-research-reports` | Business/market analysis focus |
| `treatment-plans` | Clinical healthcare focus |

### Execution Phases

**Phase 1: Directory Removal**
- Deleted 15 skill directories across 3 locations:
  - `.claude/skills/` (5 skills)
  - `skills/` (5 duplicate copies)
  - `scientific_writer/.claude/skills/` (5 nested duplicates)

**Phase 2: Cross-Skill Reference Updates**
- `venue-templates/SKILL.md`: Removed "Research Grants" subsection referencing `research-grants` skill
- `hypothesis-generation/assets/FORMATTING_GUIDE.md`: Removed `treatment-plans` skill reference
- Applied to both `.claude/skills/` and `skills/` directories

**Phase 3: Main Documentation Updates**
- `.claude/WRITER.md` and `scientific_writer/.claude/WRITER.md`: Removed 4 rows from "Special Document Types" table and 3 rows from "MINIMUM Figure Requirements" table
- `INTEGRATION_ANALYSIS.md`: Updated Section 1 (removed skill mappings) and Section 5 (simplified architecture diagram)
- `docs/original/*.md`: Added fork customization notices to archived documentation

**Phase 4: Verification Cleanup**
- `commands/scientific-writer-init.md`: Updated skill count from 22 to 17, removed clinical/grant examples
- `templates/CLAUDE.scientific-writer.md`: Removed ~245 lines of clinical-decision-support and market-research-reports content
- `venue-templates/SKILL.md`: Refactored to standalone grant template guidance (no cross-skill dependency)

### Resulting Skill Count

The fork now contains **17 active skills** focused on core scientific writing capabilities:
- Literature review and scientific writing
- LaTeX and PPTX poster generation
- Scientific slides and presentations
- Citation management and research lookup
- Scientific schematics and image generation
- Hypothesis generation and peer review
- Paper-to-web conversion tools

### Documentation Reference

Full execution details preserved in:
- `SKILL_REMOVAL_PLAN.md` (now deleted, content archived in CHANGELOG.md)
- `CHANGELOG.md` ([Unreleased] section)

---

## References

- **Template-Project Design**: `docs/template-project/brand/DOCUMENT_TEMPLATING_SYSTEM.md`
- **Scientific-Writer Skills**: `.claude/skills/*/SKILL.md`
- **Oligon Reports Package**: `src/oligon_reports/`
- **Brand Standards**: `docs/template-project/brand/BRAND_COLORS_v4.md`

---

*Integration Analysis*
*Version 1.0 | December 23, 2025*
