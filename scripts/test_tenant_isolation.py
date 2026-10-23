from qdrant_client import QdrantClient, models

client = QdrantClient(path="./qdrant_data")

results = client.scroll(
    collection_name="document_chunks",
    scroll_filter=models.Filter(
        must=[
            models.FieldCondition(
                key="tenant_id",
                match=models.MatchValue(value=2),
            )
        ]
    ),
    limit=10,
    with_payload=True,
)

points, _ = results

print("Chunks visible to tenant 2:", len(points))

for point in points:
    print("Tenant ID:", point.payload["tenant_id"])

role_results = client.scroll(
    collection_name="document_chunks",
    scroll_filter=models.Filter(
        must=[
            models.FieldCondition(
                key="tenant_id",
                match=models.MatchValue(value=1),
            ),
            models.FieldCondition(
                key="allowed_roles",
                match=models.MatchValue(value="manager"),
            ),
        ]
    ),
    limit=10,
    with_payload=True,
)

role_points, _ = role_results

print("Chunks visible to manager:", len(role_points))

client.close()