from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.context_search import build_prompt, load_chunks, score_chunks


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a prompt using the generated context chunks.")
    parser.add_argument("--chunks", default="outputs/context/context_chunks.jsonl")
    parser.add_argument("--question", required=True)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--output", default="outputs/context/prompt.md")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    chunks_path = Path(args.chunks)
    output_path = Path(args.output)

    chunks = load_chunks(chunks_path)
    ranked = score_chunks(args.question, chunks)
    selected = [chunk for _, chunk in ranked[: args.top_k]]

    if not selected:
        raise ValueError("No relevant chunks found. Try a more specific question or rebuild the context.")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_prompt(args.question, selected), encoding="utf-8")
    print(f"Prompt generated: {output_path}")


if __name__ == "__main__":
    main()
