import io
import os
import re

import fitz  # PyMuPDF
import pytesseract
from PIL import Image


def extract_text_from_footer(pdf_path, page_number, footer_height=75):
    # Open the PDF document
    document = fitz.open(pdf_path)

    # Load the specific page
    page = document.load_page(page_number)

    # Get the page dimensions
    page_rect = page.rect

    # Define the footer region (bottom footer_height units of the page)
    footer_rect = fitz.Rect(page_rect.x0, page_rect.y1 - footer_height, page_rect.x1, page_rect.y1)

    # Render the footer region to an image
    pix = page.get_pixmap(clip=footer_rect, dpi=300)

    # Convert the image to a PIL Image
    img = Image.open(io.BytesIO(pix.tobytes()))

    # image_output_folder = './image_temp/'
    # if image_output_folder:
    #     img_file_name = os.path.join(image_output_folder, f"footer_page_{page_number + 1}.png")
    #     img.save(img_file_name)
    #     print(f"Saved footer image: {img_file_name}")

    # Perform OCR on the footer image
    text = pytesseract.image_to_string(img)

    return text


def extract_text_between_angles(text):
    match = re.search(r'<([^<>]+)>', text)
    if match:
        return match.group(1)
    else:
        return "Untitled"


def generate_safe_filename(base_name, extension=".pdf"):
    safe_base_name = base_name.strip().replace("\n", "_").replace(" ", "_").replace("/", "_").replace("\\", "_")
    safe_base_name = extract_text_between_angles(safe_base_name)
    return f"{safe_base_name[:50]}{extension}"


def split_pdf_to_single_pages(input_pdf_path, output_folder):
    # Making sure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the input PDF file
    document = fitz.open(input_pdf_path)
    number_of_pages = len(document)

    # Iterate through each page
    for page_number in range(number_of_pages):
        # Extract text from the current page to determine the file name
        page_text = extract_text_from_footer(input_pdf_path, page_number)
        print(f"Page {page_number}: {page_text}")
        if page_text:
            page_title = page_text.splitlines()[0]  # Use the first line of text as the title
        else:
            page_title = f"page_{page_number + 1}"

        # Generate a safe file name based on page text
        file_name = generate_safe_filename(page_title)
        output_pdf_path = os.path.join(output_folder, file_name)

        # Create a new PDF file for each page
        pdf_writer = fitz.open()
        pdf_writer.insert_pdf(document, from_page=page_number, to_page=page_number)

        # Save the single page PDF
        pdf_writer.save(output_pdf_path)
        pdf_writer.close()

        print(f"Created: {output_pdf_path}")


if __name__ == "__main__":
    input_pdf_path = 'labchip_sample_output.pdf'
    output_folder = './split/'

    split_pdf_to_single_pages(input_pdf_path, output_folder)
