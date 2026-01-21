"""
RAG System Core - Retrieval and Generation

This module handles:
1. Semantic search over vector database
2. Context retrieval with citations
3. Answer synthesis using OpenAI GPT-4
"""

import os
import chromadb
from chromadb.utils import embedding_functions
from openai import OpenAI
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()

class LennyRAG:
    def __init__(self, collection_name: str = "lenny_transcripts"):
        """Initialize RAG system"""
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(path="./data/vector_db")
        
        # Initialize OpenAI embeddings
        openai_ef = embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.getenv("OPENAI_API_KEY"),
            model_name="text-embedding-3-small"
        )
        
        # Get collection
        try:
            self.collection = self.client.get_collection(
                name=collection_name,
                embedding_function=openai_ef
            )
            print(f"✅ Loaded collection: {collection_name}")
            print(f"📊 Collection size: {self.collection.count()} chunks")
        except Exception as e:
            print(f"❌ Collection not found: {collection_name}")
            print(f"   Run 'python ingest_transcripts.py' first!")
            raise e
        
        # Initialize OpenAI client
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def search(self, query: str, n_results: int = 10) -> Dict:
        """
        Search for relevant transcript chunks
        
        Args:
            query: User's question
            n_results: Number of chunks to retrieve
            
        Returns:
            Dict with results and metadata
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        # Format results
        chunks = []
        for i in range(len(results['documents'][0])):
            chunks.append({
                'text': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i] if 'distances' in results else None
            })
        
        return {
            'query': query,
            'chunks': chunks
        }
    
    def format_context(self, chunks: List[Dict]) -> str:
        """Format retrieved chunks for LLM context"""
        context_parts = []
        
        for i, chunk in enumerate(chunks):
            meta = chunk['metadata']
            context_parts.append(
                f"[Source {i+1}]\n"
                f"Guest: {meta.get('guest', 'Unknown')}\n"
                f"Episode: {meta.get('title', 'Unknown')}\n"
                f"Content:\n{chunk['text']}\n"
            )
        
        return "\n---\n\n".join(context_parts)
    
    def synthesize_answer(self, query: str, chunks: List[Dict]) -> Dict:
        """
        Use OpenAI GPT-4 to synthesize answer from retrieved chunks
        
        Args:
            query: User's question
            chunks: Retrieved context chunks
            
        Returns:
            Dict with answer and citations
        """
        context = self.format_context(chunks)
        
        prompt = f"""You are an expert at analyzing podcast transcripts from Lenny's Podcast, which features interviews with world-class product leaders and growth experts.

A user has asked a question. Your job is to answer it using ONLY information from the provided transcript excerpts. Be specific and cite your sources.

USER QUESTION:
{query}

TRANSCRIPT EXCERPTS:
{context}

INSTRUCTIONS:
1. Answer the question comprehensively using the transcript excerpts
2. If multiple guests discuss the topic, synthesize their perspectives
3. Always include direct quotes when possible (use quotation marks)
4. Reference sources by guest name and episode title
5. If the excerpts don't contain enough information, say so
6. Format your answer in markdown

ANSWER:"""

        # Call OpenAI GPT-4
        response = self.openai_client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[{
                "role": "user",
                "content": prompt
            }],
            temperature=0.3,
            max_tokens=2000
        )
        
        answer_text = response.choices[0].message.content
        
        # Extract citations from chunks
        citations = []
        for chunk in chunks[:5]:  # Top 5 most relevant
            meta = chunk['metadata']
            citations.append({
                'guest': meta.get('guest', 'Unknown'),
                'title': meta.get('title', 'Unknown'),
                'youtube_url': meta.get('youtube_url', ''),
                'episode_folder': meta.get('episode_folder', ''),
                'text_snippet': chunk['text'][:200] + "..."
            })
        
        return {
            'answer': answer_text,
            'citations': citations,
            'n_sources': len(chunks)
        }
    
    def ask(self, query: str, n_results: int = 10) -> Dict:
        """
        Main RAG pipeline: search + synthesize
        
        Args:
            query: User's question
            n_results: Number of chunks to retrieve
            
        Returns:
            Dict with answer and full context
        """
        # Search
        search_results = self.search(query, n_results)
        
        # Synthesize
        answer_data = self.synthesize_answer(query, search_results['chunks'])
        
        return {
            'query': query,
            'answer': answer_data['answer'],
            'citations': answer_data['citations'],
            'n_sources': answer_data['n_sources'],
            'raw_chunks': search_results['chunks']
        }
    
    def export_to_markdown(self, result: Dict) -> str:
        """Export query result to markdown format"""
        md = f"# Query: {result['query']}\n\n"
        md += "## Answer\n\n"
        md += result['answer'] + "\n\n"
        md += "---\n\n"
        md += "## Sources\n\n"
        
        for i, citation in enumerate(result['citations']):
            md += f"### Source {i+1}: {citation['guest']}\n"
            md += f"**Episode:** {citation['title']}\n"
            if citation['youtube_url']:
                md += f"**YouTube:** {citation['youtube_url']}\n"
            md += f"\n**Excerpt:**\n> {citation['text_snippet']}\n\n"
        
        md += f"\n*Based on {result['n_sources']} relevant transcript excerpts*\n"
        
        return md

def test_rag():
    """Test the RAG system with sample queries"""
    print("=" * 70)
    print("Testing Ask Lenny RAG System")
    print("=" * 70)
    print()
    
    rag = LennyRAG()
    
    test_queries = [
        "What causes analytics projects to fail?",
        "How long does it take to build trust in data systems?",
        "What do founders say about build vs buy decisions?"
    ]
    
    for query in test_queries:
        print(f"\n📝 Query: {query}")
        print("-" * 70)
        
        result = rag.ask(query, n_results=5)
        
        print(f"\n✅ Answer:\n{result['answer'][:300]}...\n")
        print(f"📚 Based on {result['n_sources']} sources")
        print(f"🎤 Top guest: {result['citations'][0]['guest']}")
        print()

if __name__ == "__main__":
    test_rag()
