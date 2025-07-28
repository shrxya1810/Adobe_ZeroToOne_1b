# modules/parser.py

import fitz  # PyMuPDF

def is_good_heading(text):
    if len(text.split()) < 3:
        return False
    if text.endswith(".") or text.islower():
        return False
    return True

def extract_pdf_sections(document_paths):
    extracted = []

    for filename, filepath in document_paths:
        doc = fitz.open(filepath)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text_blocks = [line.strip() for line in page.get_text("text").split('\n') if len(line.strip()) > 10]

            if not text_blocks:
                continue

            # Smart heading detection
            heading = next((line for line in text_blocks if is_good_heading(line)), text_blocks[0])
            content_lines = [line for line in text_blocks if len(line) >= 40 and not line.isspace()]
            content = "\n".join(content_lines)

            extracted.append({
                "document": filename,
                "page": page_num + 1,
                "section_title": heading,
                "content": content
            })

    return extracted
