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

text = "Employee salary policy"

embedding = model.encode(text)

client.upsert(
    collection_name="document_embeddings",
    points=[
        PointStruct(
            id=1,
            vector=embedding.tolist(),
            payload={"text": text}
        )
    ]
)

query = "How are employee salaries revised?"

query_embedding = model.encode(query)

results = client.query_points(
    collection_name="document_embeddings",
    query=query_embedding.tolist(),
    limit=1
)

print(results)