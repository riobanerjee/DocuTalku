# app/document_processor.py
import PyPDF2
import io
from typing import List, Dict
import re

class DocumentProcessor:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def process_pdf(self, pdf_file) -> List[Dict]:
        """Extract text from PDF and split into chunks with metadata."""
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file.read()))
        
        chunks_with_metadata = []
        
        for page_num, page in enumerate(pdf_reader.pages):
            page_text = page.extract_text()
            
            # Clean text
            page_text = self._clean_text(page_text)
            
            # Create chunks with page numbers
            page_chunks = self._create_chunks_with_metadata(
                page_text, 
                page_num + 1, 
                pdf_file.name
            )
            chunks_with_metadata.extend(page_chunks)
        
        return chunks_with_metadata
    
    def _clean_text(self, text: str) -> str:
        """Clean extracted text."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters
        text = re.sub(r'[^\w\s.,!?-]', '', text)
        return text.strip()
    
    def _create_chunks_with_metadata(self, text: str, page_num: int, filename: str) -> List[Dict]:
        """Create chunks with metadata."""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + self.chunk_size
            chunk_text = text[start:end]
            
            chunks.append({
                'text': chunk_text,
                'page': page_num,
                'filename': filename,
                'chunk_id': f"{filename}_p{page_num}_c{len(chunks)}"
            })
            
            start += self.chunk_size - self.chunk_overlap
        
        return chunks