# Perguntar com contexto

Depois de gerar contexto e criar o modelo no Ollama, voce pode fazer perguntas usando os chunks mais relevantes.

## Gerar contexto

Pela interface:

```powershell
python scripts/context_gui.py
```

Ou pelo CLI:

```powershell
python scripts/build_context.py --config configs/context_builder.yaml
```

## Perguntar ao Ollama

```powershell
python scripts/ask_ollama_with_context.py --model qwen-contexto --question "Resuma os documentos principais"
```

O script:

1. Le `outputs/context/context_chunks.jsonl`.
2. Busca os chunks mais relevantes.
3. Monta um prompt com contexto.
4. Salva o prompt em `outputs/context/ollama_prompt.md`.
5. Envia para o Ollama via API local.

## Apenas gerar o prompt

Se quiser revisar antes de chamar o Ollama:

```powershell
python scripts/ask_ollama_with_context.py --model qwen-contexto --question "Quais sao os prazos citados?" --no-call
```

## Controlar quantidade de contexto

```powershell
python scripts/ask_ollama_with_context.py --model qwen-contexto --question "Quais sao os prazos citados?" --top-k 8
```

Use `top-k` maior quando a pergunta depender de varios documentos. Use menor quando quiser respostas mais focadas.
