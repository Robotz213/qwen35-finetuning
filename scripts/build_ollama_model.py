from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.ollama_builder import create_ollama_model, load_yaml_config, write_modelfile


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate an Ollama Modelfile and optionally create the model.")
    parser.add_argument("--config", default="configs/ollama_model.yaml")
    parser.add_argument("--create", action="store_true", help="Run `ollama create` after writing the Modelfile.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_yaml_config(PROJECT_ROOT / args.config)
    modelfile_path = write_modelfile(config, PROJECT_ROOT)

    print(f"Modelfile generated: {modelfile_path}")
    print(f"Model name: {config['model_name']}")
    print(f"Base model: {config['base_model']}")

    if args.create:
        create_ollama_model(config["model_name"], modelfile_path)
        print(f"Ollama model created: {config['model_name']}")
    else:
        print(f"Create it with: ollama create {config['model_name']} -f {modelfile_path}")


if __name__ == "__main__":
    main()
