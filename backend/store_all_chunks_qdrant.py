from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams,
    Distance,
    PointStruct
)

from sentence_transformers import SentenceTransformer

from database import SessionLocal
from models import DocumentChunk

db = SessionLocal()

chunks = db.query(DocumentChunk).all()

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

points = []

for chunk in chunks:

    embedding = model.encode(
        chunk.chunk_text
    )

    point = PointStruct(
        id=chunk.id,
        vector=embedding.tolist(),
        payload={
            "chunk_id": chunk.id,
            "document_id": chunk.document_id,
            "text": chunk.chunk_text
        }
    )

    points.append(point)

client.upsert(
    collection_name="document_embeddings",
    points=points
)

print(
    f"{len(points)} vectors stored successfully!"
)