import fitz
import json

def process_warning_statment(pdf_path):
    doc = fitz.open(pdf_path)
    cleaned_chunks = []

    for page_num, page in enumerate(doc):
        blocks = page.get_text("blocks")
        
        main_text = []
        warnings = []

        for b in blocks:
            x0, y0, x1, y1, text, block_no, block_type = b

            clean_text = text.strip()
            if not clean_text:
                continue

            is_warning = False

            if clean_text.startswith("WARNING") or clean_text.startswith("DANGER") or clean_text.startswith("NOTICE"):
                is_warning = True

            if is_warning:
                warnings.append(clean_text)
            else:
                main_text.append(clean_text)

            full_page_text = " ".join(main_text)

            chunk = {
                "page_number" : page_num + 1, 
                "content" : full_page_text,
                "metadata" : {
                    "source" : pdf_path,
                    "safety_warnings" : warnings
                }
            }

            cleaned_chunks.append(chunk)

        return cleaned_chunks
