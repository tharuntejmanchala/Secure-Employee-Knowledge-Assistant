from sentence_transformers import SentenceTransformer
from database import SessionLocal
from models import DocumentChunk

db = SessionLocal()

chunks = db.query(DocumentChunk).all()

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

for chunk in chunks:

    embedding = model.encode(
        chunk.chunk_text
    )

    print("Chunk ID:", chunk.id)

    print(
        "Embedding Length:",
        len(embedding)
    )

    print()