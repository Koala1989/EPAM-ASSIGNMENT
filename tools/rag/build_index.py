"""Build the local RAG index over requirements/docs/*.md.

Chunks each doc at every heading (## or ###), the same granularity as
requirements/INDEX.md: a chunk runs from its heading line to the line
before the next heading of any level. Embeds each chunk with a local
sentence-transformers model and stores it in a persisted Chroma
collection at requirements/.rag-index/ (gitignored, rebuild with this
script after any change under requirements/docs/).

Usage:
    python tools/rag/build_index.py
"""

import re
import sys
from pathlib import Path

from sentence_transformers import SentenceTransformer
import chromadb

REPO_ROOT = Path(__file__).resolve().parents[2]
DOCS_DIR = REPO_ROOT / "requirements" / "docs"
INDEX_DIR = REPO_ROOT / "requirements" / ".rag-index"
MODEL_NAME = "all-MiniLM-L6-v2"
COLLECTION_NAME = "inventree_docs_1_5_6"

HEADING_RE = re.compile(r"^(#{2,3})\s+(.*)$")


def chunk_file(path: Path):
    """Yield (heading, start_line, end_line, text) for each ##/### section."""
    lines = path.read_text(encoding="utf-8").splitlines()
    headings = []  # (line_no 1-indexed, level, title)
    for i, line in enumerate(lines, start=1):
        m = HEADING_RE.match(line)
        if m:
            headings.append((i, len(m.group(1)), m.group(2).strip()))

    for idx, (start, _level, title) in enumerate(headings):
        end = headings[idx + 1][0] - 1 if idx + 1 < len(headings) else len(lines)
        text = "\n".join(lines[start - 1 : end]).strip()
        if text:
            yield title, start, end, text


def main():
    if not DOCS_DIR.is_dir():
        print(f"No docs directory at {DOCS_DIR}", file=sys.stderr)
        sys.exit(1)

    doc_files = sorted(p for p in DOCS_DIR.glob("*.md"))
    if not doc_files:
        print(f"No .md files found under {DOCS_DIR}", file=sys.stderr)
        sys.exit(1)

    ids, texts, metadatas = [], [], []
    for path in doc_files:
        rel = f"docs/{path.name}"
        for title, start, end, text in chunk_file(path):
            ids.append(f"{rel}#L{start}")
            texts.append(f"{title}\n\n{text}")
            metadatas.append(
                {
                    "file": rel,
                    "heading": title,
                    "start_line": start,
                    "end_line": end,
                }
            )

    print(f"Chunked {len(doc_files)} files into {len(ids)} chunks.")

    print(f"Loading embedding model '{MODEL_NAME}' (first run downloads it locally)...")
    model = SentenceTransformer(MODEL_NAME)
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True).tolist()

    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(INDEX_DIR))
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    collection = client.create_collection(
        COLLECTION_NAME, metadata={"hnsw:space": "cosine"}
    )

    batch = 100
    for i in range(0, len(ids), batch):
        collection.add(
            ids=ids[i : i + batch],
            embeddings=embeddings[i : i + batch],
            documents=texts[i : i + batch],
            metadatas=metadatas[i : i + batch],
        )

    print(f"Indexed {len(ids)} chunks into {INDEX_DIR} (collection '{COLLECTION_NAME}').")


if __name__ == "__main__":
    main()
