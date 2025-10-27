# GitHub Setup Instructions

## Prerequisites
- You must have write access to the K-Dense-AI organization
- Git must be installed on your system

## Steps to Push to K-Dense-AI/claude-scientific-writer

### 1. Create the Repository on GitHub
1. Go to: https://github.com/organizations/K-Dense-AI/repositories/new
2. Repository name: `claude-scientific-writer`
3. Description: `AI-powered scientific writing assistant using Claude Sonnet 4.5. Generate research papers, conduct literature reviews, and get peer review feedback with real-time research lookup.`
4. Visibility: **Public**
5. **DO NOT** check "Initialize this repository with a README"
6. Click "Create repository"

### 2. Initialize and Push the Local Repository

```bash
# Navigate to the project directory
cd /Users/vinayak/Documents/claude-scientific-writer

# Initialize git repository (if not already done)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Claude Scientific Writer v1.0

- AI-powered scientific writing CLI tool
- Supports LaTeX, Word, and Markdown formats
- Real-time research lookup via Perplexity Sonar Pro
- Literature review and peer review capabilities
- Document manipulation (docx, pdf, pptx, xlsx)
- MIT License"

# Add the K-Dense-AI remote
git remote add origin https://github.com/K-Dense-AI/claude-scientific-writer.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

### 3. Configure Repository Settings (Optional)

After pushing, configure these settings on GitHub:

#### Topics/Tags
Add these topics to help with discoverability:
- `scientific-writing`
- `ai`
- `claude`
- `anthropic`
- `research`
- `latex`
- `literature-review`
- `python`
- `cli-tool`
- `peer-review`
- `academic-writing`

#### About Section
Short description: "AI-powered scientific writing assistant with LaTeX support, literature review, and real-time research lookup"

Website: (optional) Link to documentation or demo

#### Social Preview Image
Consider creating a social preview image (1280x640px) showing the CLI in action

### 4. Verify the Push

After pushing, verify:
- [ ] All files are visible on GitHub
- [ ] README.md displays correctly on the repository homepage
- [ ] LICENSE file is recognized (should show "MIT License" badge)
- [ ] .gitignore is working (no `__pycache__`, `.env`, or `paper_outputs/` in the repo)

### 5. Optional: Create a Release

Create your first release:
1. Go to: https://github.com/K-Dense-AI/claude-scientific-writer/releases/new
2. Tag version: `v1.0.0`
3. Release title: `v1.0.0 - Initial Release`
4. Description: 
   ```
   🎉 First public release of Claude Scientific Writer!
   
   ## Features
   - AI-powered scientific writing with Claude Sonnet 4.5
   - LaTeX document generation with BibTeX citations
   - Real-time research lookup via Perplexity Sonar Pro
   - Literature review and peer review capabilities
   - Document manipulation (DOCX, PDF, PPTX, XLSX)
   - Transparent workflow with real-time progress tracking
   
   ## Quick Start
   See README.md for installation and usage instructions.
   ```
5. Click "Publish release"

## Troubleshooting

### If you get "remote already exists" error:
```bash
git remote remove origin
git remote add origin https://github.com/K-Dense-AI/claude-scientific-writer.git
```

### If you need to force push (use with caution):
```bash
git push -f origin main
```

### If you're using SSH instead of HTTPS:
```bash
git remote add origin git@github.com:K-Dense-AI/claude-scientific-writer.git
```

## Repository URL
After setup, your repository will be available at:
https://github.com/K-Dense-AI/claude-scientific-writer

