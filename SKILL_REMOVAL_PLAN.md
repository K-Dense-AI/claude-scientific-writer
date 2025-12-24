# Skill Removal Plan

**Date:** December 23, 2025
**Purpose:** Remove 5 clinical/business-focused skills from the claude-scientific-writer fork to streamline the skill set for scientific research use cases.

---

## Skills to Remove

1. `research-grants`
2. `clinical-decision-support`
3. `clinical-reports`
4. `market-research-reports`
5. `treatment-plans`

---

## Inventory Summary

| Location | Count | Description |
|----------|-------|-------------|
| `.claude/skills/<skill>/` | 5 directories | Primary skill definitions |
| `skills/<skill>/` | 5 directories | Duplicate skill directories |
| `scientific_writer/.claude/skills/<skill>/` | 5 directories | Nested duplicate skills |
| Cross-skill references | 3 files | Skills referencing removed skills |
| Main documentation | 6 files | Docs mentioning these skills |

**Total directories to remove:** 15
**Total files requiring edits:** 9

---

## Step-by-Step Removal Plan

### Phase 1: Remove Skill Directories

#### Step 1.1: Remove primary skill folders (`.claude/skills/`)

```bash
rm -rf .claude/skills/research-grants
rm -rf .claude/skills/clinical-decision-support
rm -rf .claude/skills/clinical-reports
rm -rf .claude/skills/market-research-reports
rm -rf .claude/skills/treatment-plans
```

**Files affected per skill:**
- `SKILL.md` - Main skill definition
- `README.md` - Skill documentation
- `references/` - Reference materials (multiple .md files)
- `assets/` - Templates and guides
- `scripts/` - Python utilities (treatment-plans only)

#### Step 1.2: Remove duplicate skill folders (`skills/`)

```bash
rm -rf skills/research-grants
rm -rf skills/clinical-decision-support
rm -rf skills/clinical-reports
rm -rf skills/market-research-reports
rm -rf skills/treatment-plans
```

#### Step 1.3: Remove nested duplicate folders (`scientific_writer/.claude/skills/`)

```bash
rm -rf scientific_writer/.claude/skills/research-grants
rm -rf scientific_writer/.claude/skills/clinical-decision-support
rm -rf scientific_writer/.claude/skills/clinical-reports
rm -rf scientific_writer/.claude/skills/market-research-reports
rm -rf scientific_writer/.claude/skills/treatment-plans
```

---

### Phase 2: Update Cross-Skill References

These files reference one or more of the removed skills and need edits:

#### Step 2.1: Update `venue-templates` skill

**File:** `.claude/skills/venue-templates/SKILL.md`
**Reference:** Mentions `research-grants` in related skills section
**Action:** Remove reference to `research-grants` from the related skills list

**File:** `skills/venue-templates/SKILL.md`
**Action:** Same edit as above (duplicate file)

#### Step 2.2: Update `hypothesis-generation` skill

**File:** `.claude/skills/hypothesis-generation/assets/FORMATTING_GUIDE.md`
**Reference:** Mentions `treatment-plans` as an example
**Action:** Remove or replace the `treatment-plans` reference

**File:** `skills/hypothesis-generation/assets/FORMATTING_GUIDE.md`
**Action:** Same edit as above (duplicate file)

---

### Phase 3: Update Main Documentation

#### Step 3.1: Update `.claude/WRITER.md`

**Location:** Lines 76-84 (approximate)
**Section:** "Special Document Types" table
**Action:** Remove these rows from the table:

| Skill | What it removes |
|-------|-----------------|
| `treatment-plans` | Row for treatment plan generation |
| `clinical-reports` | Row for clinical report writing |
| `clinical-decision-support` | Row for CDS documents |
| `research-grants` | Row for grant proposals |
| `market-research-reports` | Row for market analysis |

#### Step 3.2: Update `scientific_writer/.claude/WRITER.md`

**Action:** Same edits as Step 3.1 (duplicate file)

#### Step 3.3: Update `INTEGRATION_ANALYSIS.md`

**Location:** Root of repository
**Sections to update:**

1. **Section 1 (Document Type Mapping, lines 16-36):**
   - Remove row for `research-grants` → `clinical-decision-support` mapping
   - Update "Scientific-Writer Has" list to remove:
     - `treatment-plans, clinical-reports (specialized clinical)`
     - `market-research-reports (business analysis)`

2. **Section 5 (Recommended Integration Strategy, line 156):**
   - Remove `Clinical/grant/poster specialized skills` or update to just `poster specialized skills`

#### Step 3.4: Update `docs/original/SKILLS.md`

**Action:** Remove sections documenting these 5 skills, OR add a note that these skills have been removed in the fork

#### Step 3.5: Update `docs/original/README.md`

**Action:** Remove or annotate references to the 5 removed skills

#### Step 3.6: Update `docs/original/DOCUMENTATION_INDEX.md`

**Action:** Remove entries for the 5 removed skills

#### Step 3.7: Update `docs/original/DEVELOPMENT.md`

**Action:** Remove references to the 5 removed skills

---

### Phase 4: Verification

#### Step 4.1: Verify no remaining references

```bash
# Search for any remaining references
grep -r "research-grants" --include="*.md" .
grep -r "clinical-decision-support" --include="*.md" .
grep -r "clinical-reports" --include="*.md" .
grep -r "market-research-reports" --include="*.md" .
grep -r "treatment-plans" --include="*.md" .
```

#### Step 4.2: Verify skill directories removed

```bash
# Should return nothing
find . -type d -name "research-grants"
find . -type d -name "clinical-decision-support"
find . -type d -name "clinical-reports"
find . -type d -name "market-research-reports"
find . -type d -name "treatment-plans"
```

#### Step 4.3: Test remaining skills load correctly

```bash
# Verify .claude/skills/ structure is intact
ls -la .claude/skills/
```

---



## Files Affected Summary

### Directories to Delete (15 total)

```
.claude/skills/research-grants/
.claude/skills/clinical-decision-support/
.claude/skills/clinical-reports/
.claude/skills/market-research-reports/
.claude/skills/treatment-plans/

skills/research-grants/
skills/clinical-decision-support/
skills/clinical-reports/
skills/market-research-reports/
skills/treatment-plans/

scientific_writer/.claude/skills/research-grants/
scientific_writer/.claude/skills/clinical-decision-support/
scientific_writer/.claude/skills/clinical-reports/
scientific_writer/.claude/skills/market-research-reports/
scientific_writer/.claude/skills/treatment-plans/
```

### Files to Edit (9 total)

| File | Edit Type |
|------|-----------|
| `.claude/skills/venue-templates/SKILL.md` | Remove `research-grants` reference |
| `skills/venue-templates/SKILL.md` | Remove `research-grants` reference |
| `.claude/skills/hypothesis-generation/assets/FORMATTING_GUIDE.md` | Remove `treatment-plans` reference |
| `skills/hypothesis-generation/assets/FORMATTING_GUIDE.md` | Remove `treatment-plans` reference |
| `.claude/WRITER.md` | Remove 5 rows from Special Document Types table |
| `scientific_writer/.claude/WRITER.md` | Remove 5 rows from Special Document Types table |
| `INTEGRATION_ANALYSIS.md` | Update sections 1 and 5 |
| `docs/original/SKILLS.md` | Remove/annotate 5 skill sections |
| `CHANGELOG.md` | Add removal entry |

---

## Rollback Plan

If issues arise, restore from git:

```bash
git checkout HEAD~1 -- .claude/skills/ skills/ scientific_writer/.claude/skills/
```

---

## Notes

- The `docs/original/` files are archived upstream documentation; consider whether to edit or leave as historical reference with annotations
- The `skills/` directory appears to be a duplicate of `.claude/skills/` - consider consolidating in a future cleanup
- The `scientific_writer/` subdirectory contains another copy of the skills - this may warrant investigation for whether it should exist at all

---

*Plan created: December 23, 2025*
