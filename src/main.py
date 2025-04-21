import fitz  # PyMuPDF
import os
import argparse
from tqdm import tqdm  # Importa tqdm para a barra de progresso
from google.cloud import vision  # Importa Vision API do Google Cloud
from difflib import SequenceMatcher  # Para comparar textos
from PIL import Image
import io
import google.generativeai as genai

# Configuração da API Gemini
api_key = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

def pdf_to_images(pdf_path, output_folder):
    # Abre o arquivo PDF
    pdf_document = fitz.open(pdf_path)
    
    # Verifica se a pasta de saída existe, caso contrário, cria
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Itera sobre cada página do PDF com barra de progresso
    for page_number in tqdm(range(len(pdf_document)), desc="Convertendo páginas"):
        # Obtém a página
        page = pdf_document.load_page(page_number)
        # Converte a página em uma imagem
        pix = page.get_pixmap()
        # Define o caminho da imagem de saída
        output_image_path = os.path.join(output_folder, f'page_{page_number + 1}.png')
        # Salva a imagem
        pix.save(output_image_path)

    # Fecha o documento PDF
    pdf_document.close()

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
    """Extrai texto de uma imagem usando o método Gemini."""
    try:
        # Carregar a imagem
        img = Image.open(image_path)
        img_data = io.BytesIO()
        img.save(img_data, format='PNG')
        img_data.seek(0)

        # Configurar o conteúdo para o modelo Gemini
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

        # Chamar o modelo Gemini
        model = genai.GenerativeModel('gemini-2.5-flash-preview-04-17')
        response = model.generate_content(contents)
        return response.text
    except Exception as e:
        print(f"Erro ao processar a imagem com Gemini: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Ferramenta para manipulação de PDFs e extração de texto.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcomando para extrair imagens do PDF
    parser_images = subparsers.add_parser("extract-images", help="Extrai imagens de um PDF.")
    parser_images.add_argument("--pdf", type=str, required=True, help="Caminho para o arquivo PDF de entrada.")
    parser_images.add_argument("--out", type=str, required=True, help="Pasta onde as imagens serão salvas.")

    # Subcomando para extrair texto
    parser_text = subparsers.add_parser("extract-text", help="Extrai texto de uma imagem ou de imagens em uma pasta.")
    parser_text.add_argument("--image", type=str, help="Caminho para uma única imagem.")
    parser_text.add_argument("--images", type=str, help="Pasta contendo as imagens.")
    parser_text.add_argument("--method", type=str, choices=["vision", "gemini"], default="vision", help="Método de extração de texto.")
    parser_text.add_argument("--out", type=str, help="Arquivo onde o texto será salvo. Se não especificado, imprime no stdout.")

    args = parser.parse_args()

    if args.command == "extract-images":
        pdf_to_images(args.pdf, args.out)
    elif args.command == "extract-text":
        if not args.image and not args.images:
            print("Erro: Você deve especificar --image ou --images.")
            return

        method = extract_text_with_gemini if args.method == "gemini" else extract_text_from_image
        extracted_text = []

        if args.image:
            if not os.path.exists(args.image):
                print(f"Erro: O arquivo de imagem {args.image} não existe.")
                return
            try:
                result = method(args.image)
                if result:
                    extracted_text.append(result)
                else:
                    print(f"Erro: Não foi possível extrair texto da imagem {args.image}.")
            except Exception as e:
                print(f"Erro ao processar a imagem {args.image}: {e}")
        elif args.images:
            if not os.path.exists(args.images):
                print(f"Erro: A pasta {args.images} não existe.")
                return
            for image_file in sorted(os.listdir(args.images)):
                image_path = os.path.join(args.images, image_file)
                if not os.path.isfile(image_path):
                    print(f"Pulando {image_path}, pois não é um arquivo válido.")
                    continue
                try:
                    result = method(image_path)
                    if result:
                        extracted_text.append(result)
                    else:
                        print(f"Erro: Não foi possível extrair texto da imagem {image_path}.")
                except Exception as e:
                    print(f"Erro ao processar a imagem {image_path}: {e}")

        full_text = "\n".join(extracted_text)
        if args.out:
            with open(args.out, "w", encoding="utf-8") as f:
                f.write(full_text)
            print(f"Texto salvo em {args.out}")
        else:
            print(full_text)

if __name__ == "__main__":
    main()