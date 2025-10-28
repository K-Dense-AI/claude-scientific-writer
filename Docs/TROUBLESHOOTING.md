# Troubleshooting Guide

This document provides solutions to common issues you may encounter when using the Claude Scientific Writer.

## Table of Contents
- [Windows: Claude Code Not Found Error](#windows-claude-code-not-found-error)
- [API Key Issues](#api-key-issues)
- [Installation Problems](#installation-problems)
- [LaTeX Compilation Issues](#latex-compilation-issues)
- [General Issues](#general-issues)

---

## Windows: Claude Code Not Found Error

### Problem
When running the scientific writer on Windows, you may encounter this error:
```
Error: Claude Code not found at: C:\Users\<username>\AppData\Roaming\npm\claude.CMD Please try again or type 'exit' to quit.
```

Even if `claude.CMD` exists at the specified path and works when called directly, the `claude-agent-sdk` may fail to locate or execute it properly.

### Solutions

#### 1. Verify Claude Code CLI Installation
First, test if Claude Code works directly from your command prompt:
```cmd
claude
```

If this doesn't work, reinstall the Claude Code CLI:
```cmd
npm uninstall -g @anthropic-ai/claude-code
npm install -g @anthropic-ai/claude-code
```

#### 2. Check PATH Configuration
Verify that npm's global bin directory is in your system PATH:

```cmd
where claude
echo %PATH%
```

The output should include `C:\Users\<username>\AppData\Roaming\npm`. 

**To add npm to PATH (if missing):**
1. Press `Win + X` and select "System"
2. Click "Advanced system settings"
3. Click "Environment Variables"
4. Under "User variables" or "System variables", find "Path" and click "Edit"
5. Click "New" and add: `C:\Users\<username>\AppData\Roaming\npm`
6. Click "OK" to save

#### 3. Restart Your Terminal
After any PATH changes, **completely close and reopen** your command prompt or PowerShell window to reload environment variables.

#### 4. Run as Administrator
Windows permissions can sometimes interfere with `.CMD` file execution. Try running your terminal as Administrator:
1. Right-click on Command Prompt or PowerShell
2. Select "Run as administrator"
3. Navigate to your project directory
4. Run the scientific writer again

#### 5. Use Node.js Command Prompt
If you installed Node.js via the Windows installer, try using the "Node.js command prompt" that comes with it instead of the regular command prompt.

#### 6. Alternative: Windows Subsystem for Linux (WSL)
If the above steps don't resolve the issue, consider using [WSL](https://learn.microsoft.com/en-us/windows/wsl/install):

```bash
# In PowerShell (as Administrator)
wsl --install
```

Then install Node.js and the scientific writer within your WSL environment, where the Claude Code CLI typically has fewer compatibility issues.

#### 7. Try Using npx Directly
If Claude Code works from the command line but the SDK can't find it, try using `npx` to run it:

```cmd
npx @anthropic-ai/claude-code --version
```

If this works, you might have a PATH resolution issue specific to how Python/the SDK spawns processes.

#### 8. Check for Multiple Node.js Installations
Multiple Node.js installations can cause PATH conflicts:

```cmd
where node
where npm
npm config get prefix
```

If you see multiple paths, this might be causing the issue.

#### 9. Try a Virtual Environment
Create a fresh Python virtual environment to isolate the installation:

```cmd
python -m venv venv
venv\Scripts\activate
pip install -e .
```

Then run the scientific writer from within this virtual environment.

### Known Issue: SDK Compatibility on Windows (No Admin Rights)

**If you've confirmed:**
- ✅ `claude` works when called directly (`claude --version` shows version 2.0.28 or similar)
- ✅ npm global path is in your PATH (`C:\Users\<username>\AppData\Roaming\npm`)
- ✅ Package is installed correctly (`npm list -g @anthropic-ai/claude-code` shows it)
- ✅ Tried both CMD and PowerShell
- ❌ Don't have administrator rights to modify system settings

**This appears to be a Windows-specific issue with the `claude-agent-sdk` subprocess execution.**

The SDK may be using a process spawning method that doesn't properly resolve `.CMD` files on Windows in non-admin environments. This is an **upstream SDK issue**.

**Temporary Workarounds:**

1. **Use WSL without admin rights**: You can install WSL as a user if it's enabled by your IT department:
   ```powershell
   wsl --install --distribution Ubuntu
   ```
   Then set up the project in WSL where the SDK has better compatibility.

2. **Try Git Bash**: If you have Git for Windows installed, try running the scientific writer from Git Bash instead of CMD/PowerShell, as it provides a more Unix-like environment.

3. **Request IT assistance**: Ask your IT department to either:
   - Grant you temporary admin rights for software installation
   - Install the tool in a system-wide location
   - Enable WSL if not already available

4. **Use your personal machine**: As a short-term workaround, run the tool on a machine where you have admin rights (as you mentioned trying on your Mac).

5. **Report the SDK issue**: This is likely a bug in `claude-agent-sdk`. Consider opening an issue at the [Claude Agent SDK repository](https://github.com/anthropics/claude-agent-sdk) with your diagnostic information.

### Additional Diagnostics
If the problem persists, gather this information for further troubleshooting:

```cmd
# Check Claude version
claude --version

# Check npm global packages
npm list -g @anthropic-ai/claude-code

# Check Node.js version
node --version

# Check npm version
npm --version

# Check where npm installs global packages
npm config get prefix

# Check Python version
python --version

# Try npx
npx @anthropic-ai/claude-code --version

# Check for multiple Node installations
where node
where npm
```

Share this information when reporting the issue on GitHub or the SDK repository.

---

## API Key Issues

### Problem: "ANTHROPIC_API_KEY environment variable not set"

#### Solution 1: Create a .env file
In the project root directory, create a `.env` file:
```bash
ANTHROPIC_API_KEY=your_api_key_here
```

#### Solution 2: Export in your shell
**Linux/macOS:**
```bash
export ANTHROPIC_API_KEY='your_api_key_here'
```

Add to `~/.bashrc`, `~/.zshrc`, or `~/.bash_profile` to make it permanent.

**Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY='your_api_key_here'
```

**Windows (Command Prompt):**
```cmd
set ANTHROPIC_API_KEY=your_api_key_here
```

### Getting Your API Key
1. Go to [console.anthropic.com](https://console.anthropic.com/)
2. Sign in or create an account
3. Navigate to "API Keys"
4. Create a new key or copy an existing one

---

## Installation Problems

### Problem: "Module not found" errors

#### Solution: Install dependencies
Using uv (recommended):
```bash
uv pip install -e .
```

Using pip:
```bash
pip install -e .
```

### Problem: Python version incompatibility

This project requires **Python 3.10 or higher**.

Check your Python version:
```bash
python --version
# or
python3 --version
```

If you need to upgrade, visit [python.org](https://www.python.org/downloads/).

### Problem: Permission denied when installing

**Linux/macOS:**
```bash
# Use --user flag
pip install --user -e .

# Or use a virtual environment (recommended)
python -m venv venv
source venv/bin/activate
pip install -e .
```

**Windows:**
Run your terminal as Administrator, or use a virtual environment:
```cmd
python -m venv venv
venv\Scripts\activate
pip install -e .
```

---

## LaTeX Compilation Issues

### Problem: LaTeX compilation fails

#### Install LaTeX Distribution

**macOS:**
```bash
brew install --cask mactex
# Or install BasicTeX for a smaller footprint
brew install --cask basictex
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install texlive-full
# Or for a minimal installation
sudo apt-get install texlive-latex-base texlive-latex-extra
```

**Windows:**
Download and install [MiKTeX](https://miktex.org/download) or [TeX Live](https://www.tug.org/texlive/windows.html).

#### Missing LaTeX Packages

If you get "LaTeX Error: File `package.sty' not found":

**MiKTeX (Windows):**
MiKTeX usually installs packages automatically. If not:
1. Open MiKTeX Console
2. Go to "Packages"
3. Search for the missing package
4. Click "+" to install

**TeX Live (Linux/macOS):**
```bash
sudo tlmgr install <package-name>
```

#### Common Required Packages
```bash
# If using tlmgr
sudo tlmgr install amsmath graphicx hyperref natbib geometry fancyhdr
```

---

## General Issues

### Problem: "Permission denied" when accessing files

Check file permissions:
```bash
# Linux/macOS
ls -l <file_path>
chmod +r <file_path>  # Add read permission
```

### Problem: Script hangs or doesn't respond

1. **Check your internet connection** - The tool needs to connect to Anthropic's API
2. **Verify API key** - Ensure your API key is valid and has sufficient credits
3. **Try Ctrl+C** - Interrupt and try again
4. **Check API status** - Visit [status.anthropic.com](https://status.anthropic.com/)

### Problem: Output directory not created

Ensure you have write permissions in the project directory:
```bash
# Check permissions
ls -ld /path/to/claude-scientific-writer

# Fix if needed (Linux/macOS)
chmod u+w /path/to/claude-scientific-writer
```

### Problem: Data files not being processed

1. Ensure files are in the `data/` folder at the project root
2. Check that you have an active paper (either continuing or creating new)
3. Verify file permissions allow reading
4. Check the console output for any error messages

### Problem: Cannot find existing papers

1. Papers must be in the `paper_outputs/` directory
2. Paper directories should follow the format: `YYYYMMDD_HHMMSS_topic_description`
3. Use keywords from the paper topic when referencing it
4. Try using explicit continuation keywords like "continue", "update", "the paper"

---

## Getting Additional Help

If you've tried the solutions above and still have issues:

1. **Check the GitHub Issues**: [github.com/your-repo/issues](https://github.com)
2. **Create a New Issue**: Include:
   - Operating system and version
   - Python version (`python --version`)
   - Node.js version (`node --version`)
   - Claude Code version (`claude --version`)
   - Full error message and stack trace
   - Steps to reproduce the problem
3. **Review the README**: [README.md](../README.md)
4. **Check Skills Documentation**: [SKILLS.md](SKILLS.md)

---

## Contributing to This Guide

Found a solution to a problem not listed here? Please contribute!

1. Fork the repository
2. Add your solution to this document
3. Submit a pull request

Your contribution helps the community! 🙏

