# Prompt com contexto

Depois de gerar `context_chunks.jsonl`, voce pode criar um prompt pronto com os trechos mais relevantes para uma pergunta.

Exemplo:

```powershell
python scripts/make_prompt_with_context.py --question "Qual e a politica de reembolso?"
```

Saida:

```text
outputs/context/prompt.md
```

Esse arquivo tera:

- instrucao para a IA;
- pergunta;
- trechos mais relevantes encontrados nos documentos.

## Controlar quantidade de trechos

```powershell
python scripts/make_prompt_with_context.py --question "Liste os produtos com garantia" --top-k 8
```

## Usar outro arquivo de chunks

```powershell
python scripts/make_prompt_with_context.py --chunks outputs/minha-base/context_chunks.jsonl --question "Resumo dos contratos"
```
