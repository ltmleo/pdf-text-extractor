

#!/bin/bash

# Diretório contendo os conjuntos de páginas
PAGES_DIR="pdfs/images/salgados-vo-elisa"

# Diretório de saída
OUT_DIR="./receitas/salgados-vo-elisa"

# Itera por todos os diretórios ou arquivos no diretório de páginas
for PAGES in "$PAGES_DIR"/*; do
    # Extrai o nome do conjunto de páginas
    if [[ ! -d "$PAGES" ]]; then
        echo "O caminho $PAGES não é um diretório."
        continue
    fi
    PAGE_NAME=$(basename "$PAGES")
    if [[ $PAGE_NAME == "1-10" ]]; then
        echo "O conjunto $PAGE_NAME não deve ser processado."
    else
        echo "O conjunto $PAGE_NAME será processado."
        continue
    fi
    echo "Processando o conjunto: $PAGE_NAME"
    
    # Executa o comando para o conjunto atual
    python scripts/main.py extract-text --images "$PAGES" --out "$OUT_DIR/$PAGE_NAME"
    sleep 30
done