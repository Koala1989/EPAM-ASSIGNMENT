"""Query the local RAG index over requirements/docs/*.md.

Used by the test-case-creator agent to retrieve the requirement text
for a functionality instead of reading requirements/docs/*.md directly.
Build the index first with build_index.py.

Usage:
    python tools/rag/query_index.py "<query text>" [--top-k N] [--min-score S]

Prints one block per match, most relevant first:
    <file>#L<start>-L<end> (score=<similarity>)
    <chunk text, exact wording from the source file>
"""

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
INDEX_DIR = REPO_ROOT / "requirements" / ".rag-index"
MODEL_NAME = "all-MiniLM-L6-v2"
COLLECTION_NAME = "inventree_docs_1_5_6"

# Chroma returns cosine distance (0 = identical); chunks above this
# distance are dropped rather than passed off as a relevant match.
MAX_DISTANCE = 0.8
DEFAULT_MIN_SCORE = 1 - MAX_DISTANCE

_model = None
_collection = None


def _load():
    global _model, _collection
    if _collection is None:
        if not INDEX_DIR.is_dir():
            raise FileNotFoundError(
                f"No index at {INDEX_DIR}. Run: python tools/rag/build_index.py"
            )
        from sentence_transformers import SentenceTransformer
        import chromadb

        _model = SentenceTransformer(MODEL_NAME)
        _collection = chromadb.PersistentClient(path=str(INDEX_DIR)).get_collection(
            COLLECTION_NAME
        )
    return _model, _collection


def search(query: str, top_k: int = 5, min_score: float = DEFAULT_MIN_SCORE) -> list[dict]:
    """Return matches as dicts (citation, score, text), most relevant first."""
    model, collection = _load()
    embedding = model.encode([query], convert_to_numpy=True).tolist()
    result = collection.query(query_embeddings=embedding, n_results=top_k)

    hits = []
    for doc, meta, dist in zip(
        result["documents"][0], result["metadatas"][0], result["distances"][0]
    ):
        score = 1 - dist
        if score >= min_score:
            hits.append(
                {
                    "citation": f"{meta['file']}#L{meta['start_line']}-L{meta['end_line']}",
                    "score": score,
                    "text": doc,
                }
            )
    return hits


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="natural-language question or requirement text")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--min-score", type=float, default=DEFAULT_MIN_SCORE,
                        help="drop matches below this similarity (0-1)")
    args = parser.parse_args()

    try:
        hits = search(args.query, args.top_k, args.min_score)
    except FileNotFoundError as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    for hit in hits:
        print(f"{hit['citation']} (score={hit['score']:.2f})")
        print(hit["text"])
        print("---")

    if not hits:
        print(f"No chunk scored >= {args.min_score:.2f} for: {args.query}", file=sys.stderr)
        print("Do not treat this as 'no requirement exists' -- fall back to requirements/INDEX.md "
              "and read the docs directly before writing the case.", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
