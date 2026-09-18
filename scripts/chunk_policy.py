with open("policy_text.txt", "r", encoding="utf-8") as file:
    text = file.read()

chunk_size = 1000

chunks = []

for i in range(0, len(text), chunk_size):
    chunks.append(text[i:i + chunk_size])

print("Total Chunks:", len(chunks))

print("\nFirst Chunk:\n")
print(chunks[0])