import json
import numpy as np
from sentence_transformers import SentenceTransformer


class SemanticSearch:
    def __init__(self):
        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def create_embedding(self, text):
        embedding = self.model.encode(text)
        return json.dumps(embedding.tolist())

    def load_embedding(self, embedding_text):
        return np.array(json.loads(embedding_text))

    def similarity(self, embedding_a, embedding_b):
        dot_product = np.dot(embedding_a, embedding_b)

        norm_a = np.linalg.norm(embedding_a)
        norm_b = np.linalg.norm(embedding_b)

        if norm_a == 0 or norm_b == 0:
            return 0.0

        return dot_product / (norm_a * norm_b)