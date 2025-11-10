import chromadb
import pymupdf
import re
import ollama
import uuid
from rank_bm25 import BM25Okapi
import pickle

client = chromadb.PersistentClient(path="./chroma_data")
client.delete_collection(name="lessons")
collection = client.create_collection(name="lessons")

topics_list = open("topics_list.txt", "r")

headings = {l.strip() for l in topics_list.readlines()}

# store the extracted sections from the pdf
sections = []

def get_pdf_path(week):
    return f"./knowledge_base/notes/Week_{week}.pdf"

def merge_split_headings(lines, week):
    merged = []
    skip_next = False

    for i, line in enumerate(lines):
        if skip_next:
            skip_next = False
            continue

        # since each section is indexed by week, we will look for lines in the form of
        # "week" or "week.some_digit"
        if re.match(r"^\d+(\.\d+)*$", line.strip()) and str(week) in line:
            # merge with the next line if available
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                merged.append(f"{line.strip()} {next_line}")
                skip_next = True
            else:
                merged.append(line.strip())
        else:
            merged.append(line.strip())

    return merged

# extract sections from the pdfs
for week in range(0,14):

    if (week != 7):
        doc = pymupdf.open(get_pdf_path(week))

        current_section = None

        for page in doc:
            text = page.get_text("text")  # extract page as plain text
            lines = text.split('\n')

            merged_lines = merge_split_headings(lines, week)
            
            for line in merged_lines:
                if line in headings:
                    # Start of a new section
                    if current_section:
                        sections.append(current_section)

                    current_section = {
                        "title": line.strip(),
                        "content": line + " "
                    }
                else:
                    if current_section:
                        current_section["content"] += line + " "
                    else:
                        # Handle text before first heading
                        current_section = {
                            "title": "Intro",
                            "content": line + " "
                        }

        # Append the last section
        if current_section:
            sections.append(current_section)

# dense indexing using chroma
processed_sections = [s for s in sections if s["content"].strip()]
chunks = [s["content"] for s in processed_sections]
metadatas = [{"titles": s["title"]} for s in processed_sections]
chunk_ids = [str(uuid.uuid4()) for _ in processed_sections]

section_embeddings = ollama.embed(model="embeddinggemma", input = chunks)

collection.add(
    ids=chunk_ids,
    embeddings=section_embeddings["embeddings"],
    documents=chunks,
    metadatas=metadatas
)

# sparse embedding using bm25
tokenized_corpus = [doc.lower().split(" ") for doc in chunks]
bm25_model = BM25Okapi(tokenized_corpus)
id_map = {i: chunk_ids[i] for i in range(len(chunks))}

with open("bm25_index.pickle", "wb") as f:
    pickle.dump(bm25_model, f)

with open("all_chunks.pickle", "wb") as f:
    pickle.dump(chunks, f)

with open("id_map.pickle", "wb") as f: 
    pickle.dump(id_map, f)

print("Indexing process complete. ID mapping saved for RRF.")