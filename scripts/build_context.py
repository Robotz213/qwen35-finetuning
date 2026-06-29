from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.context_builder import (
    SUPPORTED_EXTENSIONS,
    build_context_chunks,
    write_jsonl,
    write_manifest,
    write_markdown_pack,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build context packs from PDFs, spreadsheets and text files.")
    parser.add_argument("--config", default="configs/context_builder.yaml", help="Path to YAML config.")
    parser.add_argument("--source-dir", default=None, help="Override source directory.")
    parser.add_argument("--output-dir", default=None, help="Override output directory.")
    return parser.parse_args()


def load_config(path: str) -> dict:
    config_path = Path(path)
    if not config_path.exists():
        return {}

    try:
        import yaml
    except ModuleNotFoundError:
        print("PyYAML is not installed; using built-in defaults and CLI overrides.")
        return {}

    with open(path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def main() -> None:
    args = parse_args()
    config = load_config(args.config)

    source_dir = Path(args.source_dir or config.get("source_dir", "context/sources"))
    output_dir = Path(args.output_dir or config.get("output_dir", "outputs/context"))
    include_extensions = {
        extension.lower()
        for extension in config.get("include_extensions", sorted(SUPPORTED_EXTENSIONS))
    }

    if not source_dir.exists():
        raise FileNotFoundError(f"Source directory does not exist: {source_dir}")

    chunks = build_context_chunks(
        source_dir=source_dir,
        include_extensions=include_extensions,
        chunk_size=config.get("chunk_size", 1800),
        chunk_overlap=config.get("chunk_overlap", 250),
        max_rows_per_sheet=config.get("max_rows_per_sheet", 5000),
    )

    if not chunks:
        print(f"No supported files found in {source_dir}.")
        return

    write_jsonl(chunks, output_dir / "context_chunks.jsonl")
    write_markdown_pack(
        chunks,
        output_dir / "context_pack.md",
        title=config.get("context_title", "Knowledge base"),
        default_instruction=config.get("default_instruction", ""),
    )
    write_manifest(chunks, output_dir / "manifest.json")

    print(f"Context generated from {source_dir}")
    print(f"Chunks: {len(chunks)}")
    print(f"Output: {output_dir}")


if __name__ == "__main__":
    main()
