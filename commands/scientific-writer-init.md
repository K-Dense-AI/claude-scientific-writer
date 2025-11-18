---
description: Initialize the current project to use the Scientific Writer CLAUDE.md configuration.
---

# Scientific Writer Project Setup

When the user runs `/scientific-writer:init`, do the following:

## Step 1: Check for Existing CLAUDE.md

1. Check if a `CLAUDE.md` file exists in the current working directory.
   
2. If it exists:
   - Ask the user whether to:
     - a) **Back up** the existing file as `CLAUDE.md.bak` and replace it with the Scientific Writer configuration, or
     - b) **Merge** the Scientific Writer settings into the existing file (append to end), or
     - c) **Cancel** the operation.
   
3. Wait for user response before proceeding.

## Step 2: Locate the Template

First, find the Scientific Writer template file. Try these methods in order:

1. Search for the template file in the plugin directory:
   - Look in the claude-scientific-writer plugin's `templates/` directory
   - File name: `CLAUDE.scientific-writer.md`
   - Full path should be: `{plugin_dir}/templates/CLAUDE.scientific-writer.md`

2. If search fails, try these paths:
   - `/Users/vinayak/Documents/claude-scientific-writer/templates/CLAUDE.scientific-writer.md`
   - Or search the plugins directory: `~/.claude/plugins/*/claude-scientific-writer/templates/CLAUDE.scientific-writer.md`

## Step 3: Create or Update CLAUDE.md

Based on the user's choice (or create new if no existing file):

### Option A: Replace (with backup)
- Rename existing `CLAUDE.md` to `CLAUDE.md.bak`
- Copy the template file to `CLAUDE.md` in the project root (use terminal `cp` command)
- Print: "✅ Backed up existing CLAUDE.md to CLAUDE.md.bak and created new Scientific Writer configuration"

### Option B: Merge
- Append a separator to existing `CLAUDE.md` using `echo`:
  ```bash
  echo -e "\n\n---\n\n# Scientific Writer Configuration (Added by Plugin)\n" >> CLAUDE.md
  ```
- Append the template file contents using `cat`:
  ```bash
  cat {template_path} >> CLAUDE.md
  ```
- Print: "✅ Merged Scientific Writer configuration into existing CLAUDE.md"

### Option C: Create New (Default)
If no existing file:
- Copy the template file to `CLAUDE.md` in the project root (use terminal `cp` command)
- Print: "✅ Created CLAUDE.md with Scientific Writer configuration"

## Step 4: Summarize What Was Installed

After writing the file, provide a brief summary:

```
🎉 Scientific Writer has been initialized in this project!

📋 What's Included:
- Complete scientific writing workflow and standards
- 19+ specialized skills for academic writing:
  • research-lookup: Real-time literature search
  • peer-review: Systematic manuscript evaluation
  • citation-management: BibTeX and reference handling
  • clinical-reports: Medical documentation standards
  • research-grants: NSF, NIH, DOE proposal support
  • scientific-slides: Research presentations
  • latex-posters: Conference poster generation
  • And 12 more specialized skills...

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
- All 19 skills are now available for use in this project
- They can ask "What skills are available?" to see the full list
- They can reference specific skills like "@research-lookup" in their prompts

## Error Handling

If any errors occur during file creation:
- Report the specific error to the user
- Suggest manual steps (e.g., creating the file manually)
- Provide the template paths to try:
  - `/Users/vinayak/Documents/claude-scientific-writer/templates/CLAUDE.scientific-writer.md` (local dev)
  - `~/.claude/plugins/*/claude-scientific-writer/templates/CLAUDE.scientific-writer.md` (installed plugin)
- If template still can't be found, offer to create a basic CLAUDE.md with minimal scientific writing instructions

