"""
Converts data/json/Week_*.json  →  data/train.jsonl

Handles two formats that may exist in the JSON files:

Format A (old) — flat question/answer keys:
  {"question": "...", "answer": "..."}

Format B (new) — messages format:
  {"messages": [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}

Both are normalised to the messages format for training.
"""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
JSON_DIR     = PROJECT_ROOT / "data" / "json"
OUTPUT_FILE  = PROJECT_ROOT / "data" / "train.jsonl"


def normalise(pair: dict) -> dict | None:
    """Return a messages-format dict or None if the pair is invalid."""

    # Format B — already correct
    if "messages" in pair:
        msgs = pair["messages"]
        if (
            len(msgs) == 2
            and msgs[0].get("role") == "user"
            and msgs[1].get("role") == "assistant"
            and msgs[0].get("content", "").strip()
            and msgs[1].get("content", "").strip()
        ):
            return {"messages": msgs}
        return None

    # Format A — flat question/answer
    question = pair.get("question", "").strip()
    answer   = pair.get("answer", "").strip()
    if not question or not answer:
        return None

    # Strip the Step 1/Step 2/Takeaway boilerplate that crept into old data.
    # Sentences that start with "Step N:" or "Takeaway:" are structural filler,
    # not real answers — remove them so the model doesn't learn that pattern.
    import re
    clean_sentences = []
    for sentence in re.split(r'(?<=[.!?])\s+', answer):
        if re.match(r'^(Step\s+\d+:|Takeaway:)', sentence.strip()):
            # Keep the content after the label
            content = re.sub(r'^(Step\s+\d+:|Takeaway:)\s*', '', sentence.strip())
            if content:
                clean_sentences.append(content)
        else:
            clean_sentences.append(sentence.strip())

    clean_answer = " ".join(clean_sentences).strip()

    return {
        "messages": [
            {"role": "user",      "content": question},
            {"role": "assistant", "content": clean_answer},
        ]
    }


records = []
skipped = 0

for json_file in sorted(JSON_DIR.glob("Week_*.json")):
    with open(json_file, "r", encoding="utf-8") as f:
        pairs = json.load(f)

    for pair in pairs:
        result = normalise(pair)
        if result:
            records.append(result)
        else:
            skipped += 1

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for record in records:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

print(f"Wrote {len(records)} examples to {OUTPUT_FILE.relative_to(PROJECT_ROOT)}")
if skipped:
    print(f"Skipped {skipped} malformed entries")
