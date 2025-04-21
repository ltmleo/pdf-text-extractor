import fitz  # PyMuPDF
import os
import argparse
from tqdm import tqdm  # Importa tqdm para a barra de progresso
from google.cloud import vision  # Importa Vision API do Google Cloud
from difflib import SequenceMatcher  # Para comparar textos

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


def process_images_and_extract_texts(output_folder, comparison_text=None):
    """Processa as imagens na pasta de saída, extrai texto e compara com texto fornecido."""
    for image_file in os.listdir(output_folder):
        if image_file.endswith(".png"):
            image_path = os.path.join(output_folder, image_file)
            extracted_text = extract_text_from_image(image_path)
            
            # Salva o texto extraído em um arquivo .md
            md_file_path = os.path.splitext(image_path)[0] + ".md"
            with open(md_file_path, "w", encoding="utf-8") as md_file:
                md_file.write(f"# Texto extraído da imagem: {image_file}\n\n")
                md_file.write("```\n")
                md_file.write(extracted_text)
                md_file.write("\n```\n")
            
            print(f"Texto extraído da imagem {image_file} salvo em {md_file_path}.\n")
            
            # if comparison_text:
            #     similarity = compare_texts(extracted_text, comparison_text)
            #     print(f"Similaridade com o texto fornecido: {similarity:.2f}%\n")
        exit()

def main():
    parser = argparse.ArgumentParser(description="Converte um arquivo PDF em imagens e extrai texto.")
    parser.add_argument("--pdf", type=str, help="Caminho para o arquivo PDF de entrada.")
    parser.add_argument("--out", type=str, help="Pasta onde as imagens serão salvas.")
    
    args = parser.parse_args()
    
    #pdf_to_images(args.pdf, args.out)
    process_images_and_extract_texts(args.out, args.compare)

if __name__ == "__main__":
    main()