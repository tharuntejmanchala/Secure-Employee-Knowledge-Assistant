from database import SessionLocal
from models import DocumentChunk, Document

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

    document = db.query(Document).filter(
        Document.id == chunk.document_id
    ).first()

    embedding = model.encode(
        chunk.chunk_text
    )

    point = PointStruct(
        id=chunk.id,
        vector=embedding.tolist(),
        payload={
            "chunk_id": chunk.id,
            "document_id": chunk.document_id,
            "role_access": document.role_access,
            "text": chunk.chunk_text
        }
    )

    print(point.payload)   # ADD THIS

    points.append(point)

client.upsert(
    collection_name="document_embeddings",
    points=points
)

print(
    f"{len(points)} vectors stored successfully!"
)

db.close()