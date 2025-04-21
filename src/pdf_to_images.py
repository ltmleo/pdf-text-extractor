import fitz  # PyMuPDF
import os
from tqdm import tqdm

def pdf_to_images(pdf_path, output_folder):
    """Converte um PDF em imagens, salvando cada página como uma imagem."""
    pdf_document = fitz.open(pdf_path)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for page_number in tqdm(range(len(pdf_document)), desc="Convertendo páginas"):
        page = pdf_document.load_page(page_number)
        pix = page.get_pixmap()
        output_image_path = os.path.join(output_folder, f'page_{page_number + 1}.png')
        pix.save(output_image_path)

    pdf_document.close()
