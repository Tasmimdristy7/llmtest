from sentence_transformers import SentenceTransformer
import numpy as np

class SemanticSimilarityEvaluator:
    
    def __init__(self, similarity_threshold=0.7):
       
        self.threshold = similarity_threshold
        print("Loading semantic model... (this may take a moment)")
       
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        print("Semantic model loaded!")
        
    def evaluate(self, response, expected_answer):
        
        embeddings = self.model.encode([response, expected_answer])
        response_embedding = embeddings[0]
        expected_embedding = embeddings[1]
        
        similarity = self._cosine_similarity(response_embedding, expected_embedding)
        
        passed = similarity >= self.threshold
        
        if passed:
            message = f"Similar meaning (score: {similarity:.2f})"
        else:
            message = f" Different meaning (score: {similarity:.2f}, needed: {self.threshold})"
        
        return {
            'similarity_score': float(similarity),
            'threshold': float(self.threshold),
            'passed': bool(passed),  # Convert numpy bool to Python bool
            'message': message,
            'response': response,
            'expected': expected_answer
        }
    
    def _cosine_similarity(self, vec1, vec2):
        """Calculate cosine similarity between two vectors."""
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        return dot_product / (norm1 * norm2)