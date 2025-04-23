# Document Q&A System

A simple yet powerful document question-answering system that uses Claude AI to answer questions about uploaded PDF documents.

## Features

- PDF document upload and processing
- Text chunking with overlap for better context preservation
- Vector similarity search using FAISS
- Question answering powered by Claude AI
- Clean and intuitive Streamlit interface

## Prerequisites

- Python 3.8+
- Anthropic API key

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/document-qa-system.git
   cd document-qa-system

2. Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:
    ```bash
    pip install -r requirements.txt

4. Set up environment variables:
Edit .env and add your Anthropic API key


## Running the Application

Start the Streamlit app:

    ```bash
    streamlit run app/main.py
    ```

Open browser and navigate to http://localhost:8501
Upload a PDF document and start asking questions!

Project Structure
```
document-qa-system/
├── app/                    # Application code
│   ├── main.py            # Streamlit frontend
│   ├── config.py          # Configuration management
│   ├── document_processor.py  # PDF processing
│   ├── vector_store.py    # Vector storage and search
│   └── qa_engine.py       # Question answering logic
├── data/                  # Data storage (gitignored)
├── tests/                 # Unit tests
├── requirements.txt       # Project dependencies
└── README.md             # This file

Contributing
Feel free to open issues or submit pull requests with improvements.

License
MIT License