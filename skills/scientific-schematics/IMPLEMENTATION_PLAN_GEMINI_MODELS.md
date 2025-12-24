# Implementation Plan: Gemini 3 Model Configuration

> Scientific Schematics Skill - Model Upgrade
> Created: 2025-12-24
> Status: Planning

---

## Background

### Current Architecture

The scientific-schematics skill uses two AI models via OpenRouter:

| Role | Current Model | OpenRouter ID |
|------|---------------|---------------|
| **Image Generation** | Nano Banana Pro | `google/gemini-3-pro-image-preview` |
| **Quality Review** | Gemini 3 Pro | `google/gemini-3-pro` |

### Problem Statement

1. **Cost**: Gemini 3 Pro is expensive for quality review, which is a simpler task
2. **Speed**: Pro is slower than Flash for the review workload
3. **No flexibility**: Users cannot choose between speed/cost vs quality

### Proposed Solution

Use **Gemini 3 Flash Preview** as the default for quality review, with **Gemini 3 Pro** available as an option for critical work.

| Role | Default Model | Optional Model |
|------|---------------|----------------|
| **Image Generation** | Nano Banana Pro | (no change - specialized) |
| **Quality Review** | Gemini 3 Flash Preview | Gemini 3 Pro (on request) |

### Model Characteristics

**Gemini 3 Flash Preview** (`google/gemini-3-flash`)
- High speed, lower latency
- Good for structured evaluation tasks
- Requires strong prompting for best results
- 1M token context window
- Configurable thinking levels

**Gemini 3 Pro** (`google/gemini-3-pro`)
- Flagship frontier model
- Best for complex reasoning
- Higher cost and latency
- State-of-the-art benchmark results

**Nano Banana Pro** (`google/gemini-3-pro-image-preview`)
- Specialized for image generation
- Industry-leading text rendering in images
- Supports 2K/4K outputs
- No replacement available - keep as-is

---

## Claude Code Skill Compatibility

### How Skills Call External Models

When Claude Code executes this skill:
1. Claude reads SKILL.md and understands the workflow
2. Claude uses **Bash tool** to run `python scripts/generate_schematic.py`
3. The Python script uses `requests` library to call OpenRouter API
4. OpenRouter routes to the appropriate Google model

### Requirements for Skill Execution

| Requirement | Current Status | Notes |
|-------------|----------------|-------|
| OPENROUTER_API_KEY | Required env var | User must set this |
| Python 3.10+ | Required | Standard in most environments |
| `requests` library | Required dependency | `pip install requests` |
| Network access | Required | Must reach openrouter.ai |

### Bash Tool Permissions

The skill's `allowed-tools` includes `Bash`, which enables:
```yaml
allowed-tools: [Read, Write, Edit, Bash]
```

This allows Claude to execute the Python scripts that call external APIs.

---

## Files Requiring Changes

### Primary Changes

| File | Lines | Change Type | Priority |
|------|-------|-------------|----------|
| `scripts/generate_schematic_ai.py` | 838 | Core implementation | **P0** |
| `scripts/generate_schematic.py` | 140 | CLI wrapper | **P0** |
| `SKILL.md` | 614 | Documentation | **P1** |

### Secondary Changes

| File | Lines | Change Type | Priority |
|------|-------|-------------|----------|
| `README.md` | 328 | User documentation | **P2** |
| `QUICK_REFERENCE.md` | 208 | Quick reference | **P2** |
| `test_ai_generation.py` | 243 | Test updates | **P2** |
| `example_usage.sh` | 90 | Example updates | **P3** |

### No Changes Required

| File | Reason |
|------|--------|
| `references/best_practices.md` | Model-agnostic content |

---

## Detailed Implementation Plan

### Phase 1: Core Script Changes (P0)

#### 1.1 Update `scripts/generate_schematic_ai.py`

**Location**: Lines 167-172 (model definitions)

```python
# CURRENT:
self.image_model = "google/gemini-3-pro-image-preview"
self.review_model = "google/gemini-3-pro"

# PROPOSED:
self.image_model = "google/gemini-3-pro-image-preview"  # Keep - specialized
self.review_model = "google/gemini-3-flash"  # Default to Flash
self.review_model_pro = "google/gemini-3-pro"  # Available on request
```

**Constructor Changes** (around line 140):

```python
def __init__(self, api_key: Optional[str] = None,
             verbose: bool = False,
             review_model: str = "flash"):  # NEW PARAMETER
    """
    Initialize the generator.

    Args:
        api_key: OpenRouter API key
        verbose: Print detailed progress
        review_model: "flash" (default, faster) or "pro" (higher quality)
    """
    # ... existing code ...

    # Model selection
    self.image_model = "google/gemini-3-pro-image-preview"

    # Review model selection
    if review_model.lower() == "pro":
        self.review_model = "google/gemini-3-pro"
        self.review_model_name = "Gemini 3 Pro"
    else:
        self.review_model = "google/gemini-3-flash"
        self.review_model_name = "Gemini 3 Flash Preview"
```

**Strengthen Review Prompt** (around line 446):

The current review prompt is already well-structured with:
- Explicit scoring rubric (5 categories, 0-2 points each)
- Exact output format specification
- Clear decision criteria

For Flash optimization, add:
1. **Thinking level hint** in the prompt
2. **JSON output option** for more reliable parsing
3. **Step-by-step reasoning request**

```python
# Enhanced review prompt for Flash
review_prompt = f"""You are an expert reviewer evaluating a scientific diagram.

TASK: Evaluate this diagram systematically, then provide a structured assessment.

STEP 1: Examine the diagram carefully
STEP 2: Score each criterion (0-2 points)
STEP 3: List specific strengths and issues
STEP 4: Determine if quality meets threshold

ORIGINAL REQUEST: {original_prompt}
DOCUMENT TYPE: {doc_type} (quality threshold: {threshold}/10)

SCORING CRITERIA (evaluate each 0-2 points):

1. SCIENTIFIC ACCURACY
   - 0: Major errors or misrepresentations
   - 1: Minor inaccuracies
   - 2: Correct concepts, notation, relationships

2. CLARITY AND READABILITY
   - 0: Confusing or ambiguous
   - 1: Mostly clear, some issues
   - 2: Easy to understand, clear hierarchy

3. LABEL QUALITY
   - 0: Missing or unreadable labels
   - 1: Some labels unclear or incomplete
   - 2: All elements labeled clearly

4. LAYOUT AND COMPOSITION
   - 0: Poor flow, overlapping elements
   - 1: Acceptable layout, minor issues
   - 2: Logical flow, balanced, no overlaps

5. PROFESSIONAL APPEARANCE
   - 0: Draft quality
   - 1: Acceptable but needs polish
   - 2: Publication-ready

RESPOND IN THIS EXACT FORMAT:
```
SCORE: [sum of all criteria, 0-10]

STRENGTHS:
- [specific strength 1]
- [specific strength 2]

ISSUES:
- [specific issue 1, if any]
- [specific issue 2, if any]

VERDICT: [ACCEPTABLE if score >= {threshold}, else NEEDS_IMPROVEMENT]
```

Remember: Score >= {threshold} means ACCEPTABLE for {doc_type} publication."""
```

**Update Console Output** (around line 681):

```python
# Current:
print(f"Reviewing image with Gemini 3 Pro...")

# Proposed:
print(f"Reviewing image with {self.review_model_name}...")
```

#### 1.2 Update `scripts/generate_schematic.py`

**Add CLI Flag** (around line 79):

```python
parser.add_argument("--review-model", default="flash",
                   choices=["flash", "pro"],
                   help="Review model: 'flash' (default, faster) or 'pro' (higher quality)")
```

**Pass to AI Script** (around line 112):

```python
# Build command
cmd = [sys.executable, str(ai_script), args.prompt, "-o", args.output]

# Add review model
if args.review_model != "flash":
    cmd.extend(["--review-model", args.review_model])
```

**Update Help Text** (around line 34):

```python
epilog="""
How it works:
  Simply describe your diagram in natural language
  Nano Banana Pro generates it automatically with:
  - Smart iteration (only regenerates if quality is below threshold)
  - Quality review by Gemini 3 Flash Preview (or Pro with --review-model pro)
  - Document-type aware quality thresholds
  - Publication-ready output

Review Models:
  flash    (default)  - Gemini 3 Flash Preview - faster, cost-effective
  pro                 - Gemini 3 Pro - higher quality for critical work
...
"""
```

---

### Phase 2: Documentation Updates (P1-P2)

#### 2.1 Update `SKILL.md`

**Sections to update**:

1. **Line 3 (description)**: Update model mention
   ```markdown
   description: "Create publication-quality scientific diagrams using Nano Banana Pro AI
   with smart iterative refinement. Uses Gemini 3 Flash Preview for quality review
   (Gemini 3 Pro available for critical work)..."
   ```

2. **Lines 9-18 (Overview)**: Update model descriptions
   ```markdown
   **How it works:**
   - Describe your diagram in natural language
   - Nano Banana Pro generates publication-quality images automatically
   - **Gemini 3 Flash Preview reviews quality** (or Gemini 3 Pro for critical work)
   - **Smart iteration**: Only regenerates if quality is below threshold
   ```

3. **Lines 69-74 (Configuration)**: Add review model option
   ```markdown
   ### Configuration

   Set your OpenRouter API key:
   ```bash
   export OPENROUTER_API_KEY='your_api_key_here'
   ```

   Choose review model (optional):
   - `--review-model flash` (default) - Faster, cost-effective
   - `--review-model pro` - Higher quality for journal submissions
   ```

4. **Lines 280-302 (Command-Line Options)**: Add new flag
   ```markdown
   # Use Gemini 3 Pro for high-stakes review
   python scripts/generate_schematic.py "diagram" -o out.png --review-model pro
   ```

5. **Lines 150-172 (Workflow diagram)**: Update model names in diagram

#### 2.2 Update `README.md`

**Key sections**:

1. **Line 28-30**: Update feature description
2. **Line 130-134**: Add `--review-model` to options table
3. **Line 297-305**: Update cost section with model pricing

#### 2.3 Update `QUICK_REFERENCE.md`

**Key sections**:

1. **Line 3**: Update model mention
2. **Line 59-65**: Add review model to options table
3. **Line 165-168**: Update cost estimates

---

### Phase 3: Testing Updates (P2)

#### 3.1 Update `test_ai_generation.py`

**Add test for review model parameter** (after line 75):

```python
def test_review_model_selection():
    """Test review model selection."""
    print("\nTesting review model selection...")
    try:
        from generate_schematic_ai import ScientificSchematicGenerator

        # Test default (flash)
        gen_flash = ScientificSchematicGenerator(api_key="test_key", review_model="flash")
        if "flash" not in gen_flash.review_model:
            print("✗ Default review model should be Flash")
            return False
        print(f"✓ Default review model: {gen_flash.review_model}")

        # Test pro option
        gen_pro = ScientificSchematicGenerator(api_key="test_key", review_model="pro")
        if "pro" not in gen_pro.review_model or "flash" in gen_pro.review_model:
            print("✗ Pro review model not set correctly")
            return False
        print(f"✓ Pro review model: {gen_pro.review_model}")

        return True
    except Exception as e:
        print(f"✗ Review model test failed: {e}")
        return False
```

**Add to test list** (around line 198):

```python
tests = [
    ("File Structure", test_file_paths),
    ("Imports", test_imports),
    ("Class Structure", test_class_structure),
    ("Review Model Selection", test_review_model_selection),  # NEW
    ("Error Handling", test_error_handling),
    ("Wrapper Script", test_wrapper_script),
    ("Prompt Engineering", test_prompt_engineering),
]
```

---

### Phase 4: Example Updates (P3)

#### 4.1 Update `example_usage.sh`

**Add example with Pro model** (after line 67):

```bash
# Example 4: High-stakes journal figure with Pro review
echo "Example 4: Journal Figure with Pro Review"
echo "------------------------------------------"
python scripts/generate_schematic.py \
  "Complex multi-panel figure showing experimental workflow" \
  -o figures/journal_figure.png \
  --doc-type journal \
  --review-model pro \
  --iterations 2

echo ""
echo "✓ Generated with Gemini 3 Pro review for journal quality"
```

---

## Implementation Checklist

### Phase 1: Core Changes (P0)
- [ ] Update `generate_schematic_ai.py` - model selection
- [ ] Update `generate_schematic_ai.py` - constructor parameter
- [ ] Update `generate_schematic_ai.py` - strengthen review prompt
- [ ] Update `generate_schematic_ai.py` - console output
- [ ] Update `generate_schematic.py` - CLI flag
- [ ] Update `generate_schematic.py` - pass parameter
- [ ] Update `generate_schematic.py` - help text

### Phase 2: Documentation (P1-P2)
- [ ] Update `SKILL.md` - description
- [ ] Update `SKILL.md` - overview section
- [ ] Update `SKILL.md` - configuration section
- [ ] Update `SKILL.md` - command-line options
- [ ] Update `SKILL.md` - workflow diagram
- [ ] Update `README.md` - features
- [ ] Update `README.md` - options table
- [ ] Update `README.md` - cost section
- [ ] Update `QUICK_REFERENCE.md` - model mention
- [ ] Update `QUICK_REFERENCE.md` - options table
- [ ] Update `QUICK_REFERENCE.md` - cost estimates

### Phase 3: Testing (P2)
- [ ] Add `test_review_model_selection()` function
- [ ] Add to test list
- [ ] Run full test suite

### Phase 4: Examples (P3)
- [ ] Update `example_usage.sh` with Pro example

### Final Validation
- [ ] Test with actual API call (Flash default)
- [ ] Test with actual API call (Pro override)
- [ ] Verify skill works when invoked via Claude Code
- [ ] Update CHANGELOG.md

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Flash produces lower quality reviews | Medium | Medium | Strengthened prompts, Pro option available |
| API format differences between Flash/Pro | Low | High | Both use same OpenRouter format |
| Breaking change for existing users | Low | Low | Default behavior is similar |
| OpenRouter model availability | Low | High | Monitor OpenRouter status |

---

## Rollback Plan

If issues arise:
1. Revert `review_model` default back to `"google/gemini-3-pro"`
2. Keep the `--review-model` flag for flexibility
3. Document the change in CHANGELOG.md

---

## Success Criteria

1. **Functional**: Diagrams generate successfully with Flash review
2. **Quality**: Review scores comparable to Pro (within 0.5 points)
3. **Speed**: Noticeable latency improvement for review step
4. **Flexibility**: Users can override to Pro when needed
5. **Documentation**: All docs updated consistently

---

## Approval

- [ ] User approves implementation plan
- [ ] Ready to proceed with Phase 1

---

*Implementation plan created for scientific-schematics skill model configuration update.*
