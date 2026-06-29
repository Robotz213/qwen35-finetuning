# Estrutura do projeto

```text
qwen35-finetuning/
  configs/
    context_builder.yaml
    train_qwen35_lora.yaml
    train_qwen35_lora_no_bnb.yaml
  context/
    sources/
  data/
    sample_train.jsonl
  docs/
  scripts/
    build_context.py
    make_prompt_with_context.py
    train.py
    infer.py
    merge_lora.py
  src/
    context_builder.py
    context_search.py
    dataset.py
  outputs/
  mkdocs.yml
  requirements.txt
  README.md
```

## Pastas importantes

- `context/sources`: onde voce coloca os arquivos que a IA deve usar como base.
- `outputs/context`: onde o gerador salva o contexto processado.
- `data`: onde ficam datasets de fine-tuning.
- `configs`: onde ficam as configuracoes.
- `scripts`: comandos executaveis do projeto.
- `src`: codigo reutilizavel usado pelos scripts.
- `outputs`: resultados gerados, checkpoints, contextos e prompts.
- `docs`: documentacao usada pelo MkDocs.
