# Visao geral

O projeto tem tres objetivos principais:

1. Criar uma base de contexto a partir de arquivos como PDFs, planilhas, documentos Word, textos e JSON.
2. Rodar um modelo local pelo Ollama com `Modelfile` e contexto.
3. Fazer fine-tuning de um modelo Qwen3.5 usando LoRA ou QLoRA quando houver ambiente adequado.

Essas duas partes se complementam, mas nao sao a mesma coisa:

- Contexto serve para a IA consultar informacoes de documentos.
- Fine-tuning serve para ensinar formato, estilo, comportamento, padroes de resposta e tarefas repetitivas.

Na pratica, use contexto para conhecimento documental, Ollama para servir o modelo local e fine-tuning para comportamento quando voce tiver hardware ou ambiente cloud adequado.

## Componentes principais

- Gerador de contexto: transforma arquivos em Markdown e JSONL com chunks.
- Montador de prompt: busca trechos relevantes no contexto gerado.
- Ollama: cria modelo customizado via `Modelfile` e consulta a API local.
- Dataset de treino: exemplos conversacionais em JSONL.
- Treinamento LoRA/QLoRA: adapta o modelo sem treinar todos os pesos.
- Inferencia e merge: testa o adaptador e, se necessario, exporta um modelo consolidado.
