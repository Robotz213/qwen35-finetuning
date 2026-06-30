# Qwen3.5 Fine-Tuning

Documentacao do projeto para uso local com Ollama, geracao de contexto a partir de PDFs, planilhas, documentos Word, textos e JSON, e fine-tuning LoRA/QLoRA quando houver ambiente adequado.

## O que este projeto faz

1. Cria uma base de contexto a partir de arquivos comuns.
2. Monta prompts com os trechos mais relevantes dessa base.
3. Gera um `Modelfile` para criar modelo customizado no Ollama.
4. Pergunta ao Ollama usando contexto local.
5. Opcionalmente prepara datasets e treina adaptadores LoRA/QLoRA fora do Ollama.

## Como rodar a documentacao

Na raiz do projeto:

```powershell
pip install -r requirements.txt
mkdocs serve
```

Depois abra:

```text
http://127.0.0.1:8000
```

## Caminho recomendado

Comece por [Visao geral](primeiros-passos/visao-geral.md), depois leia [Instalacao](primeiros-passos/instalacao.md).

Para gerar contexto, use um destes caminhos:

- [Interface grafica](contexto/interface-grafica.md): melhor para selecionar arquivos, ajustar parametros e gerar prompts visualmente.
- [Gerar contexto pelo CLI](contexto/gerar-contexto.md): melhor para automacao e scripts.

Para usar localmente com Ollama, siga [Fluxo com Ollama](ollama/fluxo-com-ollama.md).
