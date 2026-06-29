from __future__ import annotations

import argparse
import sys
from pathlib import Path

import torch
import yaml
from peft import LoraConfig
from transformers import AutoModelForMultimodalLM, AutoProcessor, BitsAndBytesConfig
from trl import SFTConfig, SFTTrainer

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.dataset import load_jsonl_chat_dataset, validate_messages


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fine-tune Qwen3.5 with LoRA/QLoRA.")
    parser.add_argument("--config", required=True, help="Path to YAML training config.")
    return parser.parse_args()


def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def build_quantization_config(config: dict) -> BitsAndBytesConfig | None:
    if not config.get("load_in_4bit", True):
        return None

    compute_dtype = getattr(torch, config.get("bnb_4bit_compute_dtype", "bfloat16"))
    return BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type=config.get("bnb_4bit_quant_type", "nf4"),
        bnb_4bit_compute_dtype=compute_dtype,
        bnb_4bit_use_double_quant=True,
    )


def main() -> None:
    args = parse_args()
    config = load_config(args.config)

    model_name = config["model_name_or_path"]
    output_dir = Path(config["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)

    processor = AutoProcessor.from_pretrained(model_name, trust_remote_code=True)
    tokenizer = getattr(processor, "tokenizer", processor)
    if getattr(tokenizer, "pad_token", None) is None:
        tokenizer.pad_token = tokenizer.eos_token

    dataset = load_jsonl_chat_dataset(config["train_file"])
    dataset = dataset.map(validate_messages)

    quantization_config = build_quantization_config(config)
    model = AutoModelForMultimodalLM.from_pretrained(
        model_name,
        quantization_config=quantization_config,
        device_map="auto",
        trust_remote_code=True,
        torch_dtype=torch.bfloat16 if config.get("bf16", True) else torch.float16,
    )

    if config.get("gradient_checkpointing", True):
        model.config.use_cache = False

    peft_config = LoraConfig(
        r=config.get("lora_r", 16),
        lora_alpha=config.get("lora_alpha", 32),
        lora_dropout=config.get("lora_dropout", 0.05),
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=config.get("lora_target_modules"),
    )

    training_args = SFTConfig(
        output_dir=str(output_dir),
        max_length=config.get("max_seq_length", 2048),
        packing=config.get("packing", False),
        assistant_only_loss=config.get("assistant_only_loss", False),
        num_train_epochs=config.get("num_train_epochs", 1),
        per_device_train_batch_size=config.get("per_device_train_batch_size", 1),
        gradient_accumulation_steps=config.get("gradient_accumulation_steps", 8),
        learning_rate=config.get("learning_rate", 2e-4),
        weight_decay=config.get("weight_decay", 0.0),
        warmup_ratio=config.get("warmup_ratio", 0.03),
        lr_scheduler_type=config.get("lr_scheduler_type", "cosine"),
        logging_steps=config.get("logging_steps", 5),
        save_steps=config.get("save_steps", 100),
        save_total_limit=config.get("save_total_limit", 2),
        bf16=config.get("bf16", True),
        fp16=config.get("fp16", False),
        gradient_checkpointing=config.get("gradient_checkpointing", True),
        optim=config.get("optim", "paged_adamw_8bit"),
        report_to=config.get("report_to", "none"),
        seed=config.get("seed", 42),
    )

    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        processing_class=processor,
        peft_config=peft_config,
    )
    trainer.train()
    trainer.save_model(str(output_dir))
    processor.save_pretrained(str(output_dir))


if __name__ == "__main__":
    main()
