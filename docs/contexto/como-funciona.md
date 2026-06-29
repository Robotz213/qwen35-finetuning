# Como funciona

O gerador de contexto transforma arquivos comuns em dois formatos principais:

- `context_pack.md`: um arquivo Markdown unico para leitura ou uso direto em prompts.
- `context_chunks.jsonl`: uma lista de trechos menores com metadados, ideal para busca, RAG ou automacoes.

## Formatos aceitos

- `.pdf`
- `.docx`
- `.xlsx`
- `.xls`
- `.csv`
- `.tsv`
- `.txt`
- `.md`
- `.json`
- `.jsonl`

## O que e um chunk

Um chunk e um trecho do documento original. Cada chunk guarda:

- caminho do arquivo original;
- nome do arquivo;
- tipo do arquivo;
- secao ou pagina;
- indice do chunk;
- texto extraido;
- metadados.

Isso permite usar os documentos depois em prompts, busca textual, embeddings ou RAG.
