#!/bin/bash

# Research Assistant Chatbot Setup Script

echo "🚀 Setting up Research Assistant Chatbot..."
echo "================================================"

# Check Python version
python_version=$(python3 --version 2>&1)
if [[ $? -eq 0 ]]; then
    echo "✅ Found $python_version"
else
    echo "❌ Python3 not found. Please install Python 3.8 or higher."
    exit 1
fi

# Create virtual environment (optional but recommended)
read -p "Do you want to create a virtual environment? (y/n): " create_venv
if [[ $create_venv == "y" || $create_venv == "Y" ]]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✅ Virtual environment created and activated"
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

# Setup environment file
if [ ! -f .env ]; then
    echo "📝 Setting up environment file..."
    cp .env.example .env
    echo "✅ Created .env file from example"
    echo "⚠️  Please edit .env and add your HuggingFace API token"
else
    echo "✅ .env file already exists"
fi

# Test installation
echo "🧪 Testing installation..."
python3 simple_test.py

echo ""
echo "🎉 Setup Complete!"
echo "================================================"
echo "Next steps:"
echo "1. Edit .env file and add your HuggingFace API token"
echo "2. Test with: python3 src/cli.py --help"
echo "3. Start chatting: python3 src/cli.py --interactive"
echo "4. Run evaluation: python3 src/cli.py --evaluate"
echo ""
echo "For help, see README.md or run: python3 src/cli.py --help"
