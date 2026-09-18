from sentence_transformers import SentenceTransformer
import chromadb

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_collection("insurance_policy")

query = "What is the waiting period for cataract surgery?"

query_embedding = model.encode(query).tolist()

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)

for i, doc in enumerate(results["documents"][0], 1):
    print(f"\nResult {i}")
    print("-" * 50)
    print(doc)