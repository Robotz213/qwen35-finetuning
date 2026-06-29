# Gerar contexto pelo CLI

Esta pagina explica a geracao de contexto pelo terminal. Para usar a janela Tkinter, veja [Interface grafica](interface-grafica.md).

Copie seus arquivos para:

```text
C:\Github\qwen35-finetuning\context\sources
```

Exemplo:

```text
context/sources/
  contrato.pdf
  produtos.xlsx
  politicas.md
  perguntas_frequentes.docx
```

Execute pelo terminal:

```powershell
python scripts/build_context.py --config configs/context_builder.yaml
```

Tambem e possivel abrir a interface grafica:

```powershell
python scripts/context_gui.py
```

Saidas geradas:

```text
outputs/context/context_pack.md
outputs/context/context_chunks.jsonl
outputs/context/manifest.json
```

O arquivo `manifest.json` mostra quantas fontes e chunks foram gerados.

## Usar outra pasta

Voce pode apontar para qualquer pasta:

```powershell
python scripts/build_context.py --source-dir C:\MeusArquivos\BaseIA --output-dir outputs/minha-base
```

## Ajustar configuracao

Edite:

```text
configs/context_builder.yaml
```

Campos principais:

```yaml
source_dir: context/sources
output_dir: outputs/context
chunk_size: 1800
chunk_overlap: 250
max_rows_per_sheet: 5000
```

Como escolher:

- `chunk_size`: aumenta ou reduz o tamanho de cada trecho.
- `chunk_overlap`: repete parte do trecho anterior para preservar continuidade.
- `max_rows_per_sheet`: limita o numero de linhas lidas por aba de planilha.

Para documentos longos, `chunk_size` entre `1200` e `2500` costuma funcionar bem.
