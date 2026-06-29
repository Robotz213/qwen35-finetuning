# Troubleshooting

## Erro: `ModuleNotFoundError`

Instale as dependencias:

```powershell
pip install -r requirements.txt
```

## Erro com PDF, Word ou Excel

Confirme se estas dependencias estao instaladas:

```powershell
pip install pypdf python-docx pandas openpyxl
```

## Erro com `bitsandbytes` no Windows

Use a config sem bitsandbytes:

```powershell
python scripts/train.py --config configs/train_qwen35_lora_no_bnb.yaml
```

Para QLoRA 4-bit, prefira WSL2, Linux ou ambiente cloud com CUDA.

## Falta de memoria na GPU

Tente:

- usar modelo menor;
- reduzir `max_seq_length`;
- manter `per_device_train_batch_size: 1`;
- aumentar `gradient_accumulation_steps`;
- usar QLoRA 4-bit quando possivel.

## O contexto gerado ficou grande demais

Reduza no `configs/context_builder.yaml`:

```yaml
chunk_size: 1200
max_rows_per_sheet: 1000
```

Ou divida os arquivos por assunto e gere bases separadas.

## O prompt trouxe trechos pouco relevantes

Tente uma pergunta mais especifica:

```powershell
python scripts/make_prompt_with_context.py --question "Quais sao os prazos de cancelamento citados no contrato?"
```

Ou aumente `--top-k`:

```powershell
python scripts/make_prompt_with_context.py --question "Quais sao os prazos de cancelamento citados no contrato?" --top-k 10
```
