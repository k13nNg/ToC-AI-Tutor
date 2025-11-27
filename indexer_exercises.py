import chromadb
import pymupdf
import re
import uuid
import ollama

client = chromadb.PersistentClient(path="./chroma_data")
client.delete_collection(name="exercises")
collection = client.create_collection(name="exercises")

def get_pdf_path(week):
    return f"./knowledge_base/exercises/Week_{week}.pdf"

chunks= []
for week in range(0,14):
    if (week != 7):
        doc = pymupdf.open(get_pdf_path(week))

        current_chunk = None

        for page in doc:
            text = page.get_text("text")
            lines = text.split("\n")

            for line in lines:
                if (re.match(r"^\d+\.(\d+)*", line.strip())) and str(week) in line:
                    # remove the question number
                    modified_line = re.sub(r"^\d+\.(\d+)*", "", line.strip())

                    if current_chunk:
                        chunks.append(current_chunk)

                    current_chunk = {
                        "title": f"Week {str(week)}",
                        "content": modified_line.strip() + " "
                    }
                else:
                    if current_chunk:
                        current_chunk["content"] += line + " "

            # Append the last section
            if current_chunk:
                chunks.append(current_chunk)

content_chunks = [c["content"] for c in chunks]
metadata = [{"Week": c["title"]} for c in chunks]
chunk_ids = [str(uuid.uuid4()) for _ in chunks]

chunk_embeddings = ollama.embed(model="embeddinggemma", input=content_chunks)

collection.add(ids = chunk_ids,
               embeddings=chunk_embeddings["embeddings"],
               documents=content_chunks,
               metadatas=metadata)

print("Exercises indexing process complete.")