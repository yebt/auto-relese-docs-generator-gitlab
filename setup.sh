#!/bin/bash

# GitLab Changelog Generator - Setup Script
# This script automates the initial setup process

set -e

echo "🚀 GitLab Changelog Generator - Setup"
echo "======================================"
echo ""

# Check Python version
echo "📋 Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Found Python $PYTHON_VERSION"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source .venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env file and add your credentials:"
    echo "   - GITLAB_ACCESS_TOKEN"
    echo "   - GITLAB_PROJECT_ID"
    echo "   - GEMINI_TOKEN"
    echo ""
else
    echo "✅ .env file already exists"
    echo ""
fi

# Create results directory
if [ ! -d "results" ]; then
    mkdir results
    echo "✅ Created results/ directory"
else
    echo "✅ results/ directory already exists"
fi
echo ""

echo "======================================"
echo "✅ Setup completed successfully!"
echo "======================================"
echo ""
echo "📋 Next steps:"
echo "   1. Edit .env file with your credentials"
echo "   2. Run: source .venv/bin/activate"
echo "   3. Run: python main.py"
echo ""
echo "📚 Documentation:"
echo "   - Quick Start: QUICKSTART.md"
echo "   - Full Guide: README.md"
echo "   - Sample Output: SAMPLE_OUTPUT.md"
echo ""
echo "🎉 Happy changelog generating!"
