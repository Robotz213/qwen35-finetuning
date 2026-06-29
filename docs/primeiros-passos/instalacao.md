# Instalacao

Abra o PowerShell e entre no projeto:

```powershell
cd C:\Github\qwen35-finetuning
```

Crie e ative um ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Atualize o `pip`:

```powershell
pip install --upgrade pip
```

Instale as dependencias:

```powershell
pip install -r requirements.txt
```

## PyTorch e CUDA

Se voce for treinar com GPU NVIDIA, instale uma versao do PyTorch compativel com sua versao de CUDA.

Consulte:

```text
https://pytorch.org/get-started/locally/
```

## Hugging Face

Alguns modelos podem exigir autenticacao. Crie um arquivo `.env` com base em `.env.example`:

```powershell
Copy-Item .env.example .env
```

Edite o `.env`:

```text
HF_TOKEN=seu_token_aqui
WANDB_PROJECT=qwen35-finetuning
```

Se necessario, faca login pelo terminal:

```powershell
huggingface-cli login
```

## Rodar a documentacao

```powershell
mkdocs serve
```

Abra:

```text
http://127.0.0.1:8000
```
