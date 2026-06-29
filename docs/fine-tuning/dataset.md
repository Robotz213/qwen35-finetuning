# Dataset

O dataset de treino fica em JSONL. Cada linha representa uma conversa.

Exemplo:

```json
{"messages":[{"role":"system","content":[{"type":"text","text":"Voce e um assistente tecnico, claro e objetivo."}]},{"role":"user","content":[{"type":"text","text":"O que e fine-tuning com LoRA?"}]},{"role":"assistant","content":[{"type":"text","text":"Fine-tuning com LoRA ajusta pequenas matrizes treinaveis adicionadas ao modelo base."}]}]}
```

Arquivo de exemplo:

```text
data/sample_train.jsonl
```

## O que colocar no dataset

Use exemplos que mostrem como voce quer que a IA responda:

- tom de voz;
- formato de resposta;
- regras de atendimento;
- padroes juridicos, tecnicos ou comerciais;
- exemplos de perguntas e respostas;
- como lidar com duvidas sem resposta.

Nao use o fine-tuning para simplesmente jogar PDFs inteiros no modelo. Para isso, use o gerador de contexto.

## Boas praticas

- Prefira exemplos curtos e limpos.
- Remova duplicados.
- Evite respostas contraditorias.
- Mantenha o mesmo estilo de resposta.
- Comece pequeno, valide, depois aumente.

Um bom primeiro teste pode ter entre 50 e 300 exemplos bem feitos.
