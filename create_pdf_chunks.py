import fitz
from remove_headers import remove_headers
from format_page_content import format_page_content

def create_pdf_chunks(pdf_path):
    doc = fitz.open(pdf_path)
    final_chunks = []

    for i in range(len((doc))):
        page = doc[i]

        raw_blocks = page.get_text("blocks")
        raw_blocks.sort(key = lambda b: (b[0], b[1]))

        clean_blocks = remove_headers(blocks = raw_blocks, header_cutoff = 75)

        formatted_text = format_page_content(page, clean_blocks)

        if formatted_text.strip():
            chunk = {
                "id": f"page_{i + 1}",
                "page_number": i + 1,
                "content": formatted_text,
                "metadata": {
                    "source": pdf_path,
                    "has_critical_warning": "<CRITICAL_WARNING>" in formatted_text
                }
            }
            final_chunks.append(chunk)

    return final_chunks