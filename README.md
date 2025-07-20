# ClauseGPT – Legal Document RAG Assistant

ClauseGPT is an AI-powered legal document assistant that uses **Retrieval-Augmented Generation (RAG)** to answer user queries from uploaded legal PDFs. It combines the power of **Gemini LLM**, **LangChain**, and **FAISS** to deliver accurate, context-aware responses from complex legal texts.

---

## 🚀 Features

- Upload and process lengthy legal documents (PDF)
- Semantic chunking and embedding-based retrieval (FAISS)
- Query interface for asking legal questions
- Real-time LLM-powered responses using Gemini API
- Streamlit-based user interface for easy interaction

---

## 🧠 Tech Stack

| Component         | Technology                         |
|------------------|-------------------------------------|
| Language Model    | Gemini API (Google AI)             |
| RAG Framework     | LangChain                          |
| Vector Store      | FAISS (Facebook AI Similarity Search) |
| UI Framework      | Streamlit                          |
| Backend Language  | Python                             |
| PDF Processing    | PyMuPDF (`fitz`)                   |

---

## 📂 Folder Structure
ClauseGPT/
│
├── app.py # Main Streamlit app
├── utils/
│ ├── document_loader.py # Handles PDF upload and chunking
│ ├── vector_store.py # Embedding and FAISS integration
│ └── llm_response.py # Prompt formatting and Gemini integration
├── requirements.txt
└── README.md


---

## 🛠️ Installation & Setup

1. **Clone the repository**
```bash
git clone https://github.com/Sarvesh28D/ClauseGPT.git
cd ClauseGPT

(Optional) To Create virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:
pip install -r requirements.txt

Set up your Gemini API key:
Create a .env file in the root directory with the following line:
GEMINI_API_KEY=your_google_gemini_api_key_here

Run the application:
streamlit run app.py

