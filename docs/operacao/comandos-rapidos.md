# Comandos rapidos

Entrar no projeto:

```powershell
cd C:\Github\qwen35-finetuning
```

Ativar ambiente:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instalar dependencias:

```powershell
pip install -r requirements.txt
```

Rodar documentacao:

```powershell
mkdocs serve
```

Abrir interface grafica do gerador:

```powershell
python scripts/context_gui.py
```

Gerar contexto:

```powershell
python scripts/build_context.py --config configs/context_builder.yaml
```

Criar prompt com contexto:

```powershell
python scripts/make_prompt_with_context.py --question "Minha pergunta aqui"
```

Treinar:

```powershell
python scripts/train.py --config configs/train_qwen35_lora.yaml
```

Treinar sem bitsandbytes:

```powershell
python scripts/train.py --config configs/train_qwen35_lora_no_bnb.yaml
```

Inferir:

```powershell
python scripts/infer.py --adapter outputs/qwen35-lora --prompt "Minha pergunta aqui"
```

Mesclar LoRA:

```powershell
python scripts/merge_lora.py --adapter outputs/qwen35-lora --output outputs/qwen35-merged
```
