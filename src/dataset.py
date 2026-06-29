from __future__ import annotations

from pathlib import Path
from typing import Any

from datasets import Dataset, load_dataset


def load_jsonl_chat_dataset(path: str | Path) -> Dataset:
    dataset = load_dataset("json", data_files=str(path), split="train")
    if "messages" not in dataset.column_names:
        raise ValueError("Dataset must contain a 'messages' column with chat messages.")
    return dataset


def validate_messages(example: dict[str, Any]) -> dict[str, Any]:
    messages = example.get("messages")
    if not isinstance(messages, list) or not messages:
        raise ValueError("Each example must have a non-empty messages list.")

    for message in messages:
        if not isinstance(message, dict):
            raise ValueError("Each message must be an object.")
        if message.get("role") not in {"system", "user", "assistant", "tool"}:
            raise ValueError(f"Invalid role: {message.get('role')!r}")
        content = message.get("content")
        if isinstance(content, str):
            if not content.strip():
                raise ValueError("String content cannot be empty.")
            message["content"] = [{"type": "text", "text": content}]
            continue

        if not isinstance(content, list) or not content:
            raise ValueError("Content must be a string or a non-empty multimodal content list.")

        for item in content:
            if not isinstance(item, dict) or item.get("type") != "text":
                raise ValueError("This starter expects text-only content items: {'type': 'text', 'text': ...}.")
            if not isinstance(item.get("text"), str) or not item["text"].strip():
                raise ValueError("Text content items must have non-empty text.")

    return example
