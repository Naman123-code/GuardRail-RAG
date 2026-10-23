import os
from dotenv import load_dotenv
from google import genai
from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer

load_dotenv()

client = QdrantClient(path="./qdrant_data")
model = SentenceTransformer("all-MiniLM-L6-v2")
gemini = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

question = "What does COUNT(*) do in SQL?"
MIN_SIMILARITY_SCORE = 0.35

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
    print("Tenant:", point.payload["tenant_id"])
    print("Allowed roles:", point.payload["allowed_roles"])
    print("Page:", point.payload["page_number"])
    print("Text:", point.payload["text"][:200])
    print("---")

relevant_points = [
    point
    for point in search_results.points
    if point.score >= MIN_SIMILARITY_SCORE
]

if not relevant_points:
    print("No authorized document chunks found.")
else:
    context = ""

    for point in relevant_points:
        context += (
            f"Source: {point.payload['document_id']}, "
            f"Page: {point.payload['page_number']}\n"
        )
        context += point.payload["text"] + "\n\n"

    print("Retrieved context prepared.")
    print(context[:1000])

    prompt = f"""
    Answer the question using only the context below.
Cite supporting sources using their document ID and page number.
If the context is insufficient, clearly say you cannot answer
based on the provided documents.

    Context:
    {context}

    Question:
    {question}
    """

    response = gemini.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
    )

    print("\nGemini's Answer:")
    print(response.text)

client.close()