import google.generativeai as genai
import os
from PIL import Image
import io

# Método 1: Usando variável de ambiente
# Certifique-se de definir a variável de ambiente GOOGLE_API_KEY
api_key = os.environ.get("GOOGLE_API_KEY")

# Método 2: Definindo diretamente (NÃO RECOMENDADO PARA PRODUÇÃO)
# api_key = "SUA_CHAVE_DE_API"

genai.configure(api_key=api_key)

def carregar_imagem(caminho_arquivo):
    try:
        img = Image.open(caminho_arquivo)
        return img
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em {caminho_arquivo}")
        return None

def extrair_texto_da_imagem(imagem):
    model = genai.GenerativeModel('gemini-2.5-flash-preview-04-17')
    img_data = io.BytesIO()
    imagem.save(img_data, format='PNG')
    img_data.seek(0)

    contents = [
        {
            "mime_type": "image/png",
            "data": img_data.getvalue()
        },
        """Extraia o texto desta imagem, prestando atenção especial a listas e outros elementos de formatação.
        Formate como markdown, incluindo títulos, listas e formatação de texto.
        Não inclua informações adicionais ou explicações.
        """
    ]

    response = model.generate_content(contents)
    return response.text


def salvar_em_markdown(texto, nome_arquivo="receita.md"):
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(texto)
    print(f"\nO texto foi salvo em {nome_arquivo}")

if __name__ == "__main__":
    caminho_da_imagem = "pdfs/images/doces_vo_elisa/page_8.png"  # Substitua pelo caminho real do seu arquivo
    imagem = carregar_imagem(caminho_da_imagem)
    if imagem is None:
        exit()
    texto_extraido = extrair_texto_da_imagem(imagem)

    if texto_extraido:
        print("Texto extraído:\n")
        print(texto_extraido)
    else:
        print("Não foi possível extrair o texto da imagem.")


    if texto_extraido:
        salvar_em_markdown(texto_extraido)