from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.context_search import build_prompt, load_chunks, score_chunks


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ask an Ollama model using generated context chunks.")
    parser.add_argument("--model", default="qwen-contexto")
    parser.add_argument("--question", required=True)
    parser.add_argument("--chunks", default="outputs/context/context_chunks.jsonl")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--host", default="http://localhost:11434")
    parser.add_argument("--save-prompt", default="outputs/context/ollama_prompt.md")
    parser.add_argument("--no-call", action="store_true", help="Only write the prompt; do not call Ollama.")
    return parser.parse_args()


def call_ollama(host: str, model: str, prompt: str) -> str:
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }
    request = urllib.request.Request(
        f"{host.rstrip('/')}/api/generate",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=600) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        raise RuntimeError("Nao foi possivel conectar ao Ollama. Confirme se ele esta aberto.") from exc
    return data.get("response", "").strip()


def main() -> None:
    args = parse_args()
    chunks = load_chunks(PROJECT_ROOT / args.chunks)
    ranked = score_chunks(args.question, chunks)
    selected = [chunk for _, chunk in ranked[: args.top_k]]
    if not selected:
        raise ValueError("Nenhum trecho relevante encontrado. Gere o contexto ou refine a pergunta.")

    prompt = build_prompt(args.question, selected)
    prompt_path = PROJECT_ROOT / args.save_prompt
    prompt_path.parent.mkdir(parents=True, exist_ok=True)
    prompt_path.write_text(prompt, encoding="utf-8")
    print(f"Prompt saved: {prompt_path}")

    if args.no_call:
        return

    answer = call_ollama(args.host, args.model, prompt)
    print("\n--- Resposta do Ollama ---\n")
    print(answer)


if __name__ == "__main__":
    main()
