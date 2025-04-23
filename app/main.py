# app/main.py
import streamlit as st
from config import get_settings
from document_processor import DocumentProcessor
from vector_store import VectorStore
from qa_engine import QAEngine
import time
import json

# Page config
st.set_page_config(
    page_title="Document Q&A System",
    page_icon="📚",
    layout="wide"
)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'current_document' not in st.session_state:
    st.session_state.current_document = None
if 'anthropic_api_key' not in st.session_state:
    st.session_state.anthropic_api_key = None

# Initialize components
@st.cache_resource
def init_components(api_key):
    doc_processor = DocumentProcessor()
    vector_store = VectorStore()
    qa_engine = QAEngine(api_key)
    return doc_processor, vector_store, qa_engine

# App title
st.title("📚 Document Q&A System")

# API Key Input
st.markdown("### API Key Configuration")
api_key = st.text_input("Enter your Anthropic API Key:", type="password", key="api_key_input")
if api_key:
    st.session_state.anthropic_api_key = api_key
    doc_processor, vector_store, qa_engine = init_components(api_key)
else:
    st.warning("Please enter your Anthropic API Key to proceed.")
    st.stop()

# Create two columns
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### Document Upload")
    uploaded_file = st.file_uploader("Upload a PDF file", type=['pdf'])
    
    if uploaded_file:
        if st.session_state.current_document != uploaded_file.name:
            with st.spinner("Processing document..."):
                # Process the document
                chunks_with_metadata = doc_processor.process_pdf(uploaded_file)
                
                # Store in vector database
                vector_store.add_documents(chunks_with_metadata)
                
                st.session_state.current_document = uploaded_file.name
                st.session_state.chat_history = []  # Reset chat history
                
                st.success(f"Document processed successfully! Found {len(chunks_with_metadata)} text chunks.")
    
    # Q&A Interface
    if st.session_state.current_document:
        st.markdown(f"### Ask Questions about: {st.session_state.current_document}")
        
        # Chat input
        question = st.text_input("Enter your question:", key="question_input")
        
        if st.button("Ask") and question:
            with st.spinner("Finding answer..."):
                # Retrieve relevant chunks with metadata
                relevant_chunks = vector_store.search(question)
                
                # Generate answer
                answer = qa_engine.generate_answer(question, relevant_chunks)
                
                # Add to chat history
                st.session_state.chat_history.append({
                    'question': question,
                    'answer': answer,
                    'sources': relevant_chunks,
                    'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
                })
        
        # Display chat history
        st.markdown("### Conversation History")
        for i, chat in enumerate(reversed(st.session_state.chat_history)):
            with st.expander(f"Q: {chat['question']}", expanded=(i==0)):
                st.markdown(f"**Answer:** {chat['answer']}")
                st.markdown(f"*Asked at: {chat['timestamp']}*")
                
                # Show sources with citations
                st.markdown("**Sources:**")
                for j, source in enumerate(chat['sources'], 1):
                    st.markdown(f"{j}. Page {source['page']} - Relevance: {1/source['score']:.2f}")
                    st.text(source['text'][:200] + "...")

with col2:
    st.markdown("### Document Stats")
    if st.session_state.current_document:
        st.metric("Current Document", st.session_state.current_document)
        st.metric("Questions Asked", len(st.session_state.chat_history))
        
        # Export chat history
        if st.button("Export Chat History"):
            chat_export = {
                'document': st.session_state.current_document,
                'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
                'conversations': st.session_state.chat_history
            }
            
            st.download_button(
                label="Download Chat History",
                data=json.dumps(chat_export, indent=2),
                file_name=f"chat_history_{st.session_state.current_document}_{time.strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    st.markdown("### Tips")
    st.info("""
    - Be specific with your questions
    - Reference specific topics or sections
    - Ask follow-up questions for clarity
    - Check the source citations for context
    """)