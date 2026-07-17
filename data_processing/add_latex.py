"""
add_latex.py

Post-processes all markdown content files in data/markdown/ to wrap
mathematical expressions in LaTeX delimiters ($...$).

Writes output to data/markdown_latex/ — originals are never modified.

Run from repo root:
    python data_processing/add_latex.py
"""

import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MARKDOWN_DIR = PROJECT_ROOT / "data" / "markdown"
OUTPUT_DIR   = PROJECT_ROOT / "data" / "markdown_latex"

# ---------------------------------------------------------------------------
# Rules applied only to plain-text (non-math) segments of each line.
# Order matters: more specific rules first.
# Each entry: (compiled_pattern, replacement_string)
# ---------------------------------------------------------------------------

RULES = [
    # --- Greek / special symbols ---
    (re.compile(r'(?<![A-Za-z\\])Σ(?![A-Za-z])'),   r'$\\Sigma$'),
    (re.compile(r'(?<![A-Za-z\\])Γ(?![A-Za-z])'),   r'$\\Gamma$'),
    (re.compile(r'(?<![A-Za-z\\])ε(?![A-Za-z])'),    r'$\\varepsilon$'),
    (re.compile(r'(?<![A-Za-z\\])δ(?![A-Za-z(])'),   r'$\\delta$'),
    (re.compile(r'∅'),                                 r'$\\emptyset$'),
    (re.compile(r'∪'),                                 r'$\\cup$'),
    (re.compile(r'∩'),                                 r'$\\cap$'),
    (re.compile(r'[∘◦]'),                              r'$\\circ$'),
    (re.compile(r'∈'),                                 r'$\\in$'),
    (re.compile(r'∉'),                                 r'$\\notin$'),
    (re.compile(r'⊆'),                                 r'$\\subseteq$'),
    (re.compile(r'⊂'),                                 r'$\\subset$'),
    (re.compile(r'⊔'),                                 r'$\\sqcup$'),
    (re.compile(r'⟨'),                                 r'$\\langle$'),
    (re.compile(r'⟩'),                                 r'$\\rangle$'),
    (re.compile(r'⇒'),                                 r'$\\Rightarrow$'),
    (re.compile(r'→'),                                 r'$\\to$'),

    # --- State names: q0, q1, qaccept, qreject, qa, qr ---
    # Also handle "q 0", "q 1" (space between q and number from PDF parsing)
    (re.compile(r'\bq(accept|reject|start|loop|end)\b'), r'$q_{\\text{\1}}$'),
    (re.compile(r'\bq\s+([0-9]+)\b'),                  r'$q_{\1}$'),
    (re.compile(r'\bq([0-9]+)\b'),                     r'$q_{\1}$'),
    (re.compile(r'\bq([a-z])\b'),                      r'$q_{\1}$'),

    # --- Superscripts: x^n, 0^n, A^* ---
    (re.compile(r'([A-Za-z0-9])\^([A-Za-z0-9*]+)'),   r'$\1^{\2}$'),

    # --- Subscripts: x_0, r_i ---
    (re.compile(r'([A-Za-z])_([A-Za-z0-9]+)'),        r'$\1_{\2}$'),

    # --- Kleene star: A*, B* ---
    (re.compile(r'(?<![A-Za-z\\])([A-Z])\*'),          r'$\1^*$'),

    # --- Inequalities: n ≥ 0, i ≤ p ---
    (re.compile(r'([A-Za-z])\s*≥\s*([0-9]+)'),        r'$\1 \\geq \2$'),
    (re.compile(r'([A-Za-z])\s*≤\s*([0-9]+)'),        r'$\1 \\leq \2$'),

    # --- Length expressions: |y| > 0 ---
    (re.compile(r'\|([A-Za-z]+)\|\s*([><=]+)\s*([A-Za-z0-9]+)'), r'$|\1| \2 \3$'),

    # --- L(M), L(G) ---
    (re.compile(r'\bL\s*\(\s*([A-Za-z][0-9]?)\s*\)'), r'$L(\1)$'),
]


def split_math_nonmath(line: str):
    """
    Split line into alternating segments: [plain, math, plain, math, ...]
    Returns list of (text, is_math) tuples.
    """
    segments = []
    # Match both inline $...$ and display $$...$$
    pattern = re.compile(r'(\$\$.*?\$\$|\$[^$\n]+?\$)', re.DOTALL)
    last = 0
    for m in pattern.finditer(line):
        if m.start() > last:
            segments.append((line[last:m.start()], False))
        segments.append((m.group(), True))
        last = m.end()
    if last < len(line):
        segments.append((line[last:], False))
    return segments


def process_line(line: str) -> str:
    segments = split_math_nonmath(line)
    result = []
    for text, is_math in segments:
        if is_math:
            result.append(text)
        else:
            for pattern, replacement in RULES:
                text = pattern.sub(replacement, text)
            result.append(text)
    return "".join(result)


def process_file(path: Path) -> None:
    original = path.read_text(encoding="utf-8")
    lines = original.splitlines()
    processed = []
    in_code_block = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            processed.append(line)
            continue
        if in_code_block or stripped.startswith("    "):
            processed.append(line)
            continue
        processed.append(process_line(line))

    text = "\n".join(processed)

    relative = path.relative_to(MARKDOWN_DIR)
    out_path = OUTPUT_DIR / relative
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")
    print(f"Written: {out_path.relative_to(PROJECT_ROOT)}")


def main():
    md_files = sorted(MARKDOWN_DIR.rglob("*_content.md"))
    print(f"Found {len(md_files)} content files.")
    print(f"Output: {OUTPUT_DIR.relative_to(PROJECT_ROOT)}\n")
    for f in md_files:
        process_file(f)
    print("\nDone. Point indexer.py at data/markdown_latex/ and rebuild the index.")


if __name__ == "__main__":
    main()
