# 🧠 Decidr — ToC AI Tutor

**Decidr** is a Retrieval-Augmented Generation (RAG) chatbot that serves as an AI teaching assistant for **INFO 47546 – Theory of Computation** at Sheridan College. Students can ask questions in natural language and receive accurate, context-grounded answers drawn directly from the course lecture notes.

---

## System Architecture

```
    PDF Slides
        │
        ▼
┌────────────────────┐
│   PDF Parser       │  pymupdf4llm → Markdown
└───────┬────────────┘
        │
        ▼
┌────────────────────┐
│   LaTeX Processor  │  add_latex.py → Markdown with LaTeX
└───────┬────────────┘
        │
        ▼
┌─────────────────────┐
│   Indexer           │  Split by Markdown headers (#, ##)
│                     │  → Chunks with Week / Section / Subsection metadata
│                     ├──► Dense Index  (FAISS + nomic-embed-text embeddings + SQLite)
│                     └──► Sparse Index (BM25 corpus, pickled)
└─────────────────────┘

    At query time:
        │
        ▼
┌────────────────────┐
│  Query Router      │  llama3.2 classifies: on_topic / greeting / off_topic
└───────┬────────────┘
        │ on_topic
        ▼
┌────────────────────┐
│  Query Expansion   │  Abbreviation → full term (NFA, DFA, TM, PDA, CFG)
└───────┬────────────┘
        │
    ┌───┴────┐
    ▼        ▼
 Dense     Sparse
 Retrieve  Retrieve
 (FAISS)   (BM25)
    │        │
    └────┬───┘
         ▼
┌─────────────────────┐
│   RRF Fusion        │  Weighted Reciprocal Rank Fusion
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Context Builder    │  Fetch chunk text + metadata from SQLite
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  LLM Generation     │  llama3.2 via Ollama + system prompt + chat history
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Streamlit UI       │  Streaming chat with session memory + suggestion chips
└─────────────────────┘
```

---

## Component Breakdown

### 1. Data Processing (`data_processing/`)

- **`pdf_parser.py`** — converts weekly lecture PDFs (Weeks 0–12, excluding Week 7 which is reading week) to Markdown using `pymupdf4llm`, preserving heading structure.
- **`add_latex.py`** — post-processes Markdown files to wrap mathematical expressions in LaTeX delimiters (`$...$`, `$$...$$`). Outputs to `data/markdown_latex/` without modifying originals.

### 2. Ingestion & Indexing (`RAG/ingest/indexer.py`)

Markdown files from `data/markdown_latex/` are split by headers using LangChain's `MarkdownHeaderTextSplitter`. Each chunk is tagged with `Week`, `Section`, and `Subsection` metadata. Two indices are built:

- **Dense index** — chunks are embedded with `nomic-embed-text` (via Ollama) and stored in a FAISS `IndexFlatIP` + `IndexIDMap`. An accompanying SQLite database maps each ID to its text and metadata.
- **Sparse index** — a BM25Okapi model is built over the preprocessed corpus and serialized to disk.

Run `python main.py` to clear old artifacts and rebuild all indices from scratch.

### 3. Retrieval (`RAG/retrieve/hybrid_retriever.py`)

At query time, both indices are searched in parallel:

- **Dense retrieval** — query is embedded with `nomic-embed-text` and searched against FAISS.
- **Sparse retrieval** — query is tokenized and scored with BM25.

A **query expansion** step runs first, expanding abbreviations (DFA → "deterministic finite automaton", NFA → "nondeterministic finite automaton", etc.) to improve signal for both retrievers.

### 4. Reciprocal Rank Fusion (`RAG/retrieve/hybrid_retriever.py`)

RRF merges the two ranked lists:

$$\text{RRF}(d) = \sum_{i} w_i \cdot \frac{1}{k + \text{rank}_i(d)}$$

where $k=60$ is a smoothing constant and weights are configurable via `DENSE_TO_SPARSE_RATIO` (default 0.5). Top-k results are passed downstream.

### 5. Context Builder (`RAG/retrieve/context_builder.py`)

Top-k doc IDs are fetched from SQLite with full text and metadata. Each chunk is formatted with Week, Section, Subsection, and score, then concatenated into a context string.

### 6. Query Router (`RAG/retrieve/query_router.py`)

Before retrieval, every query is classified by llama3.2 into one of three routes:

- `on_topic` → proceed with RAG pipeline
- `greeting` → return hardcoded Decidr introduction
- `off_topic` → return hardcoded decline message

The router receives the last 4 messages of chat history so it can correctly classify follow-up questions.

### 7. LLM Generation (`RAG/retrieve/llm.py`)

The context, system prompt (`RAG/retrieve/prompt.txt`), and last 4 turns of chat history are assembled and sent to llama3.2 via Ollama with streaming enabled. Tokens are yielded as they arrive.

### 8. Chat Interface (`app.py`)

A Streamlit app with:
- Floating fixed header with the Decidr branding
- Suggestion chips on startup (hidden after first message)
- Streaming response with cursor indicator
- Session memory across turns
- Model warmup on startup via `@st.cache_resource`

---

## Project Structure

```
ToC-AI-Tutor/
├── app.py                          # Streamlit chat UI
├── main.py                         # Index rebuild script
├── environment.yml                 # Conda environment
│
├── data_processing/
│   ├── pdf_parser.py               # PDF → Markdown
│   ├── add_latex.py                # Markdown → Markdown with LaTeX
│   └── prepare_finetune_data.py    # Fine-tuning data preparation
│
├── RAG/
│   ├── ingest/
│   │   └── indexer.py              # Build FAISS + BM25 + SQLite indices
│   │
│   ├── retrieve/
│   │   ├── hybrid_retriever.py     # Dense + sparse retrieval + RRF
│   │   ├── context_builder.py      # Fetch chunks and format context
│   │   ├── query_router.py         # LLM-based query classifier
│   │   ├── llm.py                  # Streaming LLM call via Ollama
│   │   └── prompt.txt              # System prompt for Decidr
│   │
│   └── stores/
│       ├── vector_store.py         # FAISS wrapper
│       └── metadata_store.py       # SQLite wrapper
│
└── data/
    ├── pdf/                        # Raw lecture PDFs (Week 0–12)
    ├── markdown/                   # Parsed Markdown (original)
    ├── markdown_latex/             # Markdown with LaTeX (processed)
    ├── dense/
    │   ├── faiss/                  # faiss_index.index
    │   └── sql/                    # docs_metadata.db
    └── sparse/
        └── bm25_corpus.pkl         # Serialized BM25 corpus
```

---

## Installation

### Prerequisites

- [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or Anaconda
- [Ollama](https://ollama.com/)

### 1. Clone the repository

```bash
git clone https://github.com/k13nNg/ToC-AI-Tutor.git
cd ToC-AI-Tutor
```

### 2. Create the conda environment

```bash
conda env create -f environment.yml
conda activate ToC_chatbot_env
```

### 3. Install Python dependencies

```bash
pip install streamlit langchain langchain-ollama langchain-text-splitters \
            rank-bm25 faiss-cpu pymupdf4llm
```

### 4. Pull required Ollama models

```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

---

## Development Setup

### 1. Process PDFs to Markdown (if starting from raw PDFs)

```bash
python data_processing/pdf_parser.py
```

### 2. Add LaTeX formatting to Markdown

```bash
python data_processing/add_latex.py
```

Output goes to `data/markdown_latex/`. Review a few files to verify the conversion looks correct before indexing.

### 3. Build the indices

```bash
python main.py
```

This clears any existing FAISS index, SQLite DB, and BM25 corpus, then rebuilds all three from `data/markdown_latex/`.

### 4. Run the app

The bottleneck in both cases is **CPU memory bandwidth, not RAM**. LLM token generation (the decode phase) is an inherently memory-bound workload. On every single forward pass the model must stream all of its weights from memory into the compute units — for a 70B parameter model at FP16 that is ~140 GB of data moved *per token*. The rate at which this can happen is capped entirely by the memory bus, not by how much RAM is installed or how many CPU cores are available.

This is well established in the literature. DigitalOcean's engineering team notes that ["LLM inference is fundamentally stateful, bottlenecked by memory bandwidth rather than raw compute"](https://www.digitalocean.com/blog/llm-inference-tradeoffs). A detailed roofline analysis (Spheron, 2026) shows that at batch size 1, autoregressive decode has an arithmetic intensity of roughly **1–2 FLOPs per byte** — compared to an H100's roofline ridge of ~591 FLOPs/byte, placing decode operations roughly 300–600× below the compute-bound threshold, meaning [adding FLOPS does nothing to improve token throughput](https://www.spheron.network/blog/ai-memory-wall-inference-latency-guide-2026/). This is independently confirmed in peer-reviewed work: Guo et al. (2025) find that even in large-batch settings, inference ["remains memory-bound, with most GPU compute capabilities underutilized due to DRAM bandwidth saturation as the primary bottleneck"](https://arxiv.org/html/2503.08311v2).

A CPU compounds this problem severely. A high-end desktop CPU offers roughly **50–100 GB/s** of memory bandwidth, compared to **3.35 TB/s** on an H100 SXM5 — a ~35–67× gap. The CPU is not slow because it lacks RAM; it is slow because it cannot move the data fast enough, regardless of how much RAM you give it.

### Re-indexing

Any time you update the Markdown source files, re-run:

```bash
python data_processing/add_latex.py
python main.py
```

---

## Tech Stack

| Component | Library / Service |
|---|---|
| PDF parsing | `pymupdf4llm` |
| Text splitting | LangChain `MarkdownHeaderTextSplitter` |
| Embeddings | `nomic-embed-text` via Ollama |
| Dense index | FAISS (`IndexFlatIP` + `IndexIDMap`) |
| Metadata store | SQLite (`sqlite3`) |
| Sparse index | `rank-bm25` (BM25Okapi) |
| Rank fusion | Weighted RRF (custom) |
| Query routing | llama3.2 via Ollama |
| LLM generation | llama3.2 via Ollama (streaming) |
| UI | Streamlit |

---

## Known Limitations

- **No Week 7** — reading week has no lecture content; queries about topics only in that week may return weak results.
- **Static index** — adding new material requires re-running the ingestion pipeline.
- **Small model hallucination** — llama3.2 3B occasionally ignores the "use only course notes" instruction, especially for well-known topics. Using a larger model significantly reduces this.
- **Abbreviation expansion is manual** — the `QUERY_EXPANSIONS` dictionary covers common acronyms but does not handle all possible student shorthand.

---

## License

This project is for educational use. Course material is the property of the respective instructors and Sheridan College.
