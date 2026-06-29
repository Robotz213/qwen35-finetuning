# Merge LoRA

O treino salva apenas o adaptador LoRA. Para criar um modelo consolidado:

```powershell
python scripts/merge_lora.py --adapter outputs/qwen35-lora --output outputs/qwen35-merged
```

Use merge quando:

- voce quer publicar um modelo unico;
- voce quer usar o modelo em uma ferramenta que nao carrega adaptadores;
- voce quer simplificar deploy.

Nao e obrigatorio fazer merge. Muitas vezes e melhor manter modelo base + adaptador.
