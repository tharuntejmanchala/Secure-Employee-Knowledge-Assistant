from database import SessionLocal
from models import DocumentChunk

from qdrant_db import client

from sentence_transformers import SentenceTransformer

from qdrant_client.models import PointStruct

db = SessionLocal()

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

chunks = db.query(DocumentChunk).all()

points = []

for chunk in chunks:

    embedding = model.encode(
        chunk.chunk_text
    )

    points.append(
        PointStruct(
            id=chunk.id,
            vector=embedding.tolist(),
            payload={
                "chunk_id": chunk.id,
                "document_id": chunk.document_id,
                "text": chunk.chunk_text
            }
        )
    )

client.upsert(
    collection_name="document_embeddings",
    points=points
)

print(
    f"{len(points)} vectors stored!"
)

db.close()