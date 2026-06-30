# Criar modelo customizado

O arquivo principal e:

```text
configs/ollama_model.yaml
```

Ele define:

- nome do modelo local;
- modelo base do Ollama;
- parametros de geracao;
- system prompt;
- exemplos fixos;
- caminho opcional para adapter.

## Gerar Modelfile

Na raiz do projeto:

```powershell
python scripts/build_ollama_model.py --config configs/ollama_model.yaml
```

Saida padrao:

```text
ollama/Modelfile
```

## Criar modelo no Ollama

```powershell
ollama create qwen-contexto -f ollama/Modelfile
```

Ou gere e crie em um comando:

```powershell
python scripts/build_ollama_model.py --config configs/ollama_model.yaml --create
```

## Testar modelo

```powershell
ollama run qwen-contexto
```

## Alterar modelo base

Edite:

```yaml
base_model: qwen3:0.6b
```

Exemplos:

```yaml
base_model: qwen3:1.7b
```

ou:

```yaml
base_model: llama3.2:1b
```

Use modelos pequenos se estiver sem GPU.

## Usar adapter LoRA

O `Modelfile` suporta `ADAPTER`, mas o adapter precisa estar pronto e compativel com o modelo base.

No `configs/ollama_model.yaml`:

```yaml
adapter_path: outputs/meu-adapter.gguf
```

Para CPU/16 GB RAM, prefira primeiro o fluxo sem adapter: contexto + system prompt.
