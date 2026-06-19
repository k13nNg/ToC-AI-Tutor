from retrieve.context_builder import *
import ollama
import time
import re

LLM_NAME = "llama3.2"

# Patterns that indicate the model leaked internal content
_LEAK_PATTERNS = [
    r"^\s*(Question|Context|Notes|Course notes|Score|Week|Section|Subsection)\s*:",
    r"\[Week\s*:.*?\]",
    r"\[Score\s*:.*?\]",
    r"(system prompt|retrieved (context|material|notes)|RAG|retrieval score)",
    r"as (an AI|a language model|an assistant),?\s+I (don'?t|cannot|can't)",
    r"(Okay|Sure|Got it|Understood|Great).{0,60}(role|question|ask)",
]

_LEAK_RE = re.compile("|".join(_LEAK_PATTERNS), re.IGNORECASE | re.MULTILINE)


def _sanitize(text: str) -> str:
    lines = text.splitlines()
    clean = [line for line in lines if not _LEAK_RE.search(line)]
    result = re.sub(r"\n{3,}", "\n\n", "\n".join(clean)).strip()
    if not result:
        return "I wasn't able to generate a clean answer. Please try rephrasing your question."
    return result


def ask_llm(query, chat_history):
    t0 = time.time()

    context = build_context(query, k=2)

    with open("retrieve/prompt.txt", "r", encoding="utf-8") as f:
        system_prompt = f.read()

    messages = [
        {"role": "system", "content": system_prompt},
        *chat_history[-4:],
        {"role": "user", "content": f"{query}\n\n{context}"}
    ]

    t1 = time.time()

    response = ollama.chat(
        model=LLM_NAME,
        messages=messages
    )

    print("Generation:", time.time() - t1)
    print("Total:", time.time() - t0)
    print("-" * 16)

    raw = response["message"]["content"]
    return _sanitize(raw)
