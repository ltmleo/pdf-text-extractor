# Python PDF to Images

Este projeto tem como objetivo ler um arquivo PDF e converter cada página em uma imagem, salvando essas imagens em uma pasta específica.

## Estrutura do Projeto

```
python-pdf-to-images
├── pdfs
│   ├── images
│   │   └── (as imagens geradas serão salvas aqui)
│   └── sample.pdf
├── src
│   ├── main.py
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

Para executar o projeto e converter o PDF em imagens, siga os passos abaixo:

1. Certifique-se de que o arquivo `sample.pdf` está na pasta `pdfs`.
2. Execute o script principal:
   ```
   python src/main.py
   ```

As imagens geradas serão salvas na pasta `pdfs/images`.

## Contribuição

Sinta-se à vontade para contribuir com melhorias ou correções. Faça um fork do repositório e envie suas alterações.

## Licença

Este projeto está licenciado sob a MIT License. Veja o arquivo LICENSE para mais detalhes.