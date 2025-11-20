# Scientific Writer 2.8.0 - Nano Banana Pro Scientific Schematics 🎨

**Release Date:** November 20, 2025

## 🚀 Headline Feature: AI-Powered Scientific Diagrams with Nano Banana Pro

Version 2.8.0 introduces **Nano Banana Pro**, a revolutionary AI-powered system for generating publication-quality scientific diagrams from natural language descriptions. No coding, no templates, no manual drawing required—just describe what you want, and Nano Banana Pro creates it automatically.

### ✨ Simply Describe Your Diagram

```bash
# CONSORT flowchart
python scripts/generate_schematic.py \
  "CONSORT participant flow: screened n=500, excluded n=150, randomized n=350" \
  -o consort.png

# Neural network architecture
python scripts/generate_schematic.py \
  "Transformer architecture with encoder and decoder, show attention mechanism" \
  -o transformer.png

# Biological pathway
python scripts/generate_schematic.py \
  "MAPK signaling pathway: EGFR → RAS → RAF → MEK → ERK → nucleus" \
  -o mapk.png
```

**That's it!** Nano Banana Pro automatically:
- ✅ Generates your diagram from the description
- ✅ Reviews quality and identifies improvements
- ✅ Iteratively refines the diagram (3 iterations by default)
- ✅ Produces publication-ready output

## 🎯 What Makes Nano Banana Pro Special

### 1. **Automatic Iterative Refinement**

Nano Banana Pro doesn't just generate once—it improves your diagram through an intelligent review cycle:

**Iteration 1:** Initial generation from your description
- AI evaluates: clarity, labels, accuracy, accessibility
- Scores the diagram (0-10) with specific critiques

**Iteration 2:** Improvements based on feedback
- Addresses specific issues identified in review
- Re-evaluates with updated quality assessment

**Iteration 3:** Final polished version
- Incorporates all feedback from previous iterations
- Publication-ready output

**Example progression:**
```
v1: Score 7.0 - "Good structure, but font size too small, labels overlap"
v2: Score 8.5 - "Much improved readability, minor spacing issues remain"
v3: Score 9.5 - "Excellent. Publication ready. Professional quality."
```

### 2. **Built-In Scientific Quality Standards**

Every diagram automatically follows best practices:

**Visual Quality:**
- Clean white/light backgrounds
- High contrast for readability
- Sharp, clear lines and text
- Professional appearance

**Typography:**
- Sans-serif fonts (Arial, Helvetica)
- Minimum 10pt font size
- Consistent sizing throughout
- No overlapping text

**Scientific Standards:**
- Accurate representation of concepts
- Clear labels for all components
- Appropriate scale bars, legends, axes
- Standard notation and symbols

**Accessibility:**
- Colorblind-friendly color palettes (Okabe-Ito scheme)
- High contrast ratios
- Grayscale-compatible designs
- WCAG 2.1 compliant

### 3. **Universal Diagram Support**

Nano Banana Pro works for **any** type of scientific diagram:

**Clinical & Medical:**
- CONSORT participant flowcharts
- Clinical trial designs
- Diagnostic algorithms
- Medical decision trees
- Patient treatment pathways

**Computational & AI:**
- Neural network architectures (CNNs, Transformers, RNNs)
- Algorithm flowcharts
- System architectures
- Data pipelines
- Software workflows

**Biological & Chemical:**
- Signaling pathways (MAPK, PI3K/AKT, etc.)
- Metabolic pathways
- Gene regulation networks
- Protein structures
- Chemical reaction schemes

**Engineering & Physics:**
- Circuit diagrams
- Block diagrams
- System architectures
- Signal processing flows
- Experimental setups

**And Many More:**
- Study designs
- Conceptual frameworks
- Process diagrams
- Organizational charts
- Timeline diagrams

### 4. **Comprehensive Output**

For every diagram, you receive:

```
your_diagram_v1.png          # First iteration
your_diagram_v2.png          # Second iteration
your_diagram_v3.png          # Final polished version
your_diagram.png             # Copy of final (for convenience)
your_diagram_review_log.json # Detailed quality assessment
```

**Review Log Example:**
```json
{
  "user_prompt": "CONSORT participant flow diagram...",
  "iterations": [
    {
      "iteration": 1,
      "image_path": "figures/consort_v1.png",
      "score": 7.0,
      "critique": "Good structure. Issues: font too small at 8pt (need 10pt+), 
                  some labels overlap, arrows could be clearer.",
      "success": true
    },
    {
      "iteration": 2,
      "score": 8.5,
      "critique": "Much improved. Font now readable, labels clear. 
                  Minor spacing issues in exclusion criteria box.",
      "success": true
    },
    {
      "iteration": 3,
      "score": 9.5,
      "critique": "Excellent. Publication ready. Professional quality, 
                  clear hierarchy, excellent readability.",
      "success": true
    }
  ],
  "final_image": "figures/consort_v3.png",
  "final_score": 9.5,
  "success": true
}
```

## 📖 Real-World Examples

### Example 1: Clinical Research

**Prompt:**
```bash
python scripts/generate_schematic.py \
  "CONSORT participant flow diagram for RCT.
   Assessed for eligibility (n=500).
   Excluded (n=150): age<18 (n=80), declined (n=50), other (n=20).
   Randomized (n=350) into Treatment (n=175) and Control (n=175).
   Lost to follow-up: 15 and 10 respectively.
   Final analysis: 160 and 165." \
  -o figures/consort.png
```

**Result:** Professional CONSORT flowchart ready for journal submission

### Example 2: Deep Learning Architecture

**Prompt:**
```bash
python scripts/generate_schematic.py \
  "Transformer architecture. Left side: encoder with input embedding, 
   positional encoding, multi-head self-attention, feed-forward layers. 
   Right side: decoder with masked attention, cross-attention, feed-forward. 
   Show attention connections from encoder to decoder. 
   Label all components with dimensions." \
  -o figures/transformer.png --iterations 5
```

**Result:** Detailed architecture diagram suitable for conference papers

### Example 3: Biological Pathway

**Prompt:**
```bash
python scripts/generate_schematic.py \
  "MAPK signaling pathway showing activation cascade. 
   Start with EGFR receptor at membrane → RAS → RAF → MEK → ERK → nucleus. 
   Label each phosphorylation step. Use different colors for each kinase. 
   Include inhibitor binding sites." \
  -o figures/mapk.png
```

**Result:** Publication-quality pathway diagram with proper biological notation

## 🎓 Prompt Engineering Tips

### ✅ **Effective Prompts (Specific & Detailed)**

**Good:**
```
"CONSORT flowchart with vertical flow, top to bottom. 
 Screening box at top (n=500), exclusion criteria in middle (n=150), 
 randomization at bottom (n=350 split into two groups)"
```

**Why it works:**
- Specifies layout direction (vertical, top-to-bottom)
- Includes all quantitative details
- Describes structure clearly
- Mentions grouping explicitly

### ❌ **Ineffective Prompts (Too Vague)**

**Bad:**
```
"Make a flowchart"
```

**Why it fails:**
- No structural details
- No content specified
- No layout guidance
- Missing quantitative information

### 🌟 **Key Elements of Great Prompts:**

1. **Specify Layout:**
   - "Vertical flow, top to bottom"
   - "Architecture with encoder on left, decoder on right"
   - "Circular pathway around central hub"

2. **Include Quantitative Details:**
   - "Neural network: input layer (784 nodes), hidden (128), output (10)"
   - "Patient flow: n=500 screened, n=150 excluded, n=350 randomized"
   - "Pathway with 5 phosphorylation steps"

3. **Describe Visual Style:**
   - "Minimalist block diagram with clean lines"
   - "Detailed biological pathway with protein structures"
   - "Technical schematic with engineering notation"

4. **Request Specific Labels:**
   - "Label all arrows with activation/inhibition"
   - "Include layer dimensions in each box"
   - "Show molecular weights for each protein"

5. **Mention Color Requirements:**
   - "Use colorblind-friendly palette"
   - "Grayscale-compatible design"
   - "Color-code by function: blue=input, green=processing, red=output"

## 🚀 Getting Started

### Step 1: Get Your API Key

Visit https://openrouter.ai/keys to get your OpenRouter API key.

### Step 2: Set Environment Variable

```bash
# One-time setup
export OPENROUTER_API_KEY='sk-or-v1-your_key_here'

# Make it permanent (add to ~/.bashrc or ~/.zshrc)
echo 'export OPENROUTER_API_KEY="sk-or-v1-your_key"' >> ~/.zshrc
source ~/.zshrc
```

### Step 3: Generate Your First Diagram

```bash
# Try a simple test
python scripts/generate_schematic.py \
  "Simple flowchart with 3 boxes connected by arrows" \
  -o test.png

# Check the outputs
ls test*.png              # v1, v2, v3 versions
cat test_review_log.json  # Quality scores and feedback
```

### Step 4: Review the Results

Open the generated images:
- `test_v1.png` - See the initial generation
- `test_v2.png` - Notice the improvements
- `test_v3.png` - Final polished version

Read the review log to understand the quality progression.

## 🔧 Advanced Features

### Custom Iteration Count

Need more refinement? Adjust the iteration count:

```bash
# 5 iterations for complex diagrams
python scripts/generate_schematic.py \
  "Complex multi-layer neural network architecture" \
  -o complex_nn.png \
  --iterations 5
```

### Verbose Mode for Debugging

See detailed progress and API interactions:

```bash
python scripts/generate_schematic.py \
  "diagram description" \
  -o output.png \
  -v  # Verbose mode
```

### Python API Integration

Use Nano Banana Pro programmatically in your own code:

```python
from scripts.generate_schematic_ai import ScientificSchematicGenerator

# Initialize generator
generator = ScientificSchematicGenerator(
    api_key="your_key_here",
    verbose=True
)

# Generate with iterative refinement
results = generator.generate_iterative(
    user_prompt="CONSORT flowchart for clinical trial",
    output_path="figures/consort.png",
    iterations=3
)

# Access results
print(f"Final quality score: {results['final_score']}/10")
print(f"Final image: {results['final_image']}")

# Review all iterations
for iteration in results['iterations']:
    print(f"Iteration {iteration['iteration']}: {iteration['score']}/10")
    print(f"  Critique: {iteration['critique']}")
```

## 📊 Performance & Cost

### Speed

**Generation Time (typical):**
- Iteration 1: ~15-30 seconds
- Iteration 2: ~15-30 seconds
- Iteration 3: ~15-30 seconds
- **Total: ~1-2 minutes** for publication-ready diagram

### Cost

**Per Diagram (3 iterations):**
- Simple diagrams: **$0.10 - $0.30**
- Complex diagrams: **$0.30 - $0.50**

**Model Pricing:**
- Nano Banana Pro (via OpenRouter)
- ~$2/M input tokens
- ~$12/M output tokens

**Cost-Effective:**
- Much faster than manual drawing
- Cheaper than hiring a graphic designer
- Includes automatic quality review
- Multiple iterations for refinement

## 🎨 Example Gallery

Check out real examples in the `figures/` directory:

**Generated with Nano Banana Pro:**
- `google_gemini_architecture.png` - Complex AI system architecture
- `gemini_moe_architecture.png` - Mixture-of-Experts diagram
- `test_nano_banana.png` - Test diagram showcasing capabilities

**With Review Logs:**
- `*_review_log.json` - See quality scores and critiques

## 🛠️ Integration with Scientific Writer

Nano Banana Pro is fully integrated into the Scientific Writer workflow:

### In Paper Generation

```bash
scientific-writer
> Create a Nature Methods paper on a novel microscopy technique

# The system will:
# ✓ Generate the paper content
# ✓ Automatically create diagrams using Nano Banana Pro
# ✓ Include figures in the LaTeX document
# ✓ Compile to professional PDF
```

### Standalone Usage

```bash
# Generate diagrams independently
python scripts/generate_schematic.py "diagram description" -o output.png

# Use in your own LaTeX documents
\begin{figure}
  \includegraphics[width=\textwidth]{figures/your_diagram.png}
  \caption{AI-generated diagram with Nano Banana Pro}
\end{figure}
```

## 📚 Documentation

### Complete Resources

- **Quick Start:** `skills/scientific-schematics/QUICK_REFERENCE.md`
- **Full Documentation:** `skills/scientific-schematics/README.md`
- **Implementation Details:** `skills/scientific-schematics/IMPLEMENTATION_SUMMARY.md`
- **Comprehensive Skill Guide:** `skills/scientific-schematics/SKILL.md`

### Example Scripts

- **Basic Usage:** `skills/scientific-schematics/example_usage.sh`
- **Test Suite:** `skills/scientific-schematics/test_ai_generation.py`
- **Python Examples:** See README.md

## 🧪 Verification

Run the test suite to verify your installation:

```bash
cd skills/scientific-schematics
python test_ai_generation.py

# Expected output:
# ✓ PASS: File Structure
# ✓ PASS: Imports
# ✓ PASS: Class Structure
# ✓ PASS: Error Handling
# ✓ PASS: Wrapper Script
# ✓ PASS: Prompt Engineering
# 
# Total: 6/6 tests passed
```

## 🎯 Key Benefits

### For Researchers
- ✅ **No artistic skills required** - Just describe what you need
- ✅ **Fast turnaround** - Minutes instead of hours/days
- ✅ **Publication quality** - Automatic adherence to standards
- ✅ **Iterative refinement** - Continuous improvement until perfect

### For Paper Writing
- ✅ **Integrated workflow** - Works seamlessly with Scientific Writer
- ✅ **Professional output** - Ready for journal submission
- ✅ **Reproducible** - Save prompts to regenerate diagrams
- ✅ **Version control** - Track iterations and improvements

### For Teaching & Presentations
- ✅ **Quick visualization** - Generate diagrams for lectures instantly
- ✅ **Clear communication** - Optimized for educational clarity
- ✅ **Customizable** - Easy to iterate based on feedback
- ✅ **Accessible** - Colorblind-friendly and high contrast

## 🔄 Backward Compatibility

All existing features remain fully functional:

- ✅ Code-based diagram generation still available via `--method code`
- ✅ All existing templates and scripts unchanged
- ✅ Graphviz, TikZ, and other tools still supported
- ✅ Classic workflow available for users who prefer it

```bash
# Use classic code-based generation if preferred
python scripts/generate_schematic.py \
  "diagram description" \
  -o output.tex \
  --method code
```

## 📦 Installation

Update to version 2.8.0:

```bash
# Using pip
pip install scientific-writer==2.8.0

# Using uv
uv pip install scientific-writer==2.8.0

# One-time use with uvx
uvx scientific-writer@2.8.0
```

## 🐛 Troubleshooting

### Common Issues

**1. API Key Not Found**
```bash
# Check if set
echo $OPENROUTER_API_KEY

# Set it
export OPENROUTER_API_KEY='your_key'
```

**2. Import Errors**
```bash
# Install required library
pip install requests
```

**3. Low Quality Scores**
- Make your prompt more specific
- Include more layout and labeling details
- Increase iterations: `--iterations 5`
- Use verbose mode to see AI feedback: `-v`

**4. Generation Fails**
```bash
# Check API status
curl https://openrouter.ai/api/v1/models

# Try verbose mode for detailed error messages
python scripts/generate_schematic.py "test" -o test.png -v
```

## 🙏 Acknowledgments

Nano Banana Pro is powered by:
- **OpenRouter API** - Unified API for accessing AI models
- **Google Gemini** - Advanced vision and generation capabilities
- **Scientific Writer Framework** - Integrated scientific document generation

Special thanks to the research community for feedback and testing.

## 🚀 What's Next

Future enhancements planned:
- Multi-panel figure generation
- Automatic legend and caption generation
- Style transfer from example diagrams
- Batch processing for multiple diagrams
- Interactive refinement via CLI
- Integration with more publication venues

## 📖 Learn More

- **GitHub:** https://github.com/K-Dense-AI/claude-scientific-writer
- **Documentation:** See `docs/` directory
- **Examples:** See `paper_outputs/` for real-world usage
- **Support:** Open an issue on GitHub

---

## 💻 Quick Command Reference

```bash
# Basic generation
python scripts/generate_schematic.py "description" -o output.png

# With custom iterations
python scripts/generate_schematic.py "description" -o output.png --iterations 5

# Verbose mode
python scripts/generate_schematic.py "description" -o output.png -v

# Help
python scripts/generate_schematic.py --help

# Test installation
python skills/scientific-schematics/test_ai_generation.py
```

---

**Happy diagram generation! 🎨✨**

Simply describe your scientific diagram, and let Nano Banana Pro create it automatically—publication-ready in minutes.

*Scientific Writer 2.8.0 - Making scientific visualization accessible to everyone.*

