import streamlit as st
from transformers import pipeline
from PIL import Image
from docx import Document
import fitz  # PyMuPDF for PDFs

# Page settings
st.set_page_config(
    page_title="📝 Text Summarizer",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        color: #0d6efd;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        text-align: center;
        font-size: 1.1rem;
        color: #6c757d;
        margin-bottom: 2rem;
    }
    .stTextArea textarea {
        font-size: 1rem;
    }
    .summary-box {
        background-color: #e9f5ff;
        padding: 1.2rem;
        border-radius: 0.5rem;
        border-left: 5px solid #0d6efd;
        font-size: 1.1rem;
        color: #0a3c78;
    }
    </style>
""", unsafe_allow_html=True)

# App Header
st.markdown('<div class="title">📝 Text Summarizer App</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Powered by 🤗 Transformers (T5 Model) | Built with ❤ in Streamlit</div>', unsafe_allow_html=True)

# Function to extract text from uploaded files
def extract_text_from_file(uploaded_file):
    file_type = uploaded_file.name.split('.')[-1].lower()
    if file_type == "txt":
        return uploaded_file.read().decode("utf-8")
    elif file_type == "pdf":
        text = ""
        pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        for page in pdf:
            text += page.get_text()
        return text
    elif file_type == "docx":
        doc = Document(uploaded_file)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        return "❌ Unsupported file format. Please upload a .txt, .pdf, or .docx file."

# File uploader
uploaded_file = st.file_uploader("📂 Upload a file (.txt, .pdf, .docx)", type=["txt", "pdf", "docx"])
file_text = ""
if uploaded_file is not None:
    file_text = extract_text_from_file(uploaded_file)

# Input text area (pre-filled with file content if uploaded)
text_input = st.text_area("📜 Or Enter your text here:", value=file_text, height=250, placeholder="Paste any article, blog, or paragraph to summarize...")

# Load summarizer
@st.cache_resource
def load_model():
    return pipeline("summarization", model="t5-small", framework="pt")

summarizer = load_model()

# Summarize Button
if st.button("🔍 Summarize Text"):
    if not text_input.strip():
        st.warning("Please enter some text before summarizing.")
    else:
        with st.spinner("Generating summary..."):
            summary = summarizer(text_input, max_length=150, min_length=30, do_sample=False)
            st.markdown(
                '<div class="summary-box">📌 <strong>Summary:</strong><br><br>{}</div>'.format(summary[0]['summary_text']),
                unsafe_allow_html=True
            )
