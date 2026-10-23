from app.document_processor import extract_text_from_pdf
from app.document_processor import chunk_text

pdf_path = "sample.pdf"

pages = extract_text_from_pdf(pdf_path)

all_chunks = []
document_id = "policy_001"

for page in pages:
    chunks = chunk_text(page["text"])

    for chunk in chunks:
        all_chunks.append({
            "text": chunk,
            "page_number": page["page_number"],
            "document_id": document_id,
        })

    #print(f"\nPage {page['page_number']}")
    #rint(f"Number of chunks: {len(chunks)}")
#print(all_chunks[0])  

#  print(pages)



sample_text = "ABCDEFGHIJKL"

chunks = chunk_text(
    sample_text,
    chunk_size=5,
    overlap=2,
)

#print(chunks)

