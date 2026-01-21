#!/bin/bash

# Setup script for Ask Lenny RAG System

echo "=================================="
echo "Ask Lenny - Setup"
echo "=================================="
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

echo "✅ Python 3 found"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Check for .env file
if [ ! -f .env ]; then
    echo ""
    echo "⚠️  .env file not found!"
    echo ""
    echo "📝 Creating .env file from template..."
    cp env-template.txt .env
    echo ""
    echo "🔑 Please edit .env and add your OpenAI API key:"
    echo "   - OPENAI_API_KEY"
    echo ""
    echo "Then run this script again."
    exit 1
fi

# Check if API key is set
source .env
if [ -z "$OPENAI_API_KEY" ] || [ "$OPENAI_API_KEY" = "your_openai_api_key_here" ]; then
    echo ""
    echo "❌ OPENAI_API_KEY not set in .env"
    echo "   Please edit .env and add your OpenAI API key"
    echo "   Get it from: https://platform.openai.com/api-keys"
    exit 1
fi

echo ""
echo "✅ API key configured"

# Check if transcripts exist
if [ ! -d "../lennys-podcast-transcripts" ]; then
    echo ""
    echo "❌ Transcripts not found at ../lennys-podcast-transcripts"
    echo ""
    echo "Expected structure:"
    echo "  Enterprise SaaS insights/"
    echo "  ├── ask-lenny/"
    echo "  └── lennys-podcast-transcripts/"
    exit 1
fi

echo "✅ Transcripts found"

# Ask if user wants to ingest now
echo ""
read -p "📚 Ingest transcripts now? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "🔄 Starting ingestion (this will take 5-10 minutes)..."
    python ingest_transcripts.py
fi

echo ""
echo "=================================="
echo "✅ Setup complete!"
echo "=================================="
echo ""
echo "To start the chat interface:"
echo "  source venv/bin/activate"
echo "  streamlit run app.py"
echo ""
echo "Or test the RAG system:"
echo "  source venv/bin/activate"
echo "  python rag_system.py"
echo ""
