# Qwen3.5 Fine-Tuning

Documentacao do projeto para fine-tuning de modelos Qwen3.5 com LoRA/QLoRA e geracao de contexto a partir de PDFs, planilhas, documentos Word, textos e JSON.

## O que este projeto faz

1. Cria uma base de contexto a partir de arquivos comuns.
2. Monta prompts com os trechos mais relevantes dessa base.
3. Prepara datasets conversacionais para fine-tuning.
4. Treina adaptadores LoRA/QLoRA.
5. Testa e exporta o modelo ajustado.

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
