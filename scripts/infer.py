from __future__ import annotations

import argparse

import torch
from peft import PeftModel
from transformers import AutoModelForMultimodalLM, AutoProcessor


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run inference with a Qwen3.5 LoRA adapter.")
    parser.add_argument("--adapter", required=True, help="Path to trained LoRA adapter.")
    parser.add_argument("--base-model", default=None, help="Base model. Defaults to adapter metadata when possible.")
    parser.add_argument("--prompt", required=True, help="User prompt.")
    parser.add_argument("--system", default="Voce e um assistente util.", help="System message.")
    parser.add_argument("--max-new-tokens", type=int, default=512)
    parser.add_argument("--temperature", type=float, default=0.7)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    base_model = args.base_model

    if base_model is None:
        from peft import PeftConfig

        base_model = PeftConfig.from_pretrained(args.adapter).base_model_name_or_path

    processor = AutoProcessor.from_pretrained(args.adapter, trust_remote_code=True)
    tokenizer = getattr(processor, "tokenizer", processor)
    model = AutoModelForMultimodalLM.from_pretrained(
        base_model,
        device_map="auto",
        torch_dtype=torch.bfloat16,
        trust_remote_code=True,
    )
    model = PeftModel.from_pretrained(model, args.adapter)
    model.eval()

    messages = [
        {"role": "system", "content": [{"type": "text", "text": args.system}]},
        {"role": "user", "content": [{"type": "text", "text": args.prompt}]},
    ]
    inputs = processor.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_dict=True,
        return_tensors="pt",
    ).to(model.device)

    with torch.no_grad():
        generated = model.generate(
            **inputs,
            max_new_tokens=args.max_new_tokens,
            do_sample=args.temperature > 0,
            temperature=args.temperature,
            pad_token_id=tokenizer.eos_token_id,
        )

    completion = generated[0][inputs["input_ids"].shape[-1] :]
    print(tokenizer.decode(completion, skip_special_tokens=True).strip())


if __name__ == "__main__":
    main()
