from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

client = QdrantClient(path="./qdrant_data")

collections = client.get_collections()

collection_names = [
    collection.name
    for collection in collections.collections
]

if "document_embeddings" not in collection_names:
    client.create_collection(
        collection_name="document_embeddings",
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    )