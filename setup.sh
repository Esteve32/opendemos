#!/bin/bash

# Gemini HTML Manager Setup Script
# This script helps you set up the Gemini HTML Manager for managing Google Gemini exports

echo "🚀 Gemini HTML Manager Setup"
echo "=============================="
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1)
if [[ $? -eq 0 ]]; then
    echo "✅ Found: $python_version"
else
    echo "❌ Python 3 is required but not found"
    exit 1
fi

# Install dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

if [[ $? -eq 0 ]]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Create export directory
echo ""
echo "📁 Setting up directories..."
mkdir -p html_exports
echo "✅ Created html_exports directory"

# Copy configuration
if [[ ! -f "config.yaml" ]]; then
    cp config.example.yaml config.yaml
    echo "✅ Created config.yaml from example"
else
    echo "ℹ️  config.yaml already exists"
fi

# Check for Google credentials
echo ""
echo "🔑 Checking Google Workspace credentials..."
if [[ ! -f "credentials.json" ]]; then
    echo "⚠️  Google Workspace credentials not found"
    echo ""
    echo "To set up Google Workspace integration:"
    echo "1. Go to https://console.cloud.google.com/"
    echo "2. Create a new project or select existing one"
    echo "3. Enable Google Drive API and Google Docs API"
    echo "4. Create OAuth 2.0 Client ID for Desktop application"
    echo "5. Download credentials as 'credentials.json'"
    echo "6. Run: python scripts/gemini_manager.py setup"
    echo ""
    echo "You can still use the local file management features without Google integration."
else
    echo "✅ Found credentials.json"
    echo "🔄 Testing Google Workspace authentication..."
    python3 scripts/gemini_manager.py setup
fi

echo ""
echo "🎉 Setup completed!"
echo ""
echo "Next steps:"
echo "1. 📥 Import HTML files: python scripts/gemini_manager.py import-file path/to/your/file.html"
echo "2. 🌐 Start web interface: python scripts/gemini_manager.py web"
echo "3. 📋 List files: python scripts/gemini_manager.py list-files"
echo "4. ☁️  Upload to Google Drive: python scripts/gemini_manager.py upload path/to/file.html"
echo ""
echo "Web interface will be available at: http://localhost:5000"
echo "Documentation available in the docs/ directory"
echo ""
echo "Happy managing! 🚀"