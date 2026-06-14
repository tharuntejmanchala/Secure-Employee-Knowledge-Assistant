from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

chunk = "Employee salary policy"

embedding = model.encode(chunk)

print(type(embedding))

print(len(embedding))

print(embedding[:10])