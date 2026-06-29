from __future__ import annotations

import json
import math
import re
from collections import Counter
from pathlib import Path
from typing import Any


STOPWORDS = {
    "a",
    "as",
    "com",
    "da",
    "das",
    "de",
    "do",
    "dos",
    "e",
    "em",
    "na",
    "nas",
    "no",
    "nos",
    "o",
    "os",
    "para",
    "por",
    "que",
    "um",
    "uma",
}


def tokenize(text: str) -> list[str]:
    tokens = re.findall(r"[\wÀ-ÿ]{3,}", text.lower())
    return [token for token in tokens if token not in STOPWORDS]


def load_chunks(path: Path) -> list[dict[str, Any]]:
    chunks = []
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                chunks.append(json.loads(line))
    return chunks


def score_chunks(query: str, chunks: list[dict[str, Any]]) -> list[tuple[float, dict[str, Any]]]:
    query_terms = Counter(tokenize(query))
    if not query_terms:
        return []

    document_frequency: Counter[str] = Counter()
    chunk_terms: list[Counter[str]] = []
    for chunk in chunks:
        terms = Counter(tokenize(chunk.get("text", "")))
        chunk_terms.append(terms)
        document_frequency.update(terms.keys())

    total_chunks = max(len(chunks), 1)
    scored: list[tuple[float, dict[str, Any]]] = []

    for chunk, terms in zip(chunks, chunk_terms):
        score = 0.0
        for term, query_count in query_terms.items():
            if term not in terms:
                continue
            idf = math.log((total_chunks + 1) / (document_frequency[term] + 1)) + 1
            score += query_count * terms[term] * idf
        if score > 0:
            scored.append((score, chunk))

    return sorted(scored, key=lambda item: item[0], reverse=True)


def build_prompt(query: str, chunks: list[dict[str, Any]]) -> str:
    lines = [
        "# Prompt com contexto",
        "",
        "Responda usando apenas o contexto abaixo quando ele for suficiente. Se o contexto nao trouxer a informacao necessaria, diga isso claramente.",
        "",
        "## Pergunta",
        "",
        query,
        "",
        "## Contexto",
        "",
    ]

    for index, chunk in enumerate(chunks, start=1):
        lines.extend(
            [
                f"### Fonte {index}: {chunk['source_path']} / {chunk['section']}",
                "",
                chunk["text"],
                "",
            ]
        )

    return "\n".join(lines).strip() + "\n"
