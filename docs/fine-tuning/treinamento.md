# Treinamento

O projeto inclui duas configuracoes principais:

```text
configs/train_qwen35_lora.yaml
configs/train_qwen35_lora_no_bnb.yaml
```

Use `train_qwen35_lora.yaml` para QLoRA 4-bit quando o ambiente suportar `bitsandbytes`.

Use `train_qwen35_lora_no_bnb.yaml` no Windows nativo ou quando `bitsandbytes` nao estiver funcionando.

## Treinar com QLoRA

```powershell
python scripts/train.py --config configs/train_qwen35_lora.yaml
```

Saida padrao:

```text
outputs/qwen35-lora
```

## Treinar sem bitsandbytes

```powershell
python scripts/train.py --config configs/train_qwen35_lora_no_bnb.yaml
```

Saida padrao:

```text
outputs/qwen35-lora-no-bnb
```

## Ajustes importantes

No arquivo de treino:

```yaml
model_name_or_path: Qwen/Qwen3.5-4B
train_file: data/sample_train.jsonl
output_dir: outputs/qwen35-lora
```

Se tiver pouca VRAM, reduza:

```yaml
max_seq_length: 1024
per_device_train_batch_size: 1
```

E aumente:

```yaml
gradient_accumulation_steps: 8
```

Se tiver mais VRAM, voce pode testar modelos maiores, batch maior ou sequencias maiores.
