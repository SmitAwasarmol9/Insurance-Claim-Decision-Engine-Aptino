# Import libraries (Import Statement)
import chromadb
from sentence_transformers import SentenceTransformer

# Connect to ChromaDB database (Object Creation)
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_collection("insurance_policy")

# Load embedding model (Object Initialization)
model = SentenceTransformer("all-MiniLM-L6-v2")

# Take user input (Input Function)
disease = input("Enter Disease: ").strip().lower()
days = int(input("Enter Hospitalization Days: "))

# Create query using f-string (String Formatting)
claim_query = f"""
Hospitalization due to {disease} for {days} days.
Is this claim covered?
"""

# Convert query into embeddings (Method Call)
query_embedding = model.encode(claim_query).tolist()

# Search similar policy chunks (Database Query)
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5
)

# Combine retrieved chunks (String Join)
doc = " ".join(results["documents"][0])

print("\nRetrieved Policy Chunks:\n")
print(doc)

# Convert text to lowercase (String Method)
text = doc.lower()

# Default values (Variable Initialization)
decision = "NEED MORE INFORMATION"
reason = "No matching rule found."

# Disease exclusion rules (Dictionary)
disease_rules = {
    "asthma": 3,
    "bronchitis": 3,
    "chronic nephritis": 3,
    "chronic bronchitis": 3
}

# Waiting period diseases (List)
waiting_period_diseases = [
    "cataract",
    "hernia",
    "hydrocele",
    "fistula",
    "myomectomy",
    "hysterectomy",
    "benign prostatic hypertrophy"
]

# Check exclusion rules (For Loop)
for disease_name, max_days in disease_rules.items():

    if disease == disease_name:

        if disease_name in text and "not exceeding three days" in text:

            if days <= max_days:

                decision = "NOT COVERED"
                reason = (
                    f"{disease_name.title()} treatment "
                    f"not exceeding {max_days} days is excluded."
                )

            else:

                decision = "POSSIBLY COVERED"
                reason = (
                    f"{disease_name.title()} hospitalization "
                    f"exceeds {max_days} days."
                )

            break

# Check waiting period rules (For Loop)
for item in waiting_period_diseases:

    if disease == item:

        if "first year" in text:

            decision = "WAITING PERIOD"
            reason = (
                f"{item.title()} is subject to "
                f"first-year waiting period."
            )

            break

# Print final result (Output)
print("\n" + "=" * 60)
print("CLAIM DECISION :", decision)
print("REASON         :", reason)
print("=" * 60)