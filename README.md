# Qwen3.5 Fine-Tuning Starter

Projeto base para fine-tuning de modelos Qwen3.5 com LoRA/QLoRA usando Hugging Face Transformers, TRL e PEFT.

O Qwen3.5 oficial e tratado como modelo multimodal no Hugging Face. Este starter usa `AutoProcessor` e `AutoModelForMultimodalLM`, mas o dataset de exemplo e apenas texto para deixar o primeiro treino simples.

Documentacao completa em MkDocs:

```powershell
pip install -r requirements.txt
mkdocs serve
```

Depois abra `http://127.0.0.1:8000`.

## Estrutura

```text
qwen35-finetuning/
  mkdocs.yml
  docs/index.md
  configs/train_qwen35_lora.yaml
  configs/context_builder.yaml
  context/sources/
  data/sample_train.jsonl
  scripts/context_gui.py
  scripts/build_context.py
  scripts/train.py
  scripts/infer.py
  scripts/merge_lora.py
  src/context_builder.py
  src/dataset.py
  requirements.txt
  .env.example
  .gitignore
```

## Requisitos

- Python 3.10+
- GPU NVIDIA recomendada
- CUDA/PyTorch compatíveis com sua máquina
- Conta/token do Hugging Face se o modelo ou dataset exigir autenticação

Instalação:

```powershell
cd C:\Github\qwen35-finetuning
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

Se precisar instalar PyTorch com CUDA específica, use o comando recomendado em:

https://pytorch.org/get-started/locally/

## Dataset

O formato esperado é JSONL, uma conversa por linha:

```json
{"messages":[{"role":"system","content":[{"type":"text","text":"Voce e um assistente util."}]},{"role":"user","content":[{"type":"text","text":"Explique LoRA."}]},{"role":"assistant","content":[{"type":"text","text":"LoRA e uma tecnica..."}]}]}
```

Veja `data/sample_train.jsonl`.

## Gerador de contexto

Interface grafica:

```powershell
python scripts/context_gui.py
```

Coloque os arquivos que a IA deve usar como base em:

```text
C:\Github\qwen35-finetuning\context\sources
```

Formatos aceitos:

- PDF: `.pdf`
- Word: `.docx`
- Planilhas: `.xlsx`, `.xls`, `.csv`, `.tsv`
- Texto/dados: `.txt`, `.md`, `.json`, `.jsonl`

Depois gere o pacote de contexto:

```powershell
python scripts/build_context.py --config configs/context_builder.yaml
```

Saidas geradas:

```text
outputs/context/context_pack.md
outputs/context/context_chunks.jsonl
outputs/context/manifest.json
```

Use `context_pack.md` quando quiser colar ou injetar contexto em prompts. Use `context_chunks.jsonl` se for criar busca/RAG, embeddings ou uma etapa posterior de geracao de exemplos.

Voce tambem pode apontar para outra pasta:

```powershell
python scripts/build_context.py --source-dir C:\MeusArquivos\BaseIA --output-dir outputs/minha-base
```

Para montar um prompt com os trechos mais relevantes:

```powershell
python scripts/make_prompt_with_context.py --question "Qual e a politica de reembolso?"
```

Isso cria:

```text
outputs/context/prompt.md
```

## Treinar

Edite `configs/train_qwen35_lora.yaml` conforme sua GPU e dataset, depois execute:

```powershell
python scripts/train.py --config configs/train_qwen35_lora.yaml
```

Os adaptadores LoRA serão salvos em `outputs/qwen35-lora`.

No Windows nativo, `bitsandbytes` pode não estar disponível dependendo da sua instalação. Para evitar isso, use a configuração sem 4-bit:

```powershell
python scripts/train.py --config configs/train_qwen35_lora_no_bnb.yaml
```

Para QLoRA 4-bit, prefira Linux, WSL2 ou um ambiente cloud com CUDA.

## Inferir com o adaptador

```powershell
python scripts/infer.py --adapter outputs/qwen35-lora --prompt "Crie um resumo sobre fine-tuning."
```

## Mesclar LoRA no modelo base

Use apenas se quiser exportar um modelo consolidado:

```powershell
python scripts/merge_lora.py --adapter outputs/qwen35-lora --output outputs/qwen35-merged
```

## Observações práticas

- Para GPUs com pouca VRAM, comece por `Qwen/Qwen3.5-0.8B-Instruct` ou `Qwen/Qwen3.5-2B-Instruct`.
- Para qualidade maior, tente `Qwen/Qwen3.5-4B-Instruct`, `9B` ou `27B`, ajustando batch/gradient accumulation.
- O `assistant_only_loss` fica desativado por padrao porque o TRL bloqueia esse modo em modelos VLM, mesmo quando o dataset e apenas texto.
- Dados reais importam mais que muitas epocas. Comece com exemplos limpos, variados e alinhados ao comportamento desejado.
