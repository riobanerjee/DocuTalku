from anthropic import Anthropic
from typing import List

class QAEngine:
    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)
    
    def generate_answer(self, question: str, context_chunks: List[str]) -> str:
        """Generate an answer using Claude based on the context."""
        # Combine context chunks
        context = "\n\n".join(context_chunks)
        
        # Create prompt
        prompt = f"""Based on the following context from a document, please answer the question. 
                    If the answer cannot be found in the context, say so.

                    Context:
                    {context}

                    Question: {question}

                    Answer:"""
                            
        # Get response from Claude
        response = self.client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=1000,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        return response.content[0].text