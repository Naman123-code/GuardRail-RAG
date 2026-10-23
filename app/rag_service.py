
import os

from dotenv import load_dotenv
from google import genai
from google.genai import errors
from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer

load_dotenv()

# Initialize Gemini
gemini = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Initialize Qdrant
qdrant = QdrantClient(path="./qdrant_data")

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve_chunks(
    question: str,
    tenant_id: int,
    role: str,
    limit: int = 3,
):
    query_vector = embedding_model.encode(question).tolist()

    search_results = qdrant.query_points(
        collection_name="document_chunks",
        query=query_vector,
        query_filter=models.Filter(
            must=[
                models.FieldCondition(
                    key="tenant_id",
                    match=models.MatchValue(value=tenant_id),
                ),
                models.FieldCondition(
                    key="allowed_roles",
                    match=models.MatchValue(value=role),
                ),
            ]
        ),
        limit=limit,
        with_payload=True,
    )

    relevant_chunks = [
        point
        for point in search_results.points
        if point.score >= 0.35
    ]

    return relevant_chunks


def generate_answer(question: str, chunks: list) -> str:
    # Don't call Gemini if no relevant documents were found
    if not chunks:
        return (
            "I couldn't find sufficiently relevant information "
            "in the authorized documents."
        )

    # Build context from retrieved document chunks
    context = ""

    for point in chunks:
        context += (
            f"Source: {point.payload['document_id']}, "
            f"Page: {point.payload['page_number']}\n"
        )
        context += point.payload["text"] + "\n\n"

    # Create the prompt
    prompt = f"""
Answer the question using only the provided document context.
Cite supporting sources using their document ID and page number.
If the context is insufficient, say you cannot answer from these documents.

Document context:
{context}

Question:
{question}
"""

    # Generate an answer using Gemini
    try:
        response = gemini.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
        )

        return response.text or "No answer was generated."

    except errors.ServerError as e:
        print(f"Gemini server error: {e}", flush=True)
        return (
            "The AI service is temporarily unavailable. "
            "Please try again shortly."
        )


def ask_question(
    question: str,
    tenant_id: int,
    role: str,
) -> str:
    chunks = retrieve_chunks(
        question=question,
        tenant_id=tenant_id,
        role=role,
    )

    answer = generate_answer(
        question=question,
        chunks=chunks,
    )

    return answer
