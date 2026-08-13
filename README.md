# Claude Scientific Writer

[![PyPI version](https://img.shields.io/pypi/v/scientific-writer.svg)](https://pypi.org/project/scientific-writer/)
[![Total Downloads](https://static.pepy.tech/badge/scientific-writer)](https://pepy.tech/project/scientific-writer)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![X](https://img.shields.io/badge/Follow_on_X-%40k__dense__ai-000000?logo=x)](https://x.com/k_dense_ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-K--Dense_Inc.-0A66C2?logo=linkedin)](https://www.linkedin.com/company/k-dense-inc)
[![YouTube](https://img.shields.io/badge/YouTube-K--Dense_Inc.-FF0000?logo=youtube)](https://www.youtube.com/@K-Dense-Inc)

> 🚀 **Looking for more advanced capabilities?** For end-to-end scientific writing, deep scientific search, advanced image generation and enterprise solutions, visit **[www.k-dense.ai](https://www.k-dense.ai)**

> **Stay up to date:** Follow K-Dense on [X](https://x.com/k_dense_ai), [LinkedIn](https://www.linkedin.com/company/k-dense-inc), and [YouTube](https://www.youtube.com/@K-Dense-Inc) for new features, release announcements, walkthroughs, research workflow demos, and examples you can use with Scientific Writer.

**A deep research and writing tool** that combines the power of AI-driven deep research with well-formatted written outputs. Generate publication-ready scientific papers, reports, posters, grant proposals, literature reviews, and more academic documents—all backed by real-time literature search and verified citations.

Scientific Writer performs comprehensive research before writing, ensuring every claim is supported by real, verifiable sources. Features include real-time research lookup through Parallel Search and Extract, intelligent paper detection, comprehensive document conversion, and AI-powered diagram generation. You can use it as a Claude Code plugin, Python package, or native CLI.

## Quick Start

### Prerequisites
- Python 3.10 or newer
- ANTHROPIC_API_KEY (required)
- Parallel CLI authentication (`parallel-cli login`) or `PARALLEL_API_KEY`
- OPENROUTER_API_KEY (optional, for AI image generation: schematics, figures, slides, and infographics)
- A LaTeX distribution for PDF generation (`pdflatex`, `bibtex`, and preferably `latexmk`)
- Optional: LibreOffice for Office rendering/recalculation and FFmpeg for media conversion

### Installation Options

#### Option 1: Claude Code Plugin (Recommended) ⭐
The easiest way to use Scientific Writer is as a Claude Code plugin. See the [Plugin Installation](#-use-as-a-claude-code-plugin-recommended) section below.

#### Option 2: Install from PyPI (CLI/API Usage)
```bash
pip install scientific-writer

# Optional bundled-script runtimes
pip install "scientific-writer[analysis]"  # cohort statistics and survival analysis
pip install "scientific-writer[office]"    # DOCX/PPTX/XLSX and MarkItDown helpers
```

#### Option 3: Install from source with uv
```bash
git clone https://github.com/K-Dense-AI/claude-scientific-writer.git
cd claude-scientific-writer
uv sync
```

### Configure API keys
```bash
# .env file (recommended) — see .env.example for the full list
echo "ANTHROPIC_API_KEY=your_key" > .env
echo "PARALLEL_API_KEY=your_parallel_key" >> .env            # research lookup and web search
echo "OPENROUTER_API_KEY=your_openrouter_key" >> .env        # optional: AI image generation
# or export in your shell
export ANTHROPIC_API_KEY='your_key'
```

Install and authenticate the research CLI when it is not already available:

```bash
uv tool install "parallel-web-tools[cli]==0.7.1"
parallel-cli login
parallel-cli auth
```

### Usage Options

#### Use as Plugin (Recommended)
After installing the plugin and running `/claude-scientific-writer:scientific-writer-init`, simply ask Claude:
```bash
> Create a Nature paper on CRISPR gene editing. Present experimental_data.csv 
  (efficiency across 5 cell lines), include Western_blot.png and flow_cytometry.png 
  showing 87% editing efficiency (p<0.001). Compare with literature benchmarks.

> Generate an NSF grant proposal presenting preliminary data from quantum_results.csv 
  (99.2% gate fidelity), circuit_topology.png, and error_rates.csv. 
  Include 5-year timeline with milestones_budget.xlsx.

> @research-lookup Find papers on mRNA vaccine efficacy (2022-2024). Compare 
  with our trial_outcomes.csv (n=500, 94% efficacy) and antibody_titers.png.
```

#### Use the CLI
```bash
# If installed via pip
scientific-writer
scientific-writer --effort high

# If installed from source with uv
uv run scientific-writer
```

Use `scientific-writer --help` for permission, budget, token-usage, and input-consumption controls. Input files are preserved by default; `--consume-inputs` explicitly removes them after a successful copy.

#### Use the Python API
```python
import asyncio
from scientific_writer import generate_paper

async def main():
    # Detailed prompt with specific data and figures
    async for update in generate_paper(
        query=(
            "Create a Nature paper on CRISPR gene editing. "
            "Present editing_efficiency.csv (5 cell lines, n=200 cells each). "
            "Include Western blot (protein_knockout.png) showing target depletion, "
            "flow cytometry data (editing_percentages.png) with 87% efficiency in HEK293, "
            "and off_target_analysis.csv showing <0.1% off-target effects. "
            "Compare results to published Cas9 benchmarks (typically 70-75% efficiency)."
        ),
        data_files=[
            "editing_efficiency.csv",
            "protein_knockout.png",
            "editing_percentages.png",
            "off_target_analysis.csv"
        ]
    ):
        if update["type"] == "text":
            print(update["content"], end="", flush=True)
        elif update["type"] == "progress":
            print(f"[{update['stage']}] {update['message']}")
        elif update["type"] == "result":
            print(f"✓ PDF: {update['files']['pdf_final']}")
            print(f"  Figures: {len(update['files']['figures'])} included")

asyncio.run(main())
```

## 🎯 Use as a Claude Code Plugin (Recommended)

**Scientific Writer works best as a Claude Code (Cursor) plugin**, providing seamless access to all scientific writing capabilities directly in your IDE. No CLI required!

### Quick Start - Plugin Installation

1. **Add the plugin marketplace** in Claude Code:
   ```bash
   /plugin marketplace add https://github.com/K-Dense-AI/claude-scientific-writer
   ```

2. **Install the plugin**:
   ```bash
   /plugin install claude-scientific-writer
   ```

3. **Restart Claude Code** when prompted.

4. **Initialize in your project**:
   ```bash
   /claude-scientific-writer:scientific-writer-init
   ```
   This creates a `CLAUDE.md` file with comprehensive scientific writing instructions and makes all 26 selected skills available.

5. **Start using immediately**:
   ```bash
   # Create papers with data and figures
   > Create a Nature paper on CRISPR gene editing. Present knockout_efficiency.csv 
     (5 cell lines tested), include Western blot (protein_levels.png) and flow 
     cytometry data (editing_rates.png). Highlight 87% efficiency in HEK293 cells.
   
   > Write an NSF grant proposal for quantum computing. Present preliminary results 
     from gate_fidelity.csv (99.2% fidelity), include circuit_diagram.png and 
     error_analysis.png. Compare to state-of-art 95% baseline.
   
   > Generate conference poster. Feature results from clinical_trial.csv 
     (n=150), survival_curves.png, biomarker_heatmap.png, and mechanism_diagram.svg.
   
   # Use specific skills with research data
   > @research-lookup Find papers on mRNA vaccine efficacy (2022-2024). Compare 
     with our trial_data.csv showing 94% efficacy and antibody_titers.xlsx.
   
   > @peer-review Evaluate this manuscript. Reference sample size in methods.csv 
     (n=30) and effect_sizes.png. Assess if statistical power is adequate.
   
   > @clinical-reports Create case report for autoimmune disorder. Include patient_labs.xlsx 
     (6 months data), MRI_scans/ folder, treatment_timeline.csv showing response.
   ```

### Why Use the Plugin?

- ✅ **No CLI Required** - Everything works directly in Claude Code
- ✅ **Instant Access** - All 26 selected skills available immediately
- ✅ **IDE Integration** - Files created and edited in your project
- ✅ **Context Aware** - Skills understand your project structure
- ✅ **Seamless Workflow** - No switching between tools

### Available Skills

When installed as a plugin, you get instant access to a reproducible subset of [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills), pinned in `skills.lock.json`:
- `scientific-schematics` - AI diagram generation with Nano Banana 2 (CONSORT, neural networks, pathways)
- `research-lookup` - Real-time literature search
- `peer-review` - Systematic manuscript evaluation
- `citation-management` - BibTeX and reference handling
- `clinical-reports` - Medical documentation standards
- `research-grants` - NSF, NIH, DOE proposal support
- `scientific-slides` - Research presentations
- `latex-posters` - Conference poster generation
- `hypothesis-generation` - Scientific hypothesis development
- `market-research-reports` - Comprehensive 50+ page market analysis reports with visuals
- And 16 more specialized skills...

For local plugin development and testing, see the [Development Guide](docs/DEVELOPMENT.md#plugin-development).

## Features

### 📝 Document Generation
- **Scientific papers** with IMRaD structure (Nature, Science, NeurIPS, etc.)
- **Clinical reports** (case reports, diagnostic reports, trial reports, patient documentation)
- **Research posters** using LaTeX (beamerposter, tikzposter, baposter)
- **Grant proposals** (NSF, NIH, DOE, DARPA) with agency-specific formatting
- **Literature reviews** with systematic citation management
- **Scientific schematics** powered by Nano Banana 2 (CONSORT diagrams, neural architectures, biological pathways, circuit diagrams)

### 🤖 AI-Powered Capabilities
- **Real-time research lookup** powered by Parallel Search and Extract
- **AI-powered diagram generation** - create scientific diagrams from natural-language descriptions
- **Intelligent paper detection** - automatically identifies references to existing papers
- **Peer review feedback** with quantitative ScholarEval framework (8-dimension scoring)
- **Iterative editing** with context-aware revision suggestions

### 🔧 Developer-Friendly
- **Programmatic API** - Full async Python API with type hints
- **CLI interface** - Interactive command-line tool with progress tracking
- **Progress streaming** - Real-time updates during generation
- **Comprehensive results** - JSON output with metadata, file paths, citations

### 📦 Data & File Integration
- **Automatic data handling** - Drop files in `data/`, auto-sorted to `figures/` or `data/`
- **Document conversion** - PDF, DOCX, PPTX, XLSX to Markdown with MarkItDown
- **Bibliography management** - Automatic BibTeX generation and citation formatting
- **Figure integration** - Images automatically referenced and organized

## Typical Workflow

### CLI Usage
1. Place figures and data in `data/` at the project root (images → `figures/`, files → `data/` automatically)
2. Run `scientific-writer` and describe what you want
3. Follow progress updates; outputs saved to `writing_outputs/<timestamp>_<topic>/`

```bash
# Start a new paper with figures and data
> Create a Nature paper on CRISPR gene editing. Include experimental_results.csv showing knockout efficiency across 5 cell lines. Reference figure1.png (Western blot) and figure2.png (flow cytometry data) in the results section. Discuss the 87% efficiency improvement observed in HEK293 cells.

# Continue editing with additional research results
> Add a methods section describing the experimental setup used to generate the data in results_table.csv. Reference the protocols for transfection, selection, and validation shown in microscopy_images/ folder.

# Grant proposal with preliminary data
> Write an NSF proposal for quantum computing research. Present preliminary results from quantum_fidelity.csv showing 99.2% gate fidelity. Include circuit_diagram.png and error_rates.png figures. Emphasize the breakthrough results compared to current state-of-art (95% fidelity).

# Research poster with comprehensive figures
> Generate a conference poster from my paper. Feature dose_response_graph.png as the central figure. Include mechanism_schematic.png, compare_treatments.png, and statistical_analysis.png. Highlight the p<0.001 significance for the primary outcome shown in the results.

# Clinical case report with patient data
> Create a clinical case report for rare disease presentation. Reference patient_timeline.csv showing symptom progression over 6 months. Include diagnostic_images/ (CT scans, MRI). Discuss lab_values.xlsx showing elevated biomarkers and treatment response documented in follow_up_data.csv.

# Literature review with meta-analysis
> Create a literature review on machine learning in healthcare. Reference the comparison in studies_comparison.csv covering 50 papers. Include forest_plot.png showing pooled effect sizes and quality_assessment.png from bias analysis. Synthesize the findings showing diagnostic accuracy (AUC 0.89), treatment prediction (accuracy 82%), and risk stratification results.
```

### API Usage
```python
import asyncio
from scientific_writer import generate_paper

async def main():
    async for update in generate_paper(
        query="Create a NeurIPS paper on transformers",
        data_files=["results.csv", "figure.png"],
        output_dir="./my_papers",
        track_token_usage=True  # Optional: track token consumption
    ):
        if update["type"] == "text":
            print(update["content"], end="", flush=True)
        elif update["type"] == "progress":
            print(f"[{update['stage']}] {update['message']}")
        elif update["type"] == "result":
            print(f"✓ PDF: {update['files']['pdf_final']}")
            # Token usage available when track_token_usage=True
            if "token_usage" in update:
                print(f"  Tokens used: {update['token_usage']['total_tokens']:,}")

asyncio.run(main())
```

## Quick Reference

### Common Commands

| Task | Command Example |
|------|----------------|
| **Scientific Paper** | `> Create a Nature paper on CRISPR gene editing. Present knockout efficiency data from results.csv (5 cell lines tested). Include Western blot (figure1.png) and flow cytometry (figure2.png) showing 87% efficiency in HEK293 cells. Compare with published benchmarks.` |
| **Clinical Report** | `> Create a clinical case report for rare mitochondrial disease. Include patient_timeline.csv (6-month progression), diagnostic_scans/ folder (MRI, CT images), and lab_values.xlsx showing elevated lactate (8.2 mmol/L) and creatine kinase (450 U/L). Describe treatment response.` |
| **Grant Proposal** | `> Write an NSF proposal for quantum error correction research. Present preliminary data from gate_fidelity.csv showing 99.2% fidelity (vs 95% state-of-art). Include circuit_topology.png, error_rates_comparison.png, and scalability_projections.csv for 100-qubit systems.` |
| **Research Poster** | `> Generate an A0 conference poster. Highlight findings from efficacy_study.csv (n=150 patients, 40% response rate). Feature mechanism_diagram.png, survival_curves.png, biomarker_heatmap.png, and statistical_forest_plot.png (p<0.001 primary endpoint).` |
| **Literature Review** | `> Create a systematic review on AI in drug discovery. Reference studies_database.csv (127 papers, 2020-2024). Include success_rates_meta.png (pooled OR=2.3, 95% CI 1.8-2.9), publication_trends.png, and therapeutic_areas_breakdown.csv showing oncology dominance (45% of studies).` |
| **Peer Review** | `> Evaluate this manuscript using ScholarEval. Reference figures (power_analysis.png shows n=30, underpowered), review statistics in results_table.csv, assess methodology against CONSORT standards, verify citations match claims.` |
| **Hypothesis Paper** | `> Generate research hypotheses on aging interventions. Reference transcriptomics_data.csv (15,000 genes across tissues), pathway_enrichment.png, and longevity_correlations.csv. Propose 5 testable hypotheses linking NAD+ metabolism, senescence, and lifespan extension.` |
| **Continue Editing** | `> Add methods section describing the protocols used to generate binding_assay.csv data. Include equipment specs, statistical tests used (t-tests in stats_summary.csv), and sample size justification from power_calculation.xlsx` |
| **Find Existing Paper** | `> Find the CRISPR paper and add discussion of limitations shown in off_target_analysis.csv and efficiency_variation.png across different cell types` |

### Research Lookup Examples

```bash
# Recent research with data integration (auto-triggers research lookup)
> Create a paper on recent advances in quantum computing (2024). Compare published values with our gate_fidelity_results.csv (99.2% for 2-qubit gates). Include our error_correction_benchmarks.png and cite papers achieving >98% fidelity.

# Fact verification with experimental context
> What are the current success rates for CAR-T therapy in B-cell lymphoma? Compare with our clinical_trial_outcomes.csv (n=45 patients, 62% complete response). How do our results compare to published JULIET and ZUMA trials?
```

### File Handling

```bash
# 1. Drop all your research files in the data/ folder at the project root
cp experimental_data.csv western_blot.png statistical_summary.xlsx ~/Documents/claude-scientific-writer/data/

# 2. Files are automatically sorted by type:
#    Images (png, jpg, svg, tif, pdf figures) → figures/
#    Data files (csv, json, txt, xlsx, tsv) → data/
#    Documents (pdf, docx, pptx) → converted to markdown

# 3. Reference files (or whole folders) explicitly in your prompt with specific details
> Create a NeurIPS paper on deep learning optimization. Include training_curves.csv showing convergence after 50 epochs, accuracy_comparison.png (our method: 94.2% vs baseline: 89.1%), and architecture_diagram.svg in methods.
```

For more extensive API examples (multiple data files, clinical trial reports, token tracking), see the [API Reference](docs/API.md).

## Plugin Testing (Local Development)

For developers working on the plugin or testing it locally, see the [Development Guide](docs/DEVELOPMENT.md#plugin-development), which covers setting up a local test marketplace, installing the plugin from a local checkout, verifying the plugin structure, and troubleshooting installation issues.

## 📄 Example Outputs

Want to see what Scientific Writer can create? Check out real examples in the [`docs/examples/`](docs/examples/) directory!

| Document Type | Example | Description |
|--------------|---------|-------------|
| **Research Paper** | Coming soon | Full scientific papers with IMRaD structure |
| **Grant Proposal** | [NSF Proposal](docs/examples/grants/NSF_draft1.pdf) | Complete NSF grant with budget and timeline |
| **Research Poster** | [Conference Poster](docs/examples/poster/poster.pdf) | LaTeX-generated academic poster |
| **Presentation Slides** | [AI Scientist Talk](docs/examples/slides/ai_scientist_talk.pdf) | Professional research presentation |
| **Clinical Report** | [Treatment Plan](docs/examples/treatment_plan/GERD.pdf) | Patient treatment documentation |
| **Clinical Decision Support** | [Breast Cancer](docs/examples/clinical_decision_support/breast_cancer.pdf) | Evidence-based clinical recommendations |
| **Hypothesis Generation** | [AI Weather Prediction](docs/examples/hypotheses_generation/AI_in_weather.pdf) | Research hypothesis development |
| **Market Research** | [Agentic AI Report](docs/examples/market%20research%20reports/agentic_ai_life_sciences.pdf) | Industry analysis and market insights |

**🎯 Browse the examples** to see formatting, structure, and quality before starting your own projects!

## Documentation

### User Guides
- [📖 Complete Features Guide](docs/FEATURES.md) - Comprehensive overview of all capabilities
- [🔧 API Reference](docs/API.md) - Full programmatic API documentation
- [🎯 Skills Overview](docs/SKILLS.md) - All available skills and tools
- [🐛 Troubleshooting](docs/TROUBLESHOOTING.md) - Common issues and solutions

### Developer Resources
- [🤝 Contributing Guide](CONTRIBUTING.md) - Dev setup, tests, and PR guidelines
- [💻 Development Guide](docs/DEVELOPMENT.md) - Architecture and plugin development
- [🛠️ Skill Authoring Guide](docs/SKILL_AUTHORING.md) - How to write and register a new skill
- [📦 Releasing Guide](docs/RELEASING.md) - Versioning and publishing
- [📋 Release Notes](CHANGELOG.md) - Version history and updates
- [🔌 Agent Plugins Support](docs/AGENT_PLUGINS.md) - Using and validating this repo as a portable Agent Plugin
- [🤖 System Instructions](CLAUDE.md) - Agent instructions (advanced), mirrored to [AGENTS.md](AGENTS.md)
- [📝 Zotero DOCX Extension](extensions/docx-editor-zotero/README.md) - Optional citation-preserving Word workflow

## Use with Antigravity, Pi, and Other Agents

This repository is a conformant [Agent Plugins](https://agent-plugins.org/) 1.0.0 package, the
vendor-neutral standard for packaging [Agent Skills](https://agentskills.io/specification) and MCP
servers. Its skills follow the Agent Skills format, so they load in Claude Code and in any other
Agent Plugins client without modification.

### Agent Plugins clients (recommended)

Point your client at any of these plugin roots — each has a `plugin.json` manifest and a `skills/`
directory:

```bash
# From a checkout
git clone https://github.com/K-Dense-AI/claude-scientific-writer.git

# Or from the published package — the installed payload is a plugin root too
pip install scientific-writer
python -c "import scientific_writer, pathlib; print(pathlib.Path(scientific_writer.__file__).parent / '.claude')"
```

Project instructions are available under both filenames: `CLAUDE.md` and the byte-identical
`AGENTS.md`. Running `/claude-scientific-writer:scientific-writer-init` writes both into your
project, and the CLI reads instructions from `.claude/` or `.agents/` — see
[docs/AGENT_PLUGINS.md](docs/AGENT_PLUGINS.md) for the full lookup order and how to validate a plugin
root with `scripts/validate_agent_plugin.py`.

### Manual approach

For an agent that does not load Agent Plugins packages (Antigravity, Pi, Aider, Continue, etc.), load a single skill by hand:

1. Open the relevant `skills/<skill-name>/SKILL.md` file.
2. Copy the content below the YAML frontmatter (everything after the closing `---`).
3. Paste it into your agent's system prompt, custom instructions file, or equivalent configuration.

Most agents read `AGENTS.md` from the project root, so appending the skill body there is usually enough:

```bash
# Append the scientific-writing skill (frontmatter stripped) to the project's AGENTS.md
awk 'f; /^---$/ && NR>1 {f=1}' skills/scientific-writing/SKILL.md >> AGENTS.md
```

### Claude Code-specific features

The following SKILL.md frontmatter fields are Claude Code-specific and can be safely ignored by other agents:

| Field | Claude Code behaviour | Other agents |
|-------|-----------------------|--------------|
| `allowed-tools` | Restricts which tools the agent may call; written as a space-separated string (e.g. `allowed-tools: Read Write Edit Bash`) | Ignore or map to your agent's tool-permission system |
| `hooks` | Runs shell commands before/after skill execution | Ignore or implement equivalent pre/post hooks manually |
| `version` | Used by Claude Code marketplace | Informational only |

All skill *content* (instructions, workflows, code examples) is agent-agnostic and works with any sufficiently capable LLM.

## Versioning and Publishing (short)
Use `uv` and the helper scripts:
- Bump version (keeps pyproject + __init__ in sync): `uv run scripts/bump_version.py [patch|minor|major]`
- Build and publish: `uv run scripts/publish.py` (or `--bump patch|minor|major`)
See [docs/RELEASING.md](docs/RELEASING.md) for prerequisites, dry runs, tagging, and verification.

## Migration

### v1.x -> v2.0
- CLI remains unchanged (scientific-writer).
- New programmatic API: from scientific_writer import generate_paper.
- Legacy single-file script is replaced by a proper package; no action needed for CLI users.

### Research backend (v2.13+)
- Research lookup, web search, and deep research use Parallel Search, Extract, and Research through `parallel-cli`. Authenticate with `parallel-cli login` or set `PARALLEL_API_KEY`.
- `OPENROUTER_API_KEY` is not used by the default research path. It remains optional for image-generation skills and explicitly requested Perplexity fallback research.

## License
MIT - see LICENSE.

## Support
- Open an issue on GitHub
- See [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for common problems

## 💬 Join Our Community!

**Follow us for updates:** [X](https://x.com/k_dense_ai) · [LinkedIn](https://www.linkedin.com/company/k-dense-inc) · [YouTube](https://www.youtube.com/@K-Dense-Inc)

**Want to connect with other researchers, share tips, and get help in real-time?** Join our vibrant Slack community! 🎉

Whether you're writing your first paper, exploring advanced features, or just want to chat about scientific writing and AI, we'd love to have you! Get faster support, share your success stories, and collaborate with fellow users.

👉 **[Join the K-Dense Community on Slack](https://join.slack.com/t/k-densecommunity/shared_invite/zt-3iajtyls1-EwmkwIZk0g_o74311Tkf5g)** 👈

We're excited to meet you! 🚀

## ⭐ Show Your Support

If you find this project helpful for your research or work, please consider giving it a star on GitHub! It helps others discover the tool and motivates continued development. Thank you! 🙏

![GitHub stars](https://img.shields.io/github/stars/K-Dense-AI/claude-scientific-writer?style=social)
