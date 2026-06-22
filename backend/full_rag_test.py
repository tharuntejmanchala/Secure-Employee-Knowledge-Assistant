from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams,
    Distance,
    PointStruct
)

from sentence_transformers import SentenceTransformer
import ollama

# Model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Qdrant
client = QdrantClient(":memory:")

client.create_collection(
    collection_name="document_embeddings",
    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE
    )
)

# Sample chunks
texts = [
    "Employees receive annual salary reviews based on performance evaluations.",
    "Employees are entitled to 20 days of annual leave.",
    "Travel expenses must be approved by the manager."
]

points = []

for i, text in enumerate(texts, start=1):
    embedding = model.encode(text)

    points.append(
        PointStruct(
            id=i,
            vector=embedding.tolist(),
            payload={"text": text}
        )
    )

client.upsert(
    collection_name="document_embeddings",
    points=points
)

# User Question
question = "How are employee salaries reviewed?"

# Query Embedding
query_embedding = model.encode(question)

# Retrieve Top 3 Chunks
results = client.query_points(
    collection_name="document_embeddings",
    query=query_embedding.tolist(),
    limit=3
)

context = "\n".join(
    point.payload["text"]
    for point in results.points
)

# Prompt
prompt = f"""
Answer the question using only the context below.

Context:
{context}

Question:
{question}

Answer:
"""

# LLM
response = ollama.chat(
    model="llama3.2:3b",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

print(response["message"]["content"])