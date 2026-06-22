from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams,
    Distance,
    PointStruct
)

from sentence_transformers import SentenceTransformer

client = QdrantClient(":memory:")

client.create_collection(
    collection_name="document_embeddings",
    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE
    )
)

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

texts = [
    "Employee salary policy",
    "Leave policy",
    "Travel reimbursement policy"
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

question = "How are employee salaries reviewed?"

query_embedding = model.encode(question)

results = client.query_points(
    collection_name="document_embeddings",
    query=query_embedding.tolist(),
    limit=1
)

print(results.points[0].payload["text"])