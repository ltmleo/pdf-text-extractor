# Python PDF to Images and Text Extraction

Este projeto permite converter PDFs em imagens e extrair texto das imagens geradas, utilizando Google Cloud Vision ou Gemini.

## Estrutura do Projeto

```
receitas
├── pdfs
│   ├── images
│   │   └── (as imagens geradas serão salvas aqui)
│   └── sample.pdf
├── src
│   ├── main.py
│   ├── pdf_to_images.py
│   ├── text_extraction.py
├── requirements.txt
└── README.md
```

## Pré-requisitos

Antes de executar o projeto, você precisa ter o Python instalado em sua máquina. Além disso, é necessário instalar as dependências listadas no arquivo `requirements.txt`.

## Instalação

1. Clone o repositório:
   ```
   git clone <URL_DO_REPOSITORIO>
   cd python-pdf-to-images
   ```

2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

## Uso

### Extração de Imagens

Para converter um PDF em imagens:
```
python src/main.py extract-images --pdf <CAMINHO_DO_PDF> --out <PASTA_DE_SAIDA>
```

### Extração de Texto

Para extrair texto de uma única imagem:
```
python src/main.py extract-text --image <CAMINHO_DA_IMAGEM> --method <vision|gemini> [--out <ARQUIVO_DE_SAIDA>]
```

Para extrair texto de todas as imagens em uma pasta:
```
python src/main.py extract-text --images <PASTA_DAS_IMAGENS> --method <vision|gemini> [--out <ARQUIVO_DE_SAIDA>]
```

Se `--out` não for especificado, o texto será impresso no terminal.

## Contribuição

Sinta-se à vontade para contribuir com melhorias ou correções. Faça um fork do repositório e envie suas alterações.

## Licença

Este projeto está licenciado sob a MIT License. Veja o arquivo LICENSE para mais detalhes.