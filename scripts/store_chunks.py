from sentence_transformers import SentenceTransformer
import chromadb

with open("policy_text.txt", "r", encoding="utf-8") as file:
    text = file.read()

chunk_size = 1000
chunks = []

for i in range(0, len(text), chunk_size):
    chunks.append(text[i:i + chunk_size])

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="insurance_policy"
)

for i, chunk in enumerate(chunks):
    embedding = model.encode(chunk).tolist()

    collection.add(
        ids=[str(i)],
        embeddings=[embedding],
        documents=[chunk]
    )

print(f"Stored {len(chunks)} chunks successfully!")