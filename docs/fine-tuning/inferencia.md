# Inferencia

Depois do treino, teste o adaptador:

```powershell
python scripts/infer.py --adapter outputs/qwen35-lora --prompt "Explique nossa politica de atendimento."
```

Com system prompt customizado:

```powershell
python scripts/infer.py --adapter outputs/qwen35-lora --system "Voce responde como consultor empresarial." --prompt "Crie um resumo executivo."
```

Controlar tamanho da resposta:

```powershell
python scripts/infer.py --adapter outputs/qwen35-lora --prompt "Resuma o processo" --max-new-tokens 300
```

Controlar criatividade:

```powershell
python scripts/infer.py --adapter outputs/qwen35-lora --prompt "Sugira melhorias" --temperature 0.4
```

Valores menores de `temperature` deixam a resposta mais previsivel. Valores maiores deixam a resposta mais variada.
