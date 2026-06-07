from langchain_text_splitters import MarkdownHeaderTextSplitter
from pathlib import Path
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_community.vectorstores import FAISS

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MARKDOWN_FILE_PATH = PROJECT_ROOT / "data" / "markdown"

headers_to_split_on = [("#", "Section"),
                      ("##", "Subsection")]

# open the markdown file
with open(MARKDOWN_FILE_PATH / "Week_5" / "Week_5_content.md", "r", encoding="utf-8") as file:
    markdown_content = file.read()

    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on)
    # embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    documents = markdown_splitter.split_text(markdown_content)

    # vector_db = FAISS.from_documents(documents, embedding_model)
    # vector_db.save_local("faiss_index")
    
    # for i, c in enumerate(documents):
    #     print(f"Chunk {i}:")
    #     print("-" * 5)
    #     print("Chunk metatdata:")
    #     print(c.metadata)
    #     print("-" * 5)
    #     print("Chunk content:")
    #     print(c.page_content)
    #     print("-" * 16)
    max_len = 0
    for doc in documents:
        max_len = max(max_len, len(doc.page_content))

    print("The max length is:", max_len)



