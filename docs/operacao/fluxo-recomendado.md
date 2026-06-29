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
