# Smart Iterative Refinement

The generate-review-refine loop, the command-line reference, and configuration.

## Smart Iterative Refinement

### How It Works

```
┌─────────────────────────────────────────────────────┐
│  1. Generate infographic with Nano Banana Pro       │
│                    ↓                                │
│  2. Review quality with Gemini 3.6 Flash            │
│                    ↓                                │
│  3. Score >= threshold?                             │
│       YES → DONE! (early stop)                      │
│       NO  → Improve prompt, go to step 1            │
│                    ↓                                │
│  4. Repeat until quality met OR max iterations      │
└─────────────────────────────────────────────────────┘
```

### Quality Review Criteria

Gemini 3.6 Flash evaluates each infographic on:

1. **Visual Hierarchy & Layout** (0-2 points)
   - Clear visual hierarchy
   - Logical reading flow
   - Balanced composition

2. **Typography & Readability** (0-2 points)
   - Readable text
   - Bold headlines
   - No overlapping

3. **Data Visualization** (0-2 points)
   - Prominent numbers
   - Clear charts/icons
   - Proper labels

4. **Color & Accessibility** (0-2 points)
   - Professional colors
   - Sufficient contrast
   - Colorblind-friendly

5. **Overall Impact** (0-2 points)
   - Professional appearance
   - Free of visual bugs
   - Achieves communication goal

### Review Log

Each generation produces a JSON review log:
```json
{
  "user_prompt": "5 benefits of exercise...",
  "infographic_type": "list",
  "style": "healthcare",
  "doc_type": "marketing",
  "quality_threshold": 8.5,
  "iterations": [
    {
      "iteration": 1,
      "image_path": "figures/exercise_v1.png",
      "score": 8.7,
      "needs_improvement": false,
      "critique": "SCORE: 8.7\nSTRENGTHS:..."
    }
  ],
  "final_score": 8.7,
  "early_stop": true,
  "early_stop_reason": "Quality score 8.7 meets threshold 8.5"
}
```

---

## Command-Line Reference

```bash
python skills/infographics/scripts/generate_infographic.py [OPTIONS] PROMPT

Arguments:
  PROMPT                    Description of the infographic content

Options:
  -o, --output PATH         Output file path (required)
  -t, --type TYPE           Infographic type preset
  -s, --style STYLE         Industry style preset
  -p, --palette PALETTE     Colorblind-safe palette
  -b, --background COLOR    Background color (default: white)
  --doc-type TYPE           Document type for quality threshold
  --iterations N            Maximum refinement iterations (default: 3)
  --api-key KEY             OpenRouter API key
  -v, --verbose             Verbose output
  --list-options            List all available options
```

### List All Options

```bash
python skills/infographics/scripts/generate_infographic.py --list-options
```

---

## Configuration

### API Key Setup

Set your OpenRouter API key:
```bash
export OPENROUTER_API_KEY='your_api_key_here'
```

Get an API key at: https://openrouter.ai/keys

---
