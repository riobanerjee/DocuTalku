import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from typing import List

class VectorStore:
    def __init__(self, embedding_model: str = "all-MiniLM-L6-v2"):
        self.embedder = SentenceTransformer(embedding_model)
        self.index = None
        self.chunks = []
    
    def add_documents(self, chunks: List[str]):
        """Add document chunks to the vector store."""
        self.chunks = chunks
        
        # Create embeddings
        embeddings = self.embedder.encode(chunks)
        
        # Initialize FAISS index
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        
        # Add embeddings to index
        self.index.add(embeddings.astype('float32'))
    
    def search(self, query: str, k: int = 3) -> List[str]:
        """Search for relevant chunks."""
        if self.index is None:
            return []
        
        # Create query embedding
        query_embedding = self.embedder.encode([query])
        
        # Search index
        distances, indices = self.index.search(query_embedding.astype('float32'), k)
        
        # Return relevant chunks
        results = [self.chunks[i] for i in indices[0]]
        return results