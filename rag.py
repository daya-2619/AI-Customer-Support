from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from PyPDF2 import PdfReader
import os


# 📄 Load PDF content
def load_pdf():
    pdf_path = "data/uploaded.pdf"

    if not os.path.exists(pdf_path):
        return ""

    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"

    return text


# 🧠 Create Vector Store (FAQ + PDF)
def create_vector_store():
    text = ""

    # Load FAQ
    if os.path.exists("data/faq.txt"):
        with open("data/faq.txt", "r", encoding="utf-8") as f:
            text += f.read() + "\n"

    # Load PDF
    text += load_pdf()

    # Safety check
    if not text.strip():
        text = "No data available."

    # Split text into chunks
    splitter = CharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=50
    )
    docs = splitter.split_text(text)

    # Embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Create vector DB
    db = FAISS.from_texts(docs, embeddings)

    return db


# 🔍 Retrieve context
def get_context(query, db, k=3):
    docs = db.similarity_search(query, k=k)

    if not docs:
        return ""

    context = "\n".join([doc.page_content for doc in docs])

    return context