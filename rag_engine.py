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

    def parse_pdf(self, pdf_file):
        try:
            doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
            text = "\n".join(page.get_text() for page in doc)
            if not text.strip():
                raise ValueError("PDF is empty or could not be parsed.")
            return text
        except Exception as e:
            raise RuntimeError(f"Failed to parse PDF: {e}")

    def chunk_text(self, text):
        return self.text_splitter.split_text(text)

    def embed_chunks(self, chunks):
        embeddings = self.embedder.encode(chunks, show_progress_bar=False)
        return np.array(embeddings)

    def build_vector_store(self, chunks):
        self.chunks = chunks
        self.embeddings = self.embed_chunks(chunks)
        dim = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(self.embeddings)

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
