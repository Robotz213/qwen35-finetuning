# Treinamento

O projeto inclui duas configuracoes principais:

```text
configs/train_qwen35_lora.yaml
configs/train_qwen35_lora_no_bnb.yaml
configs/train_qwen35_lora_cpu_16gb.yaml
```

Use `train_qwen35_lora.yaml` para QLoRA 4-bit quando o ambiente suportar `bitsandbytes`.

Use `train_qwen35_lora_no_bnb.yaml` no Windows nativo ou quando `bitsandbytes` nao estiver funcionando.

Use `train_qwen35_lora_cpu_16gb.yaml` quando nao tiver placa de video e tiver cerca de 16 GB de RAM.

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

## Treinar em CPU com 16 GB de RAM

```powershell
python scripts/train.py --config configs/train_qwen35_lora_cpu_16gb.yaml
```

Saida padrao:

```text
outputs/qwen35-lora-cpu-16gb
```

Essa configuracao usa:

- modelo pequeno: `Qwen/Qwen3.5-0.8B`;
- `device_map: cpu`;
- `torch_dtype: float32`;
- sequencia curta: `max_seq_length: 512`;
- LoRA pequeno: `lora_r: 4`;
- apenas `q_proj` e `v_proj` como modulos alvo;
- `batch_size: 1`;
- `gradient_accumulation_steps: 16`;
- `optim: adamw_torch`.

Treino em CPU e muito lento. Use primeiro com datasets pequenos para validar o pipeline.

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

Se nao tiver GPU, evite modelos maiores que `0.8B` no primeiro teste.
