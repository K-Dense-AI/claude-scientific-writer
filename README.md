# Claude Scientific Writer

A powerful command-line tool for scientific writing powered by Claude Sonnet 4.5 and the Claude Agents SDK. This tool provides specialized assistance for writing scientific papers, conducting literature reviews, peer review, and real-time research lookup.

## Features

- 🔬 **Scientific Writing**: Generate complete scientific papers following IMRaD structure with proper citations and formatting
- 📚 **Literature Review**: Conduct comprehensive literature reviews with citation management
- 🔍 **Research Lookup**: Real-time research information using Perplexity's Sonar Pro model via OpenRouter
- 📝 **Peer Review**: Receive constructive feedback on scientific drafts
- 📄 **Document Manipulation**: Work with various document formats (docx, pdf, pptx, xlsx)
- 🤖 **LaTeX Support**: Generates publication-ready LaTeX documents with BibTeX citations
- 📊 **Progress Tracking**: Real-time logging and transparent workflow execution

## Quick Start

### Prerequisites

- Python 3.10 or later
- An [Anthropic API key](https://console.anthropic.com/)
- An [OpenRouter API key](https://openrouter.ai/) (for research lookup functionality)

### Installation

1. **Clone this repository:**
   ```bash
   git clone https://github.com/yourusername/claude-scientific-writer.git
   cd claude-scientific-writer
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or use the setup script:
   ```bash
   bash setup.sh
   ```

3. **Set up your API keys:**

   Create a `.env` file in the project root:
   ```bash
   echo "ANTHROPIC_API_KEY=your_anthropic_api_key_here" > .env
   echo "OPENROUTER_API_KEY=your_openrouter_api_key_here" >> .env
   ```

   Or export them in your shell:
   ```bash
   export ANTHROPIC_API_KEY='your_anthropic_api_key_here'
   export OPENROUTER_API_KEY='your_openrouter_api_key_here'
   ```

### Usage

Run the scientific writer CLI:

```bash
python scientific_writer.py
```

## How It Works

### Workflow

1. **You Make a Request**: Describe what you need (e.g., "Create a NeurIPS paper on transformer attention")
2. **Brief Plan & Execution**: The assistant presents a plan and immediately starts working
3. **Real-Time Updates**: Continuous progress updates throughout execution
4. **Organized Output**: All files saved to `paper_outputs/<timestamp>_<description>/`

### Output Structure

```
paper_outputs/20241027_143022_neurips_attention/
├── progress.md              # Real-time progress log
├── SUMMARY.md               # Final summary and instructions
├── drafts/
│   ├── v1_draft.tex        # LaTeX source
│   ├── v1_draft.pdf        # Compiled PDF
│   └── v2_draft.tex        # Revised version
├── references/
│   └── references.bib      # BibTeX bibliography
├── figures/
│   └── figure_01.pdf
├── data/
└── final/
    ├── manuscript.pdf      # Final compiled PDF
    └── manuscript.tex      # Final LaTeX source
```

## Example Use Cases

### Writing a Scientific Paper

```
> Create a NeurIPS paper on efficient attention mechanisms in transformers
```

The assistant will:
- Create a complete LaTeX document following NeurIPS format
- Perform literature research for each section
- Write Introduction, Methods, Results, Discussion sections
- Generate proper BibTeX citations
- Compile to PDF
- Provide real-time progress updates

### Literature Review

```
> Conduct a literature review on CRISPR applications in agriculture
```

### Research Lookup

```
> Research the latest developments in quantum computing from 2024
```

### Peer Review

```
> Review my methods section in draft.txt and provide constructive feedback
```

### Citation Formatting

```
> Format these 10 citations in IEEE style: [paste citations]
```

## Available Skills

The CLI comes with specialized skills loaded from `.claude/skills/`:

### Scientific Writing
- IMRaD structure guidance
- Citation styles (APA, MLA, Chicago, Nature, IEEE, etc.)
- Figures and tables best practices
- Reporting guidelines for various study types

### Literature Review
- Database search strategies
- Citation management and verification
- Review template generation

### Peer Review
- Common issues identification
- Reporting standards verification
- Constructive feedback generation

### Research Lookup
- Real-time research using Perplexity Sonar Pro
- Automatic citation of sources
- Current literature access

### Document Skills
- **DOCX**: Create and edit Word documents
- **PDF**: Extract information, fill forms
- **PPTX**: Create and modify PowerPoint presentations
- **XLSX**: Work with Excel spreadsheets

For detailed skill documentation, see [SKILLS.md](SKILLS.md).

## Commands

- **Regular prompts**: Type your request and press Enter
- **`help`**: Display usage tips and examples
- **`exit` or `quit`**: End the session

## Tips for Best Results

1. **Be specific**: Mention the target journal/conference (e.g., "Nature", "NeurIPS")
2. **Provide context**: Include field of study, specific requirements, page limits
3. **Specify format**: Citation style preferences, document format
4. **Iterate**: Ask for revisions or clarifications as needed
5. **Use files**: Reference existing files for review or editing tasks

## Configuration

### Permission Modes

The tool uses `bypassPermissions` mode by default, which means:
- ✅ Brief plan shown before execution
- ✅ Immediate execution without approval delays
- ✅ Continuous progress updates
- ✅ Can interrupt with Ctrl+C if needed

To change permission modes, edit `scientific_writer.py` line 81:

```python
permission_mode="bypassPermissions"  # Options: "bypassPermissions", "acceptEdits", "default"
```

### System Instructions

The agent's behavior is defined in `claude.md`, which includes:
- Workflow protocols
- File organization standards
- Progress logging requirements
- Quality checklists

Modify this file to customize the agent's behavior.

## Project Structure

```
claude-scientific-writer/
├── .claude/
│   └── skills/                  # Specialized skills
│       ├── scientific-writing/
│       ├── literature-review/
│       ├── peer-review/
│       ├── research-lookup/
│       └── document-skills/
├── paper_outputs/               # Generated papers (auto-created)
├── scientific_writer.py         # Main CLI application
├── requirements.txt             # Python dependencies
├── setup.sh                     # Setup script
├── claude.md                    # System instructions
├── SKILLS.md                    # Detailed skills documentation
├── .env                         # API keys (create this)
└── README.md                    # This file
```

## Troubleshooting

### API Key Issues

If you see an error about missing API key:
```
Error: ANTHROPIC_API_KEY environment variable not set.
```

Make sure you've either:
1. Created a `.env` file with your API keys, or
2. Exported the environment variables in your shell

### Import Errors

Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Permission Errors

Check:
1. File permissions
2. Files aren't locked by other applications
3. You're running from the correct directory

### LaTeX Compilation Issues

If PDF generation fails:
1. Ensure you have a LaTeX distribution installed (TeX Live, MiKTeX)
2. Check `progress.md` for specific error messages
3. The `.tex` source file is always created even if PDF compilation fails

## Contributing

Contributions are welcome! To add or modify skills:

1. Navigate to `.claude/skills/`
2. Add or modify skill directories with `SKILL.md` files
3. The agent will automatically load them on next run

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with the [Claude Agents SDK](https://docs.claude.com/en/docs/claude-code/sdk/sdk-overview)
- Powered by Anthropic's Claude Sonnet 4.5
- Research lookup powered by Perplexity Sonar Pro via OpenRouter

## Support

For issues or questions:
- Open an issue on GitHub
- Check the [SKILLS.md](SKILLS.md) documentation
- Review `progress.md` files in your paper outputs for debugging

## Example Session

```
> Create a NeurIPS paper on sparse attention mechanisms

I'll create a complete NeurIPS conference paper on sparse attention mechanisms...

APPROACH:
- Format: LaTeX (using NeurIPS template)
- Structure: IMRaD with 8-page format
- Citations: BibTeX with ~30-40 references
- Style: NeurIPS citation style

OUTPUT: paper_outputs/20241027_143022_neurips_sparse_attention/

Starting execution now...

[14:30:22] STARTING: NeurIPS sparse attention paper
[14:30:23] CREATED: paper_outputs/20241027_143022_neurips_sparse_attention/
[14:30:24] CREATED: Folder structure (drafts/, references/, figures/, final/)
[14:30:25] CREATED: LaTeX document skeleton
[14:30:45] RESEARCH: Literature search for Introduction
[14:31:30] WRITING: Introduction section...
[14:33:15] COMPLETED: Introduction - 750 words, 6 citations ✅
...
[14:51:18] COMPILE: Build successful - no errors ✅
[14:51:40] ✅ PROJECT COMPLETE

All files available in: paper_outputs/20241027_143022_neurips_sparse_attention/
```

---

**Ready to revolutionize your scientific writing workflow? Get started now!**
