# app/qa_engine.py
from anthropic import Anthropic
from typing import List, Dict
import hashlib
import json

class QAEngine:
    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)
        self.cache = {}  # Simple in-memory cache
    
    def generate_answer(self, question: str, context_chunks: List[Dict]) -> str:
        """Generate an answer using Claude based on the context."""
        # Create cache key
        cache_key = self._create_cache_key(question, context_chunks)
        
        # Check cache first
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Prepare context with citations
        context_with_citations = self._prepare_context_with_citations(context_chunks)
        
        # Create prompt
        prompt = f"""Based on the following context from a document, please answer the question. 
                Include citations by referencing the page numbers where you found the information.
                If the answer cannot be found in the context, say so.

                {context_with_citations}

                Question: {question}

                Answer (include page citations):"""
        
        # Get response from Claude
        response = self.client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=1000,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        answer = response.content[0].text
        
        # Cache the response
        self.cache[cache_key] = answer
        
        return answer
    
    def _create_cache_key(self, question: str, context_chunks: List[Dict]) -> str:
        """Create a unique cache key."""
        content = question + json.dumps([c['text'] for c in context_chunks])
        return hashlib.md5(content.encode()).hexdigest()
    
    def _prepare_context_with_citations(self, context_chunks: List[Dict]) -> str:
        """Prepare context with page citations."""
        context_parts = []
        for i, chunk in enumerate(context_chunks, 1):
            context_parts.append(
                f"[Page {chunk['page']}] {chunk['text']}"
            )
        return "\n\n".join(context_parts)