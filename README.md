# Ask Lenny - RAG System
## Query 269 Episodes of Lenny's Podcast

A RAG (Retrieval-Augmented Generation) system to ask questions and get answers from Lenny's Podcast transcripts with citations.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the chat interface
streamlit run app.py
```

## Features

- 🔍 **Semantic Search** across 269 podcast episodes
- 💬 **Natural Language Queries** - ask any question
- 📝 **Cited Answers** - every answer includes episode references
- 🎯 **Speaker Attribution** - know exactly who said what
- 📊 **Export Results** - save answers to markdown/Word

## Architecture

```
User Question
    ↓
Semantic Search (OpenAI embeddings)
    ↓
Retrieve top 10 relevant chunks
    ↓
LLM synthesizes answer (OpenAI GPT-4)
    ↓
Answer + Citations + Episode links
```

## Example Queries

- "What causes analytics projects to fail?"
- "How long does it take to build trust in data systems?"
- "What do founders say about build vs buy decisions?"
- "Schema evolution challenges in analytics"

## Project Structure

```
ask-lenny/
├── app.py                  # Streamlit chat interface
├── rag_system.py           # Core RAG implementation
├── ingest_transcripts.py   # Load and chunk transcripts
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── README.md              # This file
└── data/
    ├── vector_db/         # ChromaDB storage (auto-created)
    └── transcripts/       # Link to transcript folder
```

## Configuration

Create `.env` file:

```bash
OPENAI_API_KEY=your_key_here
```

Get your key from: https://platform.openai.com/api-keys  
**New accounts get $5 free credit!**

## Next Steps

1. Install dependencies
2. Set up API keys
3. Ingest transcripts (one-time setup)
4. Start querying!

See individual files for implementation details.
