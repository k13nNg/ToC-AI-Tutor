import chromadb
import pymupdf
import re
import ollama
import uuid

temp = 10

heading_pattern = re.compile(r'^\d+(\.\d+)*\s')

client = chromadb.PersistentClient(path="./chroma_data")

collection = client.get_or_create_collection(name="lessons")

topics_list = open("topics_list.txt", "r")

def get_pdf_path(week):
    return f"./knowledge_base/notes/Week_{week}.pdf"

def merge_split_headings(lines, week):
    merged = []
    skip_next = False

    for i, line in enumerate(lines):
        if skip_next:
            skip_next = False
            continue

        # Since each section is indexed by week, we will look for lines in the form of
        # "week" or "week.some_digit"
        if re.match(r"^\d+(\.\d+)*$", line.strip()) and str(week) in line:
            # Merge with the next line if available
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                merged.append(f"{line.strip()} {next_line}")
                skip_next = True
            else:
                merged.append(line.strip())
        else:
            merged.append(line.strip())

    return merged

doc = pymupdf.open(get_pdf_path(temp))

sections = []
current_section = None

for page in doc:
    text = page.get_text("text")  # extract page as plain text
    lines = text.split('\n')
    merged_lines = merge_split_headings(lines, temp)
    
    for line in merged_lines:
        if heading_pattern.match(line):
            # Start of a new section
            if current_section:
                sections.append(current_section)
            current_section = {
                "title": line.strip(),
                "content": ""
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

# Now 'sections' contains structured chunks
for s in sections:
    print("TITLE:", s["title"])
    print("CONTENT PREVIEW:", s["content"], "\n---\n")

        