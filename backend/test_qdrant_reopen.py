from qdrant_db import client

collections = client.get_collections()

for collection in collections.collections:
    print(collection.name)