# Main entry point for the Streamlit RAG app

import streamlit as st
from rag_engine import RAGEngine
import io
from utils.ui_helpers import (
    set_custom_theme, 
    display_logo, 
    create_footer, 
    display_answer_card,
    create_sidebar_info,
    show_document_stats
)

st.set_page_config(
    page_title="ClauseGPT | Legal Document Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styling
set_custom_theme()

# Display logo and header
display_logo()

# Create sidebar with info and example questions
example_query = create_sidebar_info()

# Initialize RAG engine
if "rag" not in st.session_state:
    st.session_state.rag = RAGEngine()
    st.session_state.chat_history = []

# Main UI container with shadow effect
main_container = st.container()
with main_container:
    st.markdown('<div class="st-bw">', unsafe_allow_html=True)
    
    # Document upload section
    st.subheader("📄 Document Upload")
    uploaded_files = st.file_uploader(
        "Upload legal documents (PDF format)",
        type=["pdf"],
        accept_multiple_files=True,
        help="Upload one or more legal PDF documents to analyze"
    )

    # Process uploaded documents
    if uploaded_files:
        all_text = ""
        with st.spinner("📄 Processing documents..."):
            for file in uploaded_files:
                try:
                    text = st.session_state.rag.parse_pdf(file)
                    all_text += text + "\n"
                except Exception as e:
                    st.error(f"Error processing {file.name}: {e}")
        
        if all_text.strip():
            with st.spinner("🔍 Analyzing and indexing content..."):
                chunks = st.session_state.rag.chunk_text(all_text)
                st.session_state.rag.build_vector_store(chunks)
            
            # Display document statistics
            show_document_stats(len(uploaded_files), len(chunks))
            st.success("✅ Documents successfully indexed! Ask questions below.")
        else:
            st.warning("⚠️ Uploaded PDFs are empty or could not be processed.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Query section
    if st.session_state.rag.index is not None:
        st.markdown('<div class="st-bw">', unsafe_allow_html=True)
        st.subheader("💬 Ask Your Question")
        
        # Use example question if clicked, otherwise use text input
        col1, = st.columns([1])  # Use a single column for full width
        with col1:
            query = example_query if example_query else st.text_input(
                "Enter your question about the documents:",
                placeholder="e.g., What are the key termination clauses in the contract?",
                key="query_input"
            )
        
        if query:
            with st.spinner("🤔 Analyzing documents and generating answer..."):
                answer = st.session_state.rag.answer_query(query)
                
                # Add to chat history
                st.session_state.chat_history.append({"query": query, "answer": answer})
            
            # Display the answer in a nicely formatted card
            display_answer_card(answer, query)
            
            # Display chat history
            if len(st.session_state.chat_history) > 1:
                with st.expander("View Previous Questions & Answers"):
                    for i, qa in enumerate(st.session_state.chat_history[:-1]):
                        st.markdown(f"**Question {i+1}:** {qa['query']}")
                        st.markdown(f"**Answer:** {qa['answer']}")
                        st.markdown("---")
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="st-bw">', unsafe_allow_html=True)
        st.info("👆 Please upload documents above to start asking questions.")
        st.markdown('</div>', unsafe_allow_html=True)

# Add footer
create_footer()
