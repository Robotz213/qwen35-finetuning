# Fluxo com Ollama

O Ollama e usado neste projeto para rodar um modelo local e criar uma variante customizada via `Modelfile`.

## Ideia principal

No fluxo Ollama, o projeto faz tres coisas:

1. Gera contexto a partir de PDFs, planilhas, Word, Markdown, JSON e textos.
2. Cria um `Modelfile` com modelo base, parametros e system prompt.
3. Envia perguntas ao Ollama usando os chunks mais relevantes do contexto.

## O que muda em relacao ao LoRA

Ollama nao e o caminho principal para treinar pesos do zero dentro do projeto. O ajuste normal com Ollama e:

- `FROM`: modelo base;
- `PARAMETER`: temperatura, contexto, top-p e outros parametros;
- `SYSTEM`: comportamento padrao;
- `MESSAGE`: exemplos fixos;
- `ADAPTER`: adapter LoRA ja treinado e convertido, quando aplicavel.

Para uma maquina sem placa de video, o caminho recomendado e usar contexto + `Modelfile`.

## Fluxo recomendado

1. Instale e abra o Ollama.
2. Gere contexto pela interface grafica ou CLI.
3. Gere o `Modelfile`.
4. Crie o modelo customizado com `ollama create`.
5. Pergunte usando `ask_ollama_with_context.py`.

## Modelo base

A configuracao padrao usa:

```text
qwen3:0.6b
```

Esse modelo e pequeno e mais adequado para CPU/16 GB RAM. Se sua maquina aguentar, voce pode trocar em `configs/ollama_model.yaml`.
