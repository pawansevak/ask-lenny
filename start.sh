#!/bin/bash

echo "🚀 Starting Ask Lenny..."

# Check if vector database exists
if [ ! -f "data/vector_db/chroma.sqlite3" ]; then
    echo "📥 Vector database not found. Running ingestion..."
    echo "⏳ This will take 10-15 minutes on first deployment..."
    python ingest_transcripts.py
    
    if [ $? -eq 0 ]; then
        echo "✅ Ingestion complete!"
    else
        echo "❌ Ingestion failed. Check logs."
        exit 1
    fi
else
    echo "✅ Vector database found. Skipping ingestion."
fi

echo "🎙️ Starting Streamlit app..."
streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
