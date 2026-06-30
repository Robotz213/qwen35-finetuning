# Contexto vs Fine-tuning

Use contexto quando:

- a informacao muda com frequencia;
- voce precisa consultar documentos longos;
- voce quer preservar numeros, nomes, datas e clausulas;
- voce nao quer retreinar o modelo a cada atualizacao.

Use fine-tuning quando:

- voce quer padronizar estilo de resposta;
- voce quer ensinar um fluxo de atendimento;
- voce quer ensinar formatos fixos;
- voce quer melhorar comportamento em tarefas repetidas;
- voce tem bons exemplos de entrada e saida.

Evite treinar o modelo para memorizar documentos. Isso fica caro, dificil de atualizar e menos confiavel que usar contexto.

## Com Ollama

Quando usar Ollama, pense em tres camadas:

- contexto: documentos processados pelo gerador;
- Modelfile: comportamento, parametros e exemplos fixos;
- LoRA adapter: opcional e avancado, apenas se ja tiver um adapter compativel.

Para uso local em CPU, contexto + Modelfile costuma ser a melhor combinacao.
