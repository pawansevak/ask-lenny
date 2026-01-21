#!/usr/bin/env python3
"""
Quick setup check and instructions for Ask Lenny
"""

import os
from pathlib import Path

def check_environment():
    print("=" * 70)
    print("🎙️ ASK LENNY - Environment Check")
    print("=" * 70)
    print()
    
    checks = {
        'passed': [],
        'failed': []
    }
    
    # Check 1: Transcripts
    print("📁 Checking for transcripts...")
    transcripts_path = Path("../lennys-podcast-transcripts/episodes")
    if transcripts_path.exists():
        count = len(list(transcripts_path.glob("*/transcript.md")))
        checks['passed'].append(f"✅ Found {count} transcripts")
    else:
        checks['failed'].append("❌ Transcripts not found at ../lennys-podcast-transcripts")
    
    # Check 2: Python
    print("🐍 Checking Python...")
    import sys
    if sys.version_info >= (3, 8):
        checks['passed'].append(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")
    else:
        checks['failed'].append("❌ Python 3.8+ required")
    
    # Check 3: .env file
    print("🔑 Checking environment variables...")
    env_path = Path(".env")
    if env_path.exists():
        from dotenv import load_dotenv
        load_dotenv()
        
        if os.getenv("OPENAI_API_KEY") and os.getenv("OPENAI_API_KEY") != "your_openai_api_key_here":
            checks['passed'].append("✅ OpenAI API key configured")
        else:
            checks['failed'].append("❌ OPENAI_API_KEY not set in .env")
    else:
        checks['failed'].append("❌ .env file not found (copy env-template.txt)")
    
    # Check 4: Vector DB
    print("💾 Checking vector database...")
    db_path = Path("./data/vector_db")
    if db_path.exists():
        try:
            import chromadb
            client = chromadb.PersistentClient(path="./data/vector_db")
            collection = client.get_collection("lenny_transcripts")
            count = collection.count()
            checks['passed'].append(f"✅ Vector DB exists with {count:,} chunks")
        except:
            checks['failed'].append("❌ Vector DB exists but empty (run ingest_transcripts.py)")
    else:
        checks['failed'].append("❌ Vector DB not found (run ingest_transcripts.py)")
    
    # Check 5: Dependencies
    print("📦 Checking dependencies...")
    try:
        import streamlit
        import openai
        import chromadb
        checks['passed'].append("✅ All dependencies installed")
    except ImportError as e:
        checks['failed'].append(f"❌ Missing dependency: {e}")
    
    # Summary
    print()
    print("=" * 70)
    print("📊 RESULTS")
    print("=" * 70)
    print()
    
    for check in checks['passed']:
        print(check)
    
    if checks['failed']:
        print()
        for check in checks['failed']:
            print(check)
    
    print()
    print("=" * 70)
    
    if not checks['failed']:
        print("🎉 ALL CHECKS PASSED!")
        print()
        print("You're ready to use Ask Lenny!")
        print()
        print("Start the web interface:")
        print("  streamlit run app.py")
        print()
        print("Or use the Python API:")
        print("  python rag_system.py")
    else:
        print("⚠️  SETUP INCOMPLETE")
        print()
        print("Next steps:")
        if any("transcripts" in check for check in checks['failed']):
            print("  1. Make sure transcripts are in ../lennys-podcast-transcripts/")
        if any(".env" in check for check in checks['failed']):
            print("  2. Copy env-template.txt to .env and add API keys")
        if any("dependency" in check for check in checks['failed']):
            print("  3. Install dependencies: pip install -r requirements.txt")
        if any("Vector DB" in check for check in checks['failed']):
            print("  4. Ingest transcripts: python ingest_transcripts.py")
        print()
        print("Or run automated setup:")
        print("  bash setup.sh")
    
    print("=" * 70)

if __name__ == "__main__":
    try:
        check_environment()
    except Exception as e:
        print(f"Error during environment check: {e}")
        print()
        print("This is normal if you haven't installed dependencies yet.")
        print()
        print("Run: bash setup.sh")
