from qdrant_db import client

client.delete_collection(
    collection_name="document_embeddings"
)

print("Collection deleted!")