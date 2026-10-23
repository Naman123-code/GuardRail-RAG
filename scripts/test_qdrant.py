from qdrant_client import QdrantClient, models

client = QdrantClient(":memory:")

client.create_collection(
    collection_name="test_collection",
    vectors_config=models.VectorParams(
        size=2,
        distance=models.Distance.COSINE,
    ),
)

print("Collection created successfully!")

client.upsert(
    collection_name="test_collection",
    points=[
        models.PointStruct(
            id=1,
            vector=[0.25, 0.80],
            payload={
                "text": "Employees receive annual leave."
            },
        )
    ],
)

print("Point inserted successfully!")

result = client.retrieve(
    collection_name="test_collection",
    ids=[1],
    with_payload=True,
    with_vectors=True,
)

print(result)