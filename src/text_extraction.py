from google.cloud import vision
import google.generativeai as genai
import io
from PIL import Image
import os

# Configuração do Gemini
api_key = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

def extract_text_from_image(image_path):
    """Extrai texto de uma imagem usando o Google Cloud Vision API."""
    client = vision.ImageAnnotatorClient()
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    if response.error.message:
        raise Exception(f"Erro na API do Google Cloud Vision: {response.error.message}")
    return response.text_annotations[0].description if response.text_annotations else ""

def extract_text_with_gemini(image_path):
    """Extrai texto de uma imagem usando o Gemini."""
    model = genai.GenerativeModel('gemini-2.5-flash-preview-04-17')
    with Image.open(image_path) as img:
        img_data = io.BytesIO()
        img.save(img_data, format='PNG')
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
