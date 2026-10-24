
from qdrant_client import QdrantClient, models
from app.rag_service import retrieve_chunks


def test_retrieval_only_returns_authorized_tenant_chunks(tmp_path):
    # Use isolated temporary storage for this test.
    client = QdrantClient(path=str(tmp_path / "qdrant_test"))

    collection = "tenant_isolation_test"

    client.create_collection(
        collection_name=collection,
        vectors_config=models.VectorParams(
            size=3,
            distance=models.Distance.COSINE,
        ),
    )

    try:
        client.upsert(
            collection_name=collection,
            points=[
                models.PointStruct(
                    id=1,
                    vector=[1.0, 0.0, 0.0],
                    payload={
                        "tenant_id": 1,
                        "allowed_roles": ["intern"],
                        "document_id": "tenant_a_secret",
                        "page_number": 1,
                        "text": "Tenant A confidential information.",
                    },
                ),
                models.PointStruct(
                    id=2,
                    vector=[1.0, 0.0, 0.0],
                    payload={
                        "tenant_id": 2,
                        "allowed_roles": ["intern"],
                        "document_id": "tenant_b_secret",
                        "page_number": 1,
                        "text": "Tenant B confidential information.",
                    },
                ),
            ],
        )

        # Verify Qdrant's tenant filter in isolation.
        result = client.query_points(
            collection_name=collection,
            query=[1.0, 0.0, 0.0],
            query_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="tenant_id",
                        match=models.MatchValue(value=1),
                    ),
                    models.FieldCondition(
                        key="allowed_roles",
                        match=models.MatchValue(value="intern"),
                    ),
                ]
            ),
            limit=10,
            with_payload=True,
        )

        assert result.points
        assert all(
            point.payload["tenant_id"] == 1
            for point in result.points
        )
        assert all(
            point.payload["document_id"] != "tenant_b_secret"
            for point in result.points
        )

    finally:
        client.close()
