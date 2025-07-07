# Main entry point for the Streamlit RAG app

import streamlit as st
from rag_engine import RAGEngine
import io

st.set_page_config(page_title="Legal RAG App (Gemini)", layout="wide")
st.title("📄 Legal Document Q&A (Gemini RAG)")

if "rag" not in st.session_state:
    st.session_state.rag = RAGEngine()

uploaded_files = st.file_uploader(
    "Upload one or more legal PDF files", type=["pdf"], accept_multiple_files=True
)

if uploaded_files:
    all_text = ""
    for file in uploaded_files:
        try:
            text = st.session_state.rag.parse_pdf(file)
            all_text += text + "\n"
        except Exception as e:
            st.error(f"Error parsing {file.name}: {e}")
    if all_text.strip():
        with st.spinner("Chunking and indexing documents..."):
            chunks = st.session_state.rag.chunk_text(all_text)
            st.session_state.rag.build_vector_store(chunks)
        st.success(f"Indexed {len(chunks)} chunks from {len(uploaded_files)} file(s). Ready for questions!")
    else:
        st.warning("Uploaded PDFs are empty or could not be parsed.")

if st.session_state.rag.index is not None:
    query = st.text_input("Ask a question about your documents:")
    if query:
        with st.spinner("Retrieving answer from Gemini..."):
            answer = st.session_state.rag.answer_query(query)
        st.markdown("### Answer:")
        st.write(answer)
else:
    st.info("Upload and index PDFs to enable question answering.")
