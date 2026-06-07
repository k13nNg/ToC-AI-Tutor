import os
import pymupdf4llm as pdf_reader

os.makedirs("data/markdown", exist_ok=True)
for i in range(8, 13):
    input_path = f"data/pdf/Week_{i}.pdf"
    output_path = f"data/markdown/Week_{i}.md"

    md = pdf_reader.to_markdown(input_path)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md)

    print("Saved to:", output_path)