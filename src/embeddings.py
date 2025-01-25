import numpy as np
from sentence_transformers import SentenceTransformer

def load_model():
    """
    Load the sentence-transformers model.
    """
    return SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(data, model):
    """
    Generate embeddings for each item in the dataset.
    """
    for item in data:
        # Convert the question text into an embedding
        embedding = model.encode(item["question"])
        
        # Convert the NumPy array to float32 and then to a list
        item["embedding"] = embedding.astype(np.float32).tolist()
    
    return data
