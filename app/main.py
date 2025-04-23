import streamlit as st
from app.config import get_settings
from app.document_processor import DocumentProcessor
from app.vector_store import VectorStore
from app.qa_engine import QAEngine

# Page config
st.set_page_config(
    page_title="Document Q&A System",
    page_icon="📚",
    layout="wide"
)

# Initialize components
@st.cache_resource
def init_components():
    settings = get_settings()
    doc_processor = DocumentProcessor()
    vector_store = VectorStore()
    qa_engine = QAEngine(settings.ANTHROPIC_API_KEY)
    return doc_processor, vector_store, qa_engine

doc_processor, vector_store, qa_engine = init_components()

# App title
st.title("📚 Document Q&A System")
st.markdown("Upload a PDF document and ask questions about its content.")

# Sidebar
with st.sidebar:
    st.header("About")
    st.markdown("""
    This application allows you to:
    - Upload PDF documents
    - Ask questions about the content
    - Get AI-powered answers with context
    """)

# Main content
uploaded_file = st.file_uploader("Upload a PDF file", type=['pdf'])

if uploaded_file:
    with st.spinner("Processing document..."):
        # Process the document
        text_chunks = doc_processor.process_pdf(uploaded_file)
        
        # Store in vector database
        vector_store.add_documents(text_chunks)
        
        st.success(f"Document processed successfully! Found {len(text_chunks)} text chunks.")
    
    # Q&A Interface
    st.subheader("Ask Questions")
    question = st.text_input("Enter your question about the document:")
    
    if question:
        with st.spinner("Finding answer..."):
            # Retrieve relevant chunks
            relevant_chunks = vector_store.search(question)
            
            # Generate answer
            answer = qa_engine.generate_answer(question, relevant_chunks)
            
            # Display answer
            st.markdown("### Answer")
            st.write(answer)
            
            # Show source chunks
            with st.expander("View source text"):
                for i, chunk in enumerate(relevant_chunks, 1):
                    st.markdown(f"**Chunk {i}:**")
                    st.text(chunk)
                    st.markdown("---")