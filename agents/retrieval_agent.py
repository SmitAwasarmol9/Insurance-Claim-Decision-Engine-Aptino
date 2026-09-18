# agents/retrieval_agent.py

import chromadb

from sentence_transformers import (
    SentenceTransformer
)

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_collection(
    "insurance_policy"
)

def retrieve_policy(query):

    embedding = model.encode(
        query
    ).tolist()

    results = collection.query(
        query_embeddings=[embedding],
        n_results=5
    )

    return " ".join(
        results["documents"][0]
    )