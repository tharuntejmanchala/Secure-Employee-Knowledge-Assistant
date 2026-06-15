from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

client = QdrantClient(":memory:")

client.create_collection(
    collection_name="document_embeddings",
    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE
    )
)

print("Collection created successfully!")