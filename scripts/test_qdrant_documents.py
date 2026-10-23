from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer
from app.document_processor import extract_text_from_pdf, chunk_text

client = QdrantClient(path="./qdrant_data")

if not client.collection_exists("document_chunks"):
    client.create_collection(
        collection_name="document_chunks",
        vectors_config=models.VectorParams(
            size=384,
            distance=models.Distance.COSINE,
        ),
    )

print("Document collection created!")

pages = extract_text_from_pdf("sample.pdf")

all_chunks = []
document_id = "policy_001"

for page in pages:
    chunks = chunk_text(page["text"])

    for chunk in chunks:
        all_chunks.append({
            "text": chunk,
            "page_number": page["page_number"],
            "document_id": document_id,
            "tenant_id": 1,
            "allowed_roles": ["admin", "intern"],
        })

model = SentenceTransformer("all-MiniLM-L6-v2")

texts = [chunk["text"] for chunk in all_chunks]
embeddings = model.encode(texts)

#print("Chunks:", len(all_chunks))
#print("Embeddings:", len(embeddings))
#print("Dimensions:", embeddings.shape[1])

points = []

for i, chunk in enumerate(all_chunks):
    points.append(
        models.PointStruct(
            id=i,
            vector=embeddings[i].tolist(),
            payload={
                "text": chunk["text"],
                "page_number": chunk["page_number"],
                "document_id": chunk["document_id"],
                "tenant_id": chunk["tenant_id"],
                "allowed_roles": chunk["allowed_roles"],
            },
        )
    )

client.upsert(
    collection_name="document_chunks",
    points=points,
)

question = "How much annual leave do employees receive?"

query_vector = model.encode(question).tolist()

search_results = client.query_points(
    collection_name="document_chunks",
    query=query_vector,
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
    limit=3,
    with_payload=True,
)


for point in search_results.points:
    print("\nSimilarity score:", point.score)
    print("Page:", point.payload["page_number"])
    print("Text:", point.payload["text"][:300])

print("Points inserted:", len(points)) 
client.close()