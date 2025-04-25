#!/bin/bash

# Caminho para a pasta de PDFs/Imagens
PASTA="pdfs/images/salgados-vo-elisa"

# Verifica se a pasta existe
if [ ! -d "$PASTA" ]; then
    echo "A pasta $PASTA não existe."
    exit 1
fi

# Cria as subpastas por dezena e move os arquivos
for ARQUIVO in "$PASTA"/*; do
    if [ -f "$ARQUIVO" ]; then
        # Obtém o número do arquivo (suporta formatos como 'page_98.png')
        NUMERO=$(basename "$ARQUIVO" | grep -o '[0-9]\+')
        
        if [[ "$NUMERO" =~ ^[0-9]+$ ]]; then
            # Calcula a dezena (ajustada para 1-9, 10-19, etc.)
            INICIO=$(( (NUMERO - 1) / 10 * 10 + 1 ))
            FIM=$(( INICIO + 9 ))
            
            # Nome da subpasta
            SUBPASTA="$PASTA/$INICIO-$FIM"
            
            # Cria a subpasta, se não existir
            mkdir -p "$SUBPASTA"
            
            # Move o arquivo para a subpasta
            mv "$ARQUIVO" "$SUBPASTA/"
        else
            echo "O arquivo $ARQUIVO não tem um número válido no nome."
        fi
    fi
done

echo "Arquivos organizados por dezenas."