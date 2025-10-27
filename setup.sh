#!/bin/bash
# Setup script for Scientific Writer CLI

echo "=================================="
echo "Scientific Writer CLI Setup"
echo "=================================="
echo ""

# Check if uv is installed
echo "Checking for uv installation..."
if ! command -v uv &> /dev/null; then
    echo "✗ uv not found. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    if [ $? -eq 0 ]; then
        echo "✓ uv installed successfully"
        echo ""
        echo "⚠️  Please restart your shell or run:"
        echo "   source $HOME/.cargo/env"
        echo ""
        echo "Then run this setup script again."
        exit 0
    else
        echo "✗ Failed to install uv"
        exit 1
    fi
else
    echo "✓ uv is installed"
fi

# Check Python version
echo ""
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')
required_version="3.10"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then
    echo "✓ Python $python_version detected (requires 3.10+)"
else
    echo "✗ Python 3.10+ required. Found: $python_version"
    exit 1
fi

# Install dependencies using uv
echo ""
echo "Installing dependencies with uv..."
uv pip install -e .

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "✗ Failed to install dependencies"
    exit 1
fi

# Check for API key
echo ""
if [ -f ".env" ]; then
    echo "✓ .env file found"
else
    echo "Creating .env file..."
    echo "ANTHROPIC_API_KEY=your_api_key_here" > .env
    echo "✓ Created .env file"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your Anthropic API key!"
    echo "   Get your key from: https://console.anthropic.com/"
fi

# Make script executable
chmod +x scientific_writer.py

echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Edit .env and add your ANTHROPIC_API_KEY"
echo "2. Run: python scientific_writer.py"
echo ""
echo "For more information, see README.md"
echo ""

