from qdrant_db import client

results = client.query_points(
    collection_name="document_embeddings",
    query=[0.0] * 384,
    limit=3,
    with_payload=True
)

for point in results.points:
    print(point.payload)