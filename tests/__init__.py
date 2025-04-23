import unittest
from app.document_processor import DocumentProcessor

class TestDocumentProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = DocumentProcessor(chunk_size=100, chunk_overlap=20)
    
    def test_create_chunks(self):
        text = "This is a test document. " * 50  # Create a long text
        chunks = self.processor._create_chunks(text)
        
        # Check if chunks are created
        self.assertGreater(len(chunks), 1)
        
        # Check chunk size
        for chunk in chunks[:-1]:  # All chunks except the last one
            self.assertLessEqual(len(chunk), 100)
        
        # Check overlap
        if len(chunks) > 1:
            overlap = chunks[0][-20:]
            self.assertIn(overlap, chunks[1])

if __name__ == '__main__':
    unittest.main()