from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

text = "Employees receive 20 days of annual leave."

embedding = model.encode(text)

#print(embedding)
#print("Embedding dimensions:", len(embedding))

from app.document_processor import extract_text_from_pdf, chunk_text

pages = extract_text_from_pdf("sample.pdf")

all_chunks = []

for page in pages:
    chunks = chunk_text(page["text"])

    for chunk in chunks:
        all_chunks.append({
            "text": chunk,
            "page_number": page["page_number"],
            "document_id": "policy_001",
        })

texts = [chunk["text"] for chunk in all_chunks]
embeddings = model.encode(texts)

print("Number of embeddings:", len(embeddings))
print("Dimensions per embedding:", embeddings.shape[1])