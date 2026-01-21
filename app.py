"""
Ask Lenny - Streamlit Chat Interface

A simple chat interface to query Lenny's Podcast transcripts
"""

import streamlit as st
from rag_system import LennyRAG
import os
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Ask Lenny",
    page_icon="🎙️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .citation {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .citation-title {
        font-weight: 600;
        color: #1f1f1f;
    }
    .citation-meta {
        font-size: 0.9rem;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'rag' not in st.session_state:
    try:
        st.session_state.rag = LennyRAG()
        st.session_state.ready = True
    except Exception as e:
        st.session_state.ready = False
        st.session_state.error = str(e)

if 'history' not in st.session_state:
    st.session_state.history = []

# Header
st.markdown('<div class="main-header">🎙️ Ask Lenny</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Query 269 episodes of Lenny\'s Podcast with citations</div>', unsafe_allow_html=True)

# Check if system is ready
if not st.session_state.ready:
    st.error("❌ RAG system not initialized!")
    st.error(f"Error: {st.session_state.error}")
    st.info("💡 Make sure you've run: `python ingest_transcripts.py`")
    st.stop()

# Sidebar
with st.sidebar:
    st.header("📊 System Info")
    
    collection_size = st.session_state.rag.collection.count()
    st.metric("Total Chunks", f"{collection_size:,}")
    st.metric("Episodes", "269")
    
    st.divider()
    
    st.header("💡 Example Queries")
    example_queries = [
        "What causes analytics projects to fail?",
        "How long does it take to build trust in data?",
        "Build vs buy analytics platforms",
        "Schema evolution challenges",
        "Data governance at scale",
        "Metric consistency across teams",
        "What makes Palantir's data platform different?",
        "Why did companies switch from Mixpanel?"
    ]
    
    for query in example_queries:
        if st.button(query, key=f"example_{query}", use_container_width=True):
            st.session_state.current_query = query
    
    st.divider()
    
    st.header("⚙️ Settings")
    n_results = st.slider("Number of sources", 5, 20, 10)
    
    st.divider()
    
    if st.session_state.history:
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.history = []
            st.rerun()

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.header("💬 Ask a Question")
    
    # Query input
    query = st.text_input(
        "Your question:",
        value=st.session_state.get('current_query', ''),
        placeholder="e.g., What do founders say about data quality?",
        key="query_input"
    )
    
    search_button = st.button("🔍 Search", type="primary", use_container_width=True)
    
    if search_button and query:
        with st.spinner("🔍 Searching 269 episodes..."):
            try:
                result = st.session_state.rag.ask(query, n_results=n_results)
                st.session_state.history.insert(0, result)
                st.session_state.current_query = ""
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {e}")

# Display results
if st.session_state.history:
    st.divider()
    
    result = st.session_state.history[0]
    
    # Answer
    st.header("💡 Answer")
    st.markdown(result['answer'])
    
    # Export button
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        markdown_export = st.session_state.rag.export_to_markdown(result)
        st.download_button(
            "📥 Export Markdown",
            markdown_export,
            file_name=f"ask_lenny_{result['query'][:30]}.md",
            mime="text/markdown"
        )
    
    with col2:
        if st.button("📋 Copy Answer"):
            st.code(result['answer'], language=None)
    
    st.divider()
    
    # Citations
    st.header("📚 Sources")
    st.caption(f"Based on {result['n_sources']} relevant transcript excerpts")
    
    for i, citation in enumerate(result['citations']):
        with st.expander(f"**{i+1}. {citation['guest']}** - {citation['title'][:60]}..."):
            st.markdown(f"**Episode:** {citation['title']}")
            
            if citation['youtube_url']:
                st.markdown(f"**YouTube:** [{citation['youtube_url']}]({citation['youtube_url']})")
            
            st.markdown("**Excerpt:**")
            st.info(citation['text_snippet'])

with col2:
    st.header("📜 Query History")
    
    if not st.session_state.history:
        st.info("No queries yet. Ask a question to get started!")
    else:
        for i, item in enumerate(st.session_state.history[1:6]):  # Show last 5
            with st.container():
                st.markdown(f"**{i+1}. {item['query'][:50]}...**")
                st.caption(f"{item['n_sources']} sources")
                if st.button("View", key=f"view_{i}"):
                    st.session_state.history.insert(0, st.session_state.history.pop(i+1))
                    st.rerun()
                st.divider()

# Footer
st.divider()
st.caption("📊 Data Source: [Lenny's Podcast Transcripts Archive](https://github.com/ChatPRD/lennys-podcast-transcripts)")
st.caption("🔨 Built with Streamlit, ChromaDB, and OpenAI (Embeddings + GPT-4)")
