from __future__ import annotations

import argparse

import torch
from peft import PeftConfig, PeftModel
from transformers import AutoModelForMultimodalLM, AutoProcessor


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Merge a LoRA adapter into its Qwen3.5 base model.")
    parser.add_argument("--adapter", required=True, help="Path to trained LoRA adapter.")
    parser.add_argument("--output", required=True, help="Output path for merged model.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    peft_config = PeftConfig.from_pretrained(args.adapter)

    processor = AutoProcessor.from_pretrained(args.adapter, trust_remote_code=True)
    model = AutoModelForMultimodalLM.from_pretrained(
        peft_config.base_model_name_or_path,
        device_map="auto",
        torch_dtype=torch.bfloat16,
        trust_remote_code=True,
    )
    model = PeftModel.from_pretrained(model, args.adapter)
    model = model.merge_and_unload()

    model.save_pretrained(args.output, safe_serialization=True)
    processor.save_pretrained(args.output)


if __name__ == "__main__":
    main()
