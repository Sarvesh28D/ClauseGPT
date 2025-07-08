"""
rag_engine.py
Core logic for PDF parsing, chunking, embedding, vector store, and RAG chain.
"""

import os
import fitz  # PyMuPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter
import faiss
import numpy as np
from dotenv import load_dotenv
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
import time
import torch

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file.")

genai.configure(api_key=GEMINI_API_KEY)

class RAGEngine:
    def __init__(self, chunk_size=500, chunk_overlap=100, top_k=5):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.top_k = top_k
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
        self.index = None
        self.chunks = []
        self.embeddings = None
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        # Use GPU if available
        if torch.cuda.is_available():
            self.embedder = self.embedder.to('cuda')

    @staticmethod
    def _log_time(label, start):
        print(f"{label} took {time.time() - start:.2f} seconds")

    @staticmethod
    def _cache_embed_chunks(embedder, chunks):
        # Use batching for speed
        return np.array(embedder.encode(chunks, batch_size=32, show_progress_bar=False))

    def embed_chunks(self, chunks):
        import streamlit as st
        start = time.time()
        @st.cache_resource(show_spinner=False, hash_funcs={SentenceTransformer: id})
        def cached_embed(embedder, chunks):
            return self._cache_embed_chunks(embedder, chunks)
        result = cached_embed(self.embedder, tuple(chunks))
        self._log_time('Embedding', start)
        return result

    def build_vector_store(self, chunks):
        import streamlit as st
        start = time.time()
        self.chunks = chunks
        self.embeddings = self.embed_chunks(chunks)
        dim = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(self.embeddings)
        self._log_time('Vector store build', start)

    def chunk_text(self, text):
        start = time.time()
        result = self.text_splitter.split_text(text)
        self._log_time('Chunking', start)
        return result

    def parse_pdf(self, pdf_file):
        start = time.time()
        try:
            doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
            text = "\n".join(page.get_text() for page in doc)
            if not text.strip():
                raise ValueError("PDF is empty or could not be parsed.")
            self._log_time('PDF parsing', start)
            return text
        except Exception as e:
            raise RuntimeError(f"Failed to parse PDF: {e}")

    def retrieve(self, query):
        if self.index is None:
            raise RuntimeError("Vector store is not built.")
        query_emb = np.array([self.embedder.encode(query)])
        D, I = self.index.search(query_emb, self.top_k)
        return [self.chunks[i] for i in I[0]]

    def answer_query(self, query):
        context_chunks = self.retrieve(query)
        context = "\n\n".join(context_chunks)
        prompt = f"You are a legal assistant. Use the following context to answer the question as accurately as possible.\n\nContext:\n{context}\n\nQuestion: {query}\nAnswer:"
        # Try to list available Gemini models
        try:
            models = [m.name for m in genai.list_models()]
        except Exception as e:
            return f"Error listing Gemini models: {e}"
        # Try the first available model for answer generation
        for model_name in models:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                return response.text
            except Exception as e:
                continue
        return f"Error generating answer: No available Gemini model worked. Tried: {models}"
