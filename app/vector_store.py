# app/vector_store.py
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from typing import List, Dict
import json

class VectorStore:
    def __init__(self, embedding_model: str = "all-MiniLM-L6-v2"):
        self.embedder = SentenceTransformer(embedding_model)
        self.index = None
        self.chunks = []
        self.metadata = []
    
    def add_documents(self, chunks_with_metadata: List[Dict]):
        """Add document chunks with metadata to the vector store."""
        # Separate text and metadata
        texts = [chunk['text'] for chunk in chunks_with_metadata]
        self.metadata = chunks_with_metadata
        self.chunks = texts
        
        # Create embeddings
        embeddings = self.embedder.encode(texts, show_progress_bar=True)
        
        # Initialize FAISS index
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        
        # Add embeddings to index
        self.index.add(embeddings.astype('float32'))
    
    def search(self, query: str, k: int = 3) -> List[Dict]:
        """Search for relevant chunks with metadata."""
        if self.index is None:
            return []
        
        # Create query embedding
        query_embedding = self.embedder.encode([query])
        
        # Search index
        distances, indices = self.index.search(query_embedding.astype('float32'), k)
        
        # Return results with metadata and scores
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.metadata):
                result = self.metadata[idx].copy()
                result['score'] = float(distances[0][i])
                results.append(result)
        
        return results