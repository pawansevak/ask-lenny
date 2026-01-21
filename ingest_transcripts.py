"""
Ingest Lenny's Podcast Transcripts into Vector Database

This script:
1. Loads all 269 transcript files
2. Chunks them appropriately
3. Creates embeddings
4. Stores in ChromaDB
"""

import os
import yaml
import chromadb
from chromadb.utils import embedding_functions
from pathlib import Path
from typing import List, Dict
import re
import time
from dotenv import load_dotenv

load_dotenv()

class TranscriptIngester:
    def __init__(self, transcripts_path: str, collection_name: str = "lenny_transcripts"):
        self.transcripts_path = Path(transcripts_path)
        self.collection_name = collection_name
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(path="./data/vector_db")
        
        # Initialize OpenAI embeddings
        openai_ef = embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.getenv("OPENAI_API_KEY"),
            model_name="text-embedding-3-small"
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=openai_ef
        )
        
        print(f"✅ Initialized ChromaDB collection: {collection_name}")
    
    def parse_transcript(self, filepath: Path) -> Dict:
        """Parse a transcript markdown file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split frontmatter and content
        parts = content.split('---')
        if len(parts) >= 3:
            frontmatter = yaml.safe_load(parts[1])
            transcript_content = '---'.join(parts[2:]).strip()
            
            return {
                'metadata': frontmatter,
                'content': transcript_content,
                'filepath': str(filepath)
            }
        return None
    
    def chunk_transcript(self, transcript: Dict, chunk_size: int = 500) -> List[Dict]:
        """
        Chunk transcript into manageable pieces
        Strategy: Split by paragraphs, combine into ~500 word chunks (max ~2000 tokens)
        OpenAI embedding limit is 8192 tokens, so we stay well below that
        """
        content = transcript['content']
        metadata = transcript['metadata']
        
        # Split by double newlines (paragraphs)
        paragraphs = content.split('\n\n')
        
        chunks = []
        current_chunk = ""
        current_size = 0
        
        for para in paragraphs:
            para_size = len(para.split())  # Rough word count (tokens ≈ words * 1.3)
            
            # If this paragraph alone is too big, split it further
            if para_size > chunk_size:
                # Save current chunk if exists
                if current_chunk.strip():
                    chunks.append({
                        'text': current_chunk.strip(),
                        'metadata': metadata,
                        'filepath': transcript['filepath']
                    })
                    current_chunk = ""
                    current_size = 0
                
                # Split large paragraph by sentences
                sentences = para.split('. ')
                for sentence in sentences:
                    sentence_size = len(sentence.split())
                    if current_size + sentence_size > chunk_size and current_chunk:
                        chunks.append({
                            'text': current_chunk.strip(),
                            'metadata': metadata,
                            'filepath': transcript['filepath']
                        })
                        current_chunk = sentence + '. '
                        current_size = sentence_size
                    else:
                        current_chunk += sentence + '. '
                        current_size += sentence_size
                continue
            
            if current_size + para_size > chunk_size and current_chunk:
                # Save current chunk
                chunks.append({
                    'text': current_chunk.strip(),
                    'metadata': metadata,
                    'filepath': transcript['filepath']
                })
                current_chunk = para
                current_size = para_size
            else:
                current_chunk += "\n\n" + para
                current_size += para_size
        
        # Add final chunk
        if current_chunk.strip():
            chunks.append({
                'text': current_chunk.strip(),
                'metadata': metadata,
                'filepath': transcript['filepath']
            })
        
        return chunks
    
    def extract_speaker_context(self, text: str) -> str:
        """Extract speaker names from text for better context"""
        # Look for patterns like "Speaker Name (timestamp):"
        speakers = re.findall(r'^([A-Z][a-zA-Z\s]+)\s*\(\d+:\d+:\d+\):', text, re.MULTILINE)
        return ", ".join(set(speakers[:3])) if speakers else ""
    
    def ingest_all_transcripts(self):
        """Main ingestion process"""
        episodes_path = self.transcripts_path / "episodes"
        
        if not episodes_path.exists():
            print(f"❌ Transcripts not found at: {episodes_path}")
            return
        
        # Get all transcript files
        transcript_files = list(episodes_path.glob("*/transcript.md"))
        print(f"📚 Found {len(transcript_files)} transcripts to ingest")
        
        all_chunks = []
        chunk_ids = []
        chunk_metadatas = []
        
        for i, filepath in enumerate(transcript_files):
            try:
                # Parse transcript
                transcript = self.parse_transcript(filepath)
                if not transcript:
                    continue
                
                # Chunk it
                chunks = self.chunk_transcript(transcript)
                
                # Prepare for ChromaDB
                for j, chunk in enumerate(chunks):
                    chunk_id = f"{transcript['metadata'].get('guest', 'unknown')}_{i}_{j}"
                    
                    # Extract additional context
                    speakers = self.extract_speaker_context(chunk['text'])
                    
                    metadata = {
                        'guest': transcript['metadata'].get('guest', 'Unknown'),
                        'title': transcript['metadata'].get('title', 'Unknown'),
                        'youtube_url': transcript['metadata'].get('youtube_url', ''),
                        'publish_date': str(transcript['metadata'].get('publish_date', '')),
                        'episode_folder': filepath.parent.name,
                        'chunk_index': j,
                        'speakers': speakers
                    }
                    
                    all_chunks.append(chunk['text'])
                    chunk_ids.append(chunk_id)
                    chunk_metadatas.append(metadata)
                
                if (i + 1) % 10 == 0:
                    print(f"  Processed {i + 1}/{len(transcript_files)} transcripts...")
            
            except Exception as e:
                print(f"  ⚠️  Error processing {filepath.name}: {e}")
                continue
        
        # Batch insert into ChromaDB with rate limiting
        print(f"\n💾 Inserting {len(all_chunks)} chunks into vector database...")
        print(f"   (This may take 10-15 minutes due to OpenAI rate limits)")
        
        batch_size = 50  # Smaller batches to avoid rate limits
        for i in range(0, len(all_chunks), batch_size):
            batch_end = min(i + batch_size, len(all_chunks))
            
            # Retry logic for rate limits
            max_retries = 5
            retry_count = 0
            
            while retry_count < max_retries:
                try:
                    self.collection.add(
                        ids=chunk_ids[i:batch_end],
                        documents=all_chunks[i:batch_end],
                        metadatas=chunk_metadatas[i:batch_end]
                    )
                    print(f"  ✓ Batch {i//batch_size + 1}/{(len(all_chunks) + batch_size - 1)//batch_size}")
                    
                    # Small delay between batches to respect rate limits
                    time.sleep(2)
                    break
                    
                except Exception as e:
                    if "rate_limit" in str(e).lower():
                        retry_count += 1
                        wait_time = 2 ** retry_count  # Exponential backoff: 2, 4, 8, 16, 32 seconds
                        print(f"  ⏳ Rate limit hit. Waiting {wait_time}s... (retry {retry_count}/{max_retries})")
                        time.sleep(wait_time)
                    else:
                        raise e
            
            if retry_count >= max_retries:
                print(f"  ❌ Failed to insert batch after {max_retries} retries. Skipping...")
        
        print(f"\n✅ Successfully ingested {len(transcript_files)} transcripts into {len(all_chunks)} chunks!")
        print(f"📊 Collection size: {self.collection.count()} documents")

def main():
    """Run the ingestion process"""
    print("=" * 70)
    print("Ask Lenny - Transcript Ingestion")
    print("=" * 70)
    print()
    
    # Path to transcripts (now included in repo)
    transcripts_path = "./transcripts/episodes"
    
    if not os.path.exists(transcripts_path):
        print("❌ Transcripts folder not found!")
        print(f"   Expected: {os.path.abspath(transcripts_path)}")
        print()
        print("Make sure you have the transcripts folder in the project directory")
        return
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not found!")
        print("   Create a .env file with your API key")
        print("   Copy .env.example to .env and fill in your key")
        return
    
    # Run ingestion
    ingester = TranscriptIngester(transcripts_path)
    ingester.ingest_all_transcripts()
    
    print()
    print("=" * 70)
    print("🎉 Ingestion complete! You can now run the chat interface:")
    print("   streamlit run app.py")
    print("=" * 70)

if __name__ == "__main__":
    main()
