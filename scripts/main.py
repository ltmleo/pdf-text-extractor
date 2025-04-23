import fitz  # PyMuPDF
import os
import argparse
from tqdm import tqdm
from google.cloud import vision
from PIL import Image
import io
import google.generativeai as genai

# Configuração da API Gemini
api_key = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

def ensure_directory_exists(directory):
    """Garante que o diretório existe, criando-o se necessário."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def convert_pdf_to_images(pdf_path, output_folder):
    """Converte um PDF em imagens e salva cada página como uma imagem."""
    pdf_document = fitz.open(pdf_path)
    ensure_directory_exists(output_folder)

    for page_number in tqdm(range(len(pdf_document)), desc="Convertendo páginas"):
        page = pdf_document.load_page(page_number)
        pix = page.get_pixmap()
        output_image_path = os.path.join(output_folder, f'page_{page_number + 1}.png')
        pix.save(output_image_path)

    pdf_document.close()

def extract_text_with_vision(image_path):
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
        with Image.open(image_path) as img:
            img_data = io.BytesIO()
            img.save(img_data, format='PNG')
            img_data.seek(0)

        contents = [
            {"mime_type": "image/png", "data": img_data.getvalue()},
            """Extraia o texto desta imagem, prestando atenção especial a listas e outros elementos de formatação.
            Formate como markdown, incluindo títulos, listas e formatação de texto.
            Organize cada seção com marcadores apropriados (## para títulos, ### para subtítulos, etc.).
            Não se esqueça de incluir listas quando existirem (lista de ingredientes, passos, etc.).
            Não inclua informações adicionais ou explicações."""
        ]

        model = genai.GenerativeModel('gemini-2.5-flash-preview-04-17')
        response = model.generate_content(contents)
        return response.text
    except Exception as e:
        print(f"Erro ao processar a imagem com Gemini: {e}")
        return None

def process_single_image(image_path, method):
    """Processa uma única imagem e retorna o texto extraído."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"O arquivo de imagem {image_path} não existe.")
    return method(image_path)

def process_images_in_folder(folder_path, method, output_folder=None):
    """Processa todas as imagens em uma pasta e salva os resultados."""
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"A pasta {folder_path} não existe.")
    if output_folder:
        ensure_directory_exists(output_folder)

    extracted_texts = []
    for image_file in sorted(os.listdir(folder_path)):
        image_path = os.path.join(folder_path, image_file)
        page = image_file.split("_")[1].split(".")[0] if "_" in image_file else image_file.split(".")[0]
        if not os.path.isfile(image_path):
            print(f"Pulando {image_path}, pois não é um arquivo válido.")
            continue
        try:
            result = f"""---
sidebar_position: {page}
---
# Página {page}
:::danger[NÃO REVISADO]
A página não foi revisada, portanto pode conter erros de digitação, formatação ou alucinações.
:::
"""
            result += method(image_path)
            result += "\n\n![imagem base](./images/" + image_file + ")"
            if result:
                extracted_texts.append(result)
                if output_folder:
                    output_file = os.path.join(output_folder, f"{os.path.splitext(image_file)[0]}.md")
                    with open(output_file, "w", encoding="utf-8") as f:
                        f.write(result)
                    print(f"Texto da imagem {image_file} salvo em {output_file}")
                    # copy image to output folder
                    output_image_path = os.path.join(output_folder, "images", image_file)
                    ensure_directory_exists(os.path.dirname(output_image_path))
                    with open(image_path, "rb") as img_file:
                        with open(output_image_path, "wb") as out_file:
                            out_file.write(img_file.read())
            else:
                print(f"Erro: Não foi possível extrair texto da imagem {image_path}.")
        except Exception as e:
            print(f"Erro ao processar a imagem {image_path}: {e}")
    return extracted_texts

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
    parser_text.add_argument("--method", type=str, choices=["vision", "gemini"], default="gemini", help="Método de extração de texto.")
    parser_text.add_argument("--out", type=str, help="Pasta onde os textos extraídos serão salvos. Se não especificado, imprime no stdout.")

    args = parser.parse_args()

    if args.command == "extract-images":
        convert_pdf_to_images(args.pdf, args.out)
    elif args.command == "extract-text":
        method = extract_text_with_gemini if args.method == "gemini" else extract_text_with_vision
        try:
            if args.image:
                result = process_single_image(args.image, method)
                if args.out:
                    ensure_directory_exists(args.out)
                    output_file = os.path.join(args.out, "output.md")
                    with open(output_file, "w", encoding="utf-8") as f:
                        f.write(result)
                    print(f"Texto salvo em {output_file}")
                else:
                    print(result)
            elif args.images:
                extracted_texts = process_images_in_folder(args.images, method, args.out)
                if not args.out:
                    print("\n".join(extracted_texts))
        except Exception as e:
            print(f"Erro: {e}")

if __name__ == "__main__":
    main()