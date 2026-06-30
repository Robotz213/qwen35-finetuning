# Fluxo recomendado

Um fluxo pratico para usar o projeto:

1. Coloque PDFs, planilhas e documentos em `context/sources`.
2. Rode `python scripts/build_context.py`.
3. Use `make_prompt_with_context.py` para testar perguntas sobre os documentos.
4. Observe quais respostas voce gostaria que tivessem formato melhor.
5. Crie exemplos de treino em `data/meu_treino.jsonl`.
6. Edite a config de treino apontando para `data/meu_treino.jsonl`.
7. Rode um treino pequeno.
8. Teste com `scripts/infer.py`.
9. Ajuste dataset e config.
10. Repita ate o comportamento ficar bom.

## Fluxo recomendado com Ollama

1. Gere contexto com `python scripts/context_gui.py`.
2. Gere o `Modelfile` com `python scripts/build_ollama_model.py`.
3. Crie o modelo com `ollama create qwen-contexto -f ollama/Modelfile`.
4. Pergunte usando `python scripts/ask_ollama_with_context.py --model qwen-contexto --question "..."`.
5. Ajuste `configs/ollama_model.yaml` para mudar comportamento, temperatura ou modelo base.

Para maquinas sem GPU, este e o fluxo mais pratico.
