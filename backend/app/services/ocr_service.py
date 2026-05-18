import fitz
import io

import pytesseract

from PIL import Image

# =========================
# EXTRACT TEXT FROM PDF
# =========================

def extract_text_from_pdf(contents):

    extracted_text = ""

    metadata = {}

    pdf_document = fitz.open(
        stream=contents,
        filetype="pdf"
    )

    metadata["pages"] = len(pdf_document)

    for page_number in range(len(pdf_document)):

        page = pdf_document.load_page(
            page_number
        )

        pix = page.get_pixmap()

        image_bytes = pix.tobytes("png")

        image = Image.open(
            io.BytesIO(image_bytes)
        )

        page_text = pytesseract.image_to_string(
            image
        )

        extracted_text += page_text + "\n"

    return extracted_text, metadata

# =========================
# EXTRACT TEXT FROM IMAGE
# =========================

def extract_text_from_image(contents):

    metadata = {}

    image = Image.open(
        io.BytesIO(contents)
    )

    metadata["format"] = image.format

    metadata["mode"] = image.mode

    metadata["size"] = image.size

    exif_data = image.getexif()

    for tag_id, value in exif_data.items():

        metadata[str(tag_id)] = str(value)

    extracted_text = pytesseract.image_to_string(
        image
    )

    return extracted_text, metadata