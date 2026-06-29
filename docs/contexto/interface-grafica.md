# Interface grafica

O projeto inclui uma interface Tkinter para gerar contexto sem usar comandos longos. Ela e o caminho mais simples quando voce quer selecionar PDFs, planilhas, documentos Word, Markdown, JSON ou arquivos de texto manualmente.

Execute na raiz do projeto:

```powershell
python scripts/context_gui.py
```

## Pre-requisitos

Instale as dependencias do projeto:

```powershell
pip install -r requirements.txt
```

Para arquivos simples como `.txt`, `.md`, `.json` e `.jsonl`, o fluxo usa quase so recursos padrao do Python. Para PDF, Word e planilhas, confirme que estas bibliotecas estao instaladas:

```powershell
pip install pypdf python-docx pandas openpyxl
```

## Inspiracao visual

A interface foi desenhada com base em produtos modernos de desenvolvimento e produtividade, como Vercel, GitHub, Linear, Stripe, Raycast, Notion, Figma, Framer, Clerk, Supabase, Railway, Cloudflare, OpenAI, Anthropic, Cursor, Docker, Vite, Next.js, React, Tailwind CSS, Slack, Discord, Atlassian e outros.

Na pratica, isso aparece em:

- layout com barra lateral;
- superficies neutras e limpas;
- acoes primarias evidentes;
- poucos controles por tela;
- feedback de atividade;
- fluxo rapido para adicionar arquivos e gerar saidas.

## Fluxo basico

1. Clique em `Adicionar arquivos` ou `Adicionar pasta`.
2. Confirme que os arquivos apareceram na lista.
3. Ajuste `Tamanho do chunk`, `Sobreposicao` e `Linhas max. por planilha` se necessario.
4. Clique em `Gerar contexto`.
5. Use `Abrir pasta de saida` para acessar os arquivos gerados.

## Areas da tela

### Arquivos de entrada

Mostra os arquivos encontrados na pasta configurada em `Pasta de fontes`.

Botoes principais:

- `Adicionar arquivos`: seleciona um ou mais arquivos.
- `Adicionar pasta`: importa todos os arquivos suportados dentro de uma pasta.
- `Atualizar`: recarrega a lista.
- `Remover selecionado`: remove arquivos apenas quando eles estao em `context/sources`.

### Configuracao

Controla como o contexto sera gerado:

- `Pasta de saida`: onde os arquivos processados serao salvos.
- `Titulo do contexto`: titulo usado no `context_pack.md`.
- `Tamanho do chunk`: tamanho aproximado de cada trecho.
- `Sobreposicao`: quantidade de texto repetida entre chunks vizinhos.
- `Linhas max. por planilha`: limite de linhas lidas por aba de Excel ou CSV.
- `Instrucao padrao`: texto colocado no topo do pacote Markdown.

### Prompt com contexto

Depois de gerar `context_chunks.jsonl`, este painel cria um `prompt.md` com os trechos mais relevantes para uma pergunta.

Campos:

- caixa de pergunta;
- `Trechos`: quantidade maxima de chunks usados no prompt;
- `Criar prompt`: gera `outputs/context/prompt.md`.

## Saidas geradas

Por padrao, a GUI grava em:

```text
outputs/context/context_pack.md
outputs/context/context_chunks.jsonl
outputs/context/manifest.json
```

O que cada arquivo faz:

- `context_pack.md`: pacote unico em Markdown para leitura, copia ou injecao em prompts.
- `context_chunks.jsonl`: chunks estruturados com metadados para busca, RAG ou automacoes.
- `manifest.json`: resumo com quantidade de fontes e chunks.

## Exemplo completo

1. Abra a interface:

```powershell
python scripts/context_gui.py
```

2. Clique em `Adicionar arquivos`.
3. Selecione `contrato.pdf`, `produtos.xlsx` e `faq.docx`.
4. Mantenha `Copiar arquivos adicionados para context/sources` marcado.
5. Clique em `Gerar contexto`.
6. Clique em `Abrir pasta de saida`.
7. Abra `context_pack.md` para revisar o resultado.

## Criar prompt pela interface

Depois de gerar o contexto:

1. Digite uma pergunta no painel `Prompt com contexto`.
2. Ajuste a quantidade de trechos em `Trechos`.
3. Clique em `Criar prompt`.

O arquivo sera salvo em:

```text
outputs/context/prompt.md
```

## Copia de arquivos

Por padrao, arquivos adicionados pela interface sao copiados para:

```text
context/sources
```

Isso deixa a base do projeto organizada e reproduzivel.

Se desmarcar essa opcao, a interface passa a usar a pasta dos arquivos selecionados como fonte, sem copiar os arquivos para o projeto. Esse modo e util para testar uma pasta externa rapidamente.

Por seguranca, a acao `Remover selecionado` so apaga arquivos quando a pasta de fontes e `context/sources`.

## Parametros recomendados

Para documentos gerais:

```text
Tamanho do chunk: 1800
Sobreposicao: 250
Linhas max. por planilha: 5000
```

Para documentos muito longos:

```text
Tamanho do chunk: 1200
Sobreposicao: 200
Linhas max. por planilha: 1000
```

Para contexto mais amplo por trecho:

```text
Tamanho do chunk: 2500
Sobreposicao: 300
Linhas max. por planilha: 5000
```

## Como validar o resultado

Depois de gerar:

1. Abra `manifest.json` e confirme o numero de fontes.
2. Abra `context_pack.md` e confira se o texto extraido faz sentido.
3. Crie um prompt pela interface com uma pergunta especifica.
4. Abra `prompt.md` e veja se os trechos selecionados sao relevantes.

## Quando usar a GUI

Use a GUI quando quiser:

- selecionar arquivos manualmente;
- trabalhar com PDFs e planilhas sem lembrar comandos;
- ajustar parametros visualmente;
- gerar contexto e prompt no mesmo lugar;
- mostrar o fluxo para outra pessoa.

Use o CLI quando quiser automatizar o processo em scripts.
