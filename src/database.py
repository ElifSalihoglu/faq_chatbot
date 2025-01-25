import pinecone
from pinecone import Pinecone, ServerlessSpec
import hashlib  # For generating unique ASCII-compliant IDs


def init_pinecone(api_key, environment, index_name, dimension):
    """
    Initialize Pinecone and create an index if it doesn't already exist.
    """
    pc = Pinecone(api_key=api_key)
    
    # Check if the index exists; if not, create it
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=dimension,  # Embedding dimension
            metric='cosine',  # Using cosine similarity
            spec=ServerlessSpec(cloud="aws", region=environment)
        )
    
    # Return the initialized index
    return pc.Index(index_name)


def upsert_data(data, index):
    """
    Upload data to Pinecone.
    - data: [{'question': str, 'answer': str, 'embedding': list}, ...]
    - index: Pinecone.Index instance
    """
    upsert_items = []
    for item in data:
        # Generate a unique and ASCII-compliant ID
        vector_id = hashlib.sha256(item["question"].encode("utf-8")).hexdigest()

        # Prepare data for upsert
        upsert_items.append({
            "id": vector_id,
            "values": item["embedding"],
            "metadata": {
                "question": item["question"],
                "answer": item["answer"]
            }
        })

    # Bulk upload to Pinecone
    index.upsert(vectors=upsert_items)


def query_index(query_embedding, index, top_k=1):
    """
    Perform a query on the Pinecone index to retrieve the closest match.
    - query_embedding: Embedding of the user's query
    - index: Pinecone.Index instance
    - top_k: Number of top matches to retrieve
    """
    return index.query(query_embedding, top_k=top_k, include_metadata=True)
