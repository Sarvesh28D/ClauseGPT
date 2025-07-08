"""
UI helper functions for the ClauseGPT application.
"""

import streamlit as st
from PIL import Image
import base64
from io import BytesIO

def set_custom_theme():
    """Apply custom styling to the Streamlit app."""
    st.markdown("""
    <style>
    /* Dark theme with better contrast */
    .main {
        background-color: #121212;
        color: #FFFFFF;
    }
    .st-emotion-cache-16txtl3 h1, .st-emotion-cache-16txtl3 h2, .st-emotion-cache-16txtl3 h3 {
        color: #FFFFFF;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .st-emotion-cache-16txtl3 {
        font-family: 'Helvetica Neue', sans-serif;
        color: #FFFFFF;
    }
    /* Card styling */
    .st-bw {
        background-color: #1E1E1E;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        margin-bottom: 20px;
        color: #FFFFFF;
    }
    /* Button styling */
    .st-emotion-cache-1wrcr25 {
        background-color: #008fd5;
    }
    .st-emotion-cache-6qob1r {
        background-color: #008fd5;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
        transition: all 0.3s ease;
    }
    .st-emotion-cache-6qob1r:hover {
        background-color: #00a3ff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.4);
    }
    /* Text input visibility and alignment with improved contrast */
    input[type="text"], textarea {
        color: #FFFFFF !important;
        background-color: #2D2D2D !important;
        font-size: 16px !important;
        line-height: 1.5 !important;
        padding: 10px !important;
        border: 1px solid #444444 !important;
        width: 100% !important;
    }
    .stTextInput input {
        color: #FFFFFF !important;
        font-weight: 400;
        border: 1px solid #444444 !important;
        border-radius: 4px !important;
        padding: 10px 15px !important;
        width: 100% !important;
    }
    .stTextInput label {
        color: #FFFFFF !important;
        font-weight: 500 !important;
        margin-bottom: 5px !important;
    }
    /* Text visibility with higher contrast */
    .st-emotion-cache-q8sbsg p, .element-container p, .element-container div, 
    .stMarkdown p, .stMarkdown li, .stMarkdown a, .stTextArea textarea {
        color: #FFFFFF !important;
    }
    /* Fix answer visibility with better contrast */
    .st-emotion-cache-183lzff p, .st-emotion-cache-1fttcpj p {
        color: #FFFFFF !important;
        font-size: 16px !important;
        line-height: 1.6 !important;
    }
    /* Make sure headers are visible with higher contrast */
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
    }
    /* Fix any other Streamlit elements */
    .stAlert p, .stInfo p, .stSuccess p, .stWarning p, .stError p {
        color: inherit !important;
    }
    /* Fix code and pre blocks for dark mode */
    code, pre {
        color: #E0E0E0 !important;
        background-color: #2D2D2D !important;
        border: 1px solid #444444;
        border-radius: 4px;
    }
    /* Fix special elements and inputs */
    .st-emotion-cache-1qg05tj input, .st-emotion-cache-16j3ifd textarea {
        color: #FFFFFF !important;
        background-color: #2D2D2D !important;
        border: 1px solid #444444;
    }
    /* Sidebar styling */
    .st-emotion-cache-1cypcdb {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    /* File uploader */
    .st-emotion-cache-1erivf3 {
        color: #FFFFFF !important;
    }
    /* Document stats cards */
    .document-stats {
        background-color: #2D2D2D !important;
        padding: 15px;
        border-radius: 5px;
        text-align: center;
        border: 1px solid #444444;
    }
    /* Question input field - ensure it spans full width */
    .stTextInput div[data-testid="stTextInput"] {
        width: 100% !important;
    }
    </style>
    """, unsafe_allow_html=True)

def display_logo():
    """Display the ClauseGPT logo."""
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center;">
            <h1 style="color: #FFFFFF; font-size: 3em; margin-bottom: 0;">
                <span style="color: #008fd5;">Clause</span>GPT
            </h1>
            <p style="color: #E0E0E0; font-style: italic; margin-top: 0;">
                Intelligent Legal Document Analysis
            </p>
        </div>
        """, unsafe_allow_html=True)

def create_footer():
    """Create a professional footer."""
    st.markdown("""
    <hr style="margin: 40px 0 20px 0; border: none; border-top: 1px solid #444444;">
    <div style="text-align: center; color: #AAAAAA; padding: 20px; font-size: 0.9em;">
        &copy; 2025 ClauseGPT | Legal Document Analysis Tool
        <br>
        Powered by LangChain, Streamlit, and Gemini AI
    </div>
    """, unsafe_allow_html=True)

def display_answer_card(answer, query):
    """Display the answer in a nicely formatted card."""
    st.markdown("""
    <div style="background-color: #1E1E1E; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); margin: 20px 0;">
        <h3 style="color: #FFFFFF; border-bottom: 2px solid #008fd5; padding-bottom: 10px; font-weight: 600;">Answer</h3>
        <div style="color: #E0E0E0; font-size: 0.95em; margin-bottom: 15px; font-weight: 500;">
            Question: "{}"
        </div>
        <div style="padding: 15px; background-color: #2D2D2D; border-left: 4px solid #008fd5; margin-top: 10px; font-size: 16px; line-height: 1.6; color: #FFFFFF;">
            {}
        </div>
    </div>
    """.format(query, answer.replace('\n', '<br>')), unsafe_allow_html=True)

def create_sidebar_info():
    """Create an informative sidebar."""
    with st.sidebar:
        st.markdown("### About ClauseGPT")
        st.info("""
        ClauseGPT uses advanced AI to analyze legal documents and answer questions.
        
        This tool helps legal professionals:
        - Quickly extract insights from contracts
        - Find relevant clauses instantly
        - Analyze legal language semantically
        """)
        
        st.markdown("### How to use")
        st.markdown("""
        1. Upload one or more PDF documents
        2. Wait for the indexing process to complete
        3. Ask specific questions about the content
        """)
        
        st.markdown("### Example Questions")
        example_questions = [
            "What are the key termination clauses?",
            "What is the notice period for contract renewal?",
            "What liabilities are excluded in this agreement?",
            "What are the payment terms?"
        ]
        for q in example_questions:
            if st.button(q, key=f"example_{hash(q)}"):
                return q
    return None

def show_document_stats(num_files, num_chunks):
    """Display document statistics in an informative way."""
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="document-stats">
            <h4 style="margin: 0; color: #008fd5;">Documents Processed</h4>
            <h2 style="margin: 0; color: #FFFFFF;">{num_files}</h2>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="document-stats">
            <h4 style="margin: 0; color: #008fd5;">Text Chunks Indexed</h4>
            <h2 style="margin: 0; color: #FFFFFF;">{num_chunks}</h2>
        </div>
        """, unsafe_allow_html=True)
