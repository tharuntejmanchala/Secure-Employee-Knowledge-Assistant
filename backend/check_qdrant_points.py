from qdrant_db import client

info = client.get_collection(
    "document_embeddings"
)

print(info.points_count)