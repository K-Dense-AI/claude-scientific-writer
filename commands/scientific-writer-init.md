---
description: Initialize the current project with Scientific Writer - a deep research and writing tool that combines AI-driven research with well-formatted written outputs.
---

# Scientific Writer Project Setup

When the user runs `/claude-scientific-writer:scientific-writer-init`, do the following:

## ⚠️ CRITICAL RULE: NEVER READ THE TEMPLATE FILE

**Throughout this entire process, you must NEVER use the read_file tool on the template file. The template file is very long and reading it wastes time and tokens. Only use terminal commands (`cp`, `cat`, `mv`) to handle the file.**

## Step 1: Check for Existing CLAUDE.md

1. Check if a `CLAUDE.md` file exists in the current working directory.
   
2. If it exists:
   - Ask the user whether to:
     - a) **Back up** the existing file as `CLAUDE.md.bak` and replace it with the Scientific Writer configuration, or
     - b) **Merge** the Scientific Writer settings into the existing file (append to end), or
     - c) **Cancel** the operation.
   
3. Wait for user response before proceeding.

## Step 2: Locate the Template File Path

**CRITICAL: Do NOT use the read_file tool. Do NOT read the template contents. Only locate the file path.**

Find the path to the Scientific Writer template file. Use one of these methods:

1. **Use glob_file_search** to find `CLAUDE.scientific-writer.md` in the templates directory
2. **Use list_dir** to check if the file exists in known locations
3. **Directly try these paths** (in order):
   - `~/.claude/plugins/*/claude-scientific-writer/templates/CLAUDE.scientific-writer.md` (installed plugin)
   - `<path-to-claude-scientific-writer-checkout>/templates/CLAUDE.scientific-writer.md` (local development)

Once you have the path, immediately proceed to Step 3. **Do NOT read or verify the file contents.**

## Step 3: Create or Update CLAUDE.md

**All options below must use terminal commands only. Do NOT read the template file contents.**

Based on the user's choice (or create new if no existing file):

### Option A: Replace (with backup)
Use terminal commands to:
1. Rename existing `CLAUDE.md` to `CLAUDE.md.bak`:
   ```bash
   mv CLAUDE.md CLAUDE.md.bak
   ```
2. Copy the template file to `CLAUDE.md`:
   ```bash
   cp {template_path} CLAUDE.md
   ```
3. Print: "✅ Backed up existing CLAUDE.md to CLAUDE.md.bak and created new Scientific Writer configuration"

### Option B: Merge
Use terminal commands to:
1. Append a separator to existing `CLAUDE.md`:
   ```bash
   echo -e "\n\n---\n\n# Scientific Writer Configuration (Added by Plugin)\n" >> CLAUDE.md
   ```
2. Append the template file contents directly (without reading):
   ```bash
   cat {template_path} >> CLAUDE.md
   ```
3. Print: "✅ Merged Scientific Writer configuration into existing CLAUDE.md"

### Option C: Create New (Default)
If no existing file, use terminal command to:
1. Copy the template file to `CLAUDE.md`:
   ```bash
   cp {template_path} CLAUDE.md
   ```
2. Print: "✅ Created CLAUDE.md with Scientific Writer configuration"

## Step 4: Summarize What Was Installed

After writing the file, provide a brief summary:

```
🎉 Scientific Writer has been initialized in this project!

📋 What's Included:
- A deep research and writing tool that combines AI-driven research with well-formatted written outputs
- Complete scientific writing workflow with real-time literature search and verified citations
- 25 specialized skills for academic writing:
  • research-lookup: Real-time literature search
  • peer-review: Systematic manuscript evaluation
  • citation-management: BibTeX and reference handling
  • clinical-reports: Medical documentation standards
  • research-grants: NSF, NIH, DOE proposal support
  • scientific-slides: Research presentations
  • latex-posters: Conference poster generation
  • And 18 more specialized skills...

📝 Document Types Supported:
- Scientific papers (Nature, Science, NeurIPS, IEEE, etc.)
- Clinical reports (case reports, trial documentation)
- Grant proposals (NSF, NIH, DOE, DARPA)
- Research posters and presentations
- Literature reviews and systematic reviews

🚀 Getting Started:
1. Your CLAUDE.md file is now configured at: {path to CLAUDE.md}
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
- You can edit the CLAUDE.md file to customize behavior

📚 Documentation:
- Skill details: Browse the skills/ directory
- Full docs: https://github.com/K-Dense-AI/claude-scientific-writer

Happy writing! 🔬📄
```

## Step 5: Final Reminders

Remind the user:
- The `CLAUDE.md` file can be opened and edited manually at any time
- All 26 selected skills are now available for use in this project
- They can ask "What skills are available?" to see the full list
- They can reference specific skills like "@research-lookup" in their prompts

## Error Handling

If any errors occur during file creation:
- Report the specific error to the user
- Suggest manual steps (e.g., creating the file manually)
- Provide the template paths to try:
  - `~/.claude/plugins/*/claude-scientific-writer/templates/CLAUDE.scientific-writer.md` (installed plugin)
  - `<path-to-claude-scientific-writer-checkout>/templates/CLAUDE.scientific-writer.md` (local development)
- If template still can't be found, offer to create a basic CLAUDE.md with minimal scientific writing instructions

