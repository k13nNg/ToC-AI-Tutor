# 🧠 ToC AI Tutor

A **Retrieval-Augmented Generation (RAG)** chatbot that serves as an AI teaching assistant for a **Theory of Computation** course. Students can ask questions in natural language and receive accurate, context-grounded answers drawn directly from the course lecture slides — not hallucinated out of thin air.

---

## Introduction

Theory of Computation is a notoriously abstract course. Concepts like Turing machines, pushdown automata, and context-free grammars are hard to look up quickly, and office hours can't always be available at 2 AM before an exam. This project builds a conversational tutor that has read the actual course material and can answer questions grounded in it.

The system ingests weekly lecture PDFs (Weeks 0–12, excluding Week 7 which is a reading week), converts them to structured Markdown, indexes them with both dense and sparse retrieval methods, and serves answers through a chat interface powered by a large language model. The tutor follows the course material as its primary source of truth — if the retrieved content and the model's prior knowledge conflict, the retrieved material wins.

---

## Pipeline Overview

```
    PDF Slides
        │
        ▼
┌────────────────────┐
│   PDF Parser       │  pymupdf4llm → Markdown
└───────┬────────────┘
        │
        ▼
┌─────────────────────┐
│   Indexer           │  Split by Markdown headers (#, ##)
│                     │  → Chunks with Week / Section / Subsection metadata
│                     ├──► Dense Index  (FAISS + nomic-embed-text embeddings)
│                     └──► Sparse Index (BM25 corpus, pickled)
└─────────────────────┘

    At query time:
        │
        ▼
┌────────────────────┐
│  Query Expansion   │  Abbreviation → full term
│  (built-in)        │  e.g. "NFA" → "nondeterministic finite automaton"
└───────┬────────────┘
        │
    ┌───┴────┐
    ▼         ▼
 Dense      Sparse
 Retrieve   Retrieve
 (FAISS)    (BM25)
    │         │
    └────┬────┘
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
│  LLM                │  llama-3.2 (or llama-3.3-70b-versatile) + system prompt
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Streamlit UI       │  Multi-turn chat with session memory
└─────────────────────┘
```

---

## System Architecture

### 1. Data Processing (`data_processing/pdf_parser.py`)
Weekly lecture PDFs are converted to Markdown using **pymupdf4llm**. This preserves the document's heading structure, which is critical for the next step.

### 2. Ingestion & Indexing (`ingest/indexer.py`)
The Markdown files are split by headers using LangChain's `MarkdownHeaderTextSplitter`. Each chunk gets tagged with its `Week`, `Section`, and `Subsection`. Two indices are built in parallel:

- **Dense index** — chunks are embedded with `nomic-embed-text` (via Ollama) and stored in a **FAISS** `IndexFlatIP` (inner product / cosine similarity). Embeddings and integer IDs are stored together in an `IndexIDMap`. An accompanying **SQLite** database maps each ID back to its text and metadata.
- **Sparse index** — a **BM25Okapi** model is built over the preprocessed corpus and serialized to disk as a pickle file.

### 3. Retrieval (`retrieve/hybrid_retriever.py`)

At query time the retriever runs both indices in parallel:

- **Dense retrieval**: the query is embedded with the same `nomic-embed-text` model, L2-normalized, and searched against the FAISS index.
- **Sparse retrieval**: the query is tokenized and scored with BM25.

Before either search, a lightweight **query expansion** step expands common abbreviations (DFA, NFA, TM, PDA, CFG) to their full forms so that both the embedding model and BM25 have the best possible signal to work with.

### 4. Reciprocal Rank Fusion (RRF)

RRF combines the two ranked lists without needing calibrated scores from either. For each document the formula is:

$$
\text{RRF\_score}(d) = \sum_{i} w_i \cdot \frac{1}{k + \text{rank}_i(d)}
$$

where $k = 60$ is a smoothing constant that dampens the advantage of the very top rank, $\text{rank}_i(d)$ is the document's position in ranked list $i$, and $w_i$ is configurable via the `DENSE_TO_SPARSE_RATIO` parameter (default $w_{\text{dense}} = w_{\text{sparse}} = 0.5$). The documents are then re-sorted by their fused scores and the top-k are passed downstream.

RRF is used here because:
- Dense retrieval is good at semantic similarity ("what is a machine that accepts all strings?").
- Sparse retrieval is good at exact keyword matching ("BM25", "δ transition function").
- Neither score is directly comparable; RRF sidesteps that problem by only caring about rank position, not raw score magnitude.

### 5. Context Building (`retrieve/context_builder.py`)
The top-k doc IDs from RRF are looked up in SQLite to retrieve full text and metadata. Each chunk is formatted with its Week, Section, Subsection, and score as a header block, then concatenated into a single context string.

### 6. LLM Generation (`retrieve/llm.py`)
The context string, the system prompt (`retrieve/prompt.txt`), and up to the last few turns of chat history are assembled into a messages array and sent to the LLM. The model is instructed to:
- Treat retrieved material as the primary source of truth.
- Answer clearly and at the appropriate level of detail.
- Never expose internal metadata, retrieval scores, or the existence of a RAG system.

### 7. Chat Interface (`app.py`)
A **Streamlit** app renders the full conversation history and feeds each new user message through the pipeline. Session state persists the chat across turns.

---

## Project Structure

```
ToC-AI-Tutor/
├── app.py                        # Streamlit chat UI
├── main.py                       # Quick CLI test harness
├── environment.yml               # Conda environment
│
├── data_processing/
│   └── pdf_parser.py             # PDF → Markdown conversion
│
├── ingest/
│   └── indexer.py                # Build FAISS + BM25 + SQLite indices
│
├── retrieve/
│   ├── hybrid_retriever.py       # Dense + sparse retrieval + RRF
│   ├── context_builder.py        # Fetch chunks and format context
│   ├── llm.py                    # LLM call (Groq)
│   └── prompt.txt                # System prompt for the tutor
│
├── stores/
│   ├── vector_store.py           # FAISS wrapper
│   └── metadata_store.py        # SQLite wrapper
│
└── data/
    ├── pdf/                      # Raw lecture PDFs (Week 0–12)
    ├── markdown/                 # Parsed Markdown files
    ├── dense/
    │   ├── faiss/                # faiss_index.index
    │   └── sql/                  # docs_metadata.db
    └── sparse/
        └── bm25_corpus.pkl       # Serialized BM25 corpus
```

---

## Setup

### Prerequisites
- [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or Anaconda
- [Ollama](https://ollama.com/) (for local embedding generation during indexing)
- A [Groq](https://console.groq.com/) API key

### 1. Create the environment
```bash
conda env create -f environment.yml
conda activate ToC_chatbot_env
pip install streamlit langchain langchain-ollama langchain-text-splitters \
            rank-bm25 faiss-cpu pymupdf4llm groq
```

### 2. Pull the embedding model
```bash
ollama pull nomic-embed-text
```

### 3. Set your Groq API key
Replace the `api_key` value in `retrieve/llm.py`, or preferably export it as an environment variable:
```bash
export GROQ_API_KEY="your_key_here"
```

### 4. Build the indices (one-time)
```bash
python -c "
from ingest.indexer import load_documents, build_dense_indices, build_sparse_corpus
docs = load_documents()
print(build_dense_indices(docs))
print(build_sparse_corpus(docs))
"
```

### 5. Run the app
```bash
streamlit run app.py
```

---

## Performance & Known Limitations

### ⚠️ Compute Bottleneck — Why We Moved to Groq

Early versions of this project ran the LLM locally using **Ollama** (`llama3.2`). The performance was disappointing:

| Environment | Hardware | Response Time |
|---|---|---|
| MacBook (local) | Apple Silicon / CPU | **10–17 seconds** |
| Linux server | Beefy RAM, CPU-only | **30–32 seconds** |

The bottleneck in both cases is **CPU memory bandwidth, not RAM**. LLM token generation (the decode phase) is an inherently memory-bound workload. On every single forward pass the model must stream all of its weights from memory into the compute units — for a 70B parameter model at FP16 that is ~140 GB of data moved *per token*. The rate at which this can happen is capped entirely by the memory bus, not by how much RAM is installed or how many CPU cores are available.

This is well established in the literature. DigitalOcean's engineering team notes that ["LLM inference is fundamentally stateful, bottlenecked by memory bandwidth rather than raw compute"](https://www.digitalocean.com/blog/llm-inference-tradeoffs). A detailed roofline analysis (Spheron, 2026) shows that at batch size 1, autoregressive decode has an arithmetic intensity of roughly **1–2 FLOPs per byte** — compared to an H100's roofline ridge of ~591 FLOPs/byte, placing decode operations roughly 300–600× below the compute-bound threshold, meaning [adding FLOPS does nothing to improve token throughput](https://www.spheron.network/blog/ai-memory-wall-inference-latency-guide-2026/). This is independently confirmed in peer-reviewed work: Guo et al. (2025) find that even in large-batch settings, inference ["remains memory-bound, with most GPU compute capabilities underutilized due to DRAM bandwidth saturation as the primary bottleneck"](https://arxiv.org/html/2503.08311v2).

A CPU compounds this problem severely. A high-end desktop CPU offers roughly **50–100 GB/s** of memory bandwidth, compared to **3.35 TB/s** on an H100 SXM5 — a ~35–67× gap. The CPU is not slow because it lacks RAM; it is slow because it cannot move the data fast enough, regardless of how much RAM you give it.

The solution is to **offload inference to a provider with GPU hardware** rather than pay the cost of local CPU inference. We migrated to **[Groq](https://groq.com/)**, which runs inference on their custom LPU (Language Processing Unit) silicon. The result is sub-second time-to-first-token with no local GPU required.

**Current model:** `llama-3.3-70b-versatile` via Groq API  
**Embedding model:** `nomic-embed-text` via Ollama (embeddings are only needed at index-build time and are fast even on CPU)

### Other Limitations
- **No Week 7** — reading week has no lecture content; questions about topics exclusively covered that week may return weak results.
- **Static index** — adding new material requires re-running the full ingestion pipeline.
- **Groq rate limits** — the free tier has token-per-minute limits that may throttle heavy usage.
- **Abbreviation expansion is manual** — the `QUERY_EXPANSIONS` dictionary covers common acronyms (DFA, NFA, TM, PDA, CFG) but does not handle all possible abbreviations a student might use.

---

## Tech Stack

| Component | Library / Service |
|---|---|
| PDF parsing | `pymupdf4llm` |
| Text splitting | LangChain `MarkdownHeaderTextSplitter` |
| Embeddings | `nomic-embed-text` via Ollama |
| Dense index | FAISS (`IndexFlatIP` + `IndexIDMap`) |
| Sparse index | `rank-bm25` (BM25Okapi) |
| Metadata store | SQLite (`sqlite3`) |
| Rank fusion | Custom weighted RRF |
| LLM | `llama-3.3-70b-versatile` via Groq |
| UI | Streamlit |

---

## License

This project is for educational use. Course material is the property of the respective instructors and institution.
