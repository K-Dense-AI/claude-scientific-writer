---
description: Initialize the current project with Scientific Writer - a deep research and writing tool that combines AI-driven research with well-formatted written outputs.
---

# Scientific Writer Project Setup

When the user runs `/claude-scientific-writer:scientific-writer-init`, do the following:

## ⚠️ CRITICAL RULE: NEVER READ THE TEMPLATE FILE

**Throughout this entire process, you must NEVER use the read_file tool on a template file. The template files are very long and reading them wastes time and tokens. Only use terminal commands (`cp`, `cat`, `mv`) to handle them.**

## Instruction Files Installed

Scientific Writer configures **two** project instruction files so both Claude Code and other agent clients pick it up:

| Project file | Template |
|--------------|----------|
| `CLAUDE.md` | `CLAUDE.scientific-writer.md` |
| `AGENTS.md` | `AGENTS.scientific-writer.md` |

The two templates hold identical instructions; only the generated header differs. Steps 1 and 3 apply to **each** of these files independently.

## Step 1: Check for Existing Instruction Files

1. Check whether `CLAUDE.md` and/or `AGENTS.md` exist in the current working directory.

2. For each file that already exists:
   - Ask the user whether to:
     - a) **Back up** the existing file as `<FILE>.bak` and replace it with the Scientific Writer configuration, or
     - b) **Merge** the Scientific Writer settings into the existing file (append to end), or
     - c) **Skip** this file.
   - If both files exist, ask once and apply the same choice to both unless the user says otherwise.

3. If the user wants to cancel the whole operation, stop here.

4. Wait for user response before proceeding.

## Step 2: Locate the Template File Paths

**CRITICAL: Do NOT use the read_file tool. Do NOT read the template contents. Only locate the file paths.**

Find the paths to the Scientific Writer templates. Use one of these methods:

1. **Use glob_file_search** to find `CLAUDE.scientific-writer.md` and `AGENTS.scientific-writer.md` in the templates directory
2. **Use list_dir** to check if the files exist in known locations
3. **Directly try these paths** (in order):
   - `~/.claude/plugins/*/claude-scientific-writer/templates/` (installed plugin)
   - `<path-to-claude-scientific-writer-checkout>/templates/` (local development)

Once you have the paths, immediately proceed to Step 3. **Do NOT read or verify the file contents.**

If only `CLAUDE.scientific-writer.md` is present (an older install), use it for both `CLAUDE.md` and `AGENTS.md`.

## Step 3: Create or Update Each Instruction File

**All options below must use terminal commands only. Do NOT read the template file contents.**

Repeat for each pair of `{target}` (`CLAUDE.md`, `AGENTS.md`) and its `{template_path}`, using the user's choice from Step 1 (or create new if no existing file):

### Option A: Replace (with backup)
Use terminal commands to:
1. Rename the existing file:
   ```bash
   mv {target} {target}.bak
   ```
2. Copy the template file into place:
   ```bash
   cp {template_path} {target}
   ```
3. Print: "✅ Backed up existing {target} to {target}.bak and created new Scientific Writer configuration"

### Option B: Merge
Use terminal commands to:
1. Append a separator to the existing file:
   ```bash
   echo -e "\n\n---\n\n# Scientific Writer Configuration (Added by Plugin)\n" >> {target}
   ```
2. Append the template file contents directly (without reading):
   ```bash
   cat {template_path} >> {target}
   ```
3. Print: "✅ Merged Scientific Writer configuration into existing {target}"

### Option C: Create New (Default)
If the file does not exist, use terminal command to:
1. Copy the template file into place:
   ```bash
   cp {template_path} {target}
   ```
2. Print: "✅ Created {target} with Scientific Writer configuration"

## Step 4: Summarize What Was Installed

After writing the file, provide a brief summary:

```
🎉 Scientific Writer has been initialized in this project!

📋 What's Included:
- A deep research and writing tool that combines AI-driven research with well-formatted written outputs
- Complete scientific writing workflow with real-time literature search and verified citations
- 26 selected skills for academic writing:
  • research-lookup: Real-time literature search
  • peer-review: Systematic manuscript evaluation
  • citation-management: BibTeX and reference handling
  • clinical-reports: Medical documentation standards
  • research-grants: NSF, NIH, DOE proposal support
  • scientific-slides: Research presentations
  • latex-posters: Conference poster generation
  • And 19 more specialized skills...

📝 Document Types Supported:
- Scientific papers (Nature, Science, NeurIPS, IEEE, etc.)
- Clinical reports (case reports, trial documentation)
- Grant proposals (NSF, NIH, DOE, DARPA)
- Research posters and presentations
- Literature reviews and systematic reviews

🚀 Getting Started:
1. Your CLAUDE.md and AGENTS.md files are now configured at: {paths written}
2. All skills are automatically available in this project
3. Start with prompts like:
   - "Create a Nature paper on [topic]"
   - "Generate an NSF grant proposal for [research]"
   - "Review this manuscript using peer-review standards"
   - "Create conference slides on [topic]"

💡 Tips:
- The research-lookup skill automatically finds real papers and citations
- All documents default to LaTeX format (publication-ready)
- Peer review is conducted automatically after paper generation
- You can edit CLAUDE.md or AGENTS.md to customize behavior (keep them in sync)

📚 Documentation:
- Skill details: Browse the skills/ directory
- Full docs: https://github.com/K-Dense-AI/claude-scientific-writer

Happy writing! 🔬📄
```

## Step 5: Final Reminders

Remind the user:
- The `CLAUDE.md` and `AGENTS.md` files can be opened and edited manually at any time
- All 26 selected skills are now available for use in this project
- They can ask "What skills are available?" to see the full list
- They can reference specific skills like "@research-lookup" in their prompts

## Error Handling

If any errors occur during file creation:
- Report the specific error to the user
- Suggest manual steps (e.g., creating the file manually)
- Provide the template paths to try:
  - `~/.claude/plugins/*/claude-scientific-writer/templates/{CLAUDE,AGENTS}.scientific-writer.md` (installed plugin)
  - `<path-to-claude-scientific-writer-checkout>/templates/{CLAUDE,AGENTS}.scientific-writer.md` (local development)
- If the templates still can't be found, offer to create basic CLAUDE.md and AGENTS.md files with minimal scientific writing instructions

