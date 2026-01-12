import fitz

def format_page_content(pdf_path):
    """
    Passthrough the pages and looking for a WARNING statement and parse it
    to readable format for a agent.

    Args:
        pdf_path:str -> path to a pdf
    
    Return:
        string that contains WARNING info
    """
    doc = fitz.open(pdf_path)
    cleaned_chunks = []

    for page_num, page in enumerate(doc):
        blocks = page.get_text("blocks")
        blocks.sort(key=lambda b: (b[1], b[0]))

        image_rects = []
        for img in page.get_images():
            xref = img[0]
            rects = page.get_image_rects(xref) 
            for r in rects:
                image_rects.append(r)

        page_content_builder = []

        for b in blocks:
            x0, y0, x1, y1, text, block_no, block_type = b
            clean_text = text.strip()

            if not clean_text: continue

            is_warning_header = False

            for img_r in image_rects:
                vertical_gap = y0 - img_r.y1

                is_close_below = (0 < vertical_gap < 40)
                is_aligned = (x0 < img_r.x1) and (x1 > img_r.x0)

                if is_close_below and is_aligned:
                    is_warning_header = True
                    break

            if clean_text.upper().startswith("NOTICE"):
                formatted_block = f"\n <NOTICE>\n{clean_text}\n</NOTICE>\n"
                page_content_builder.append(formatted_block)
                continue

            if is_warning_header:
                formatted_block = (
                    f"\n<CRITICAL_WARNING>\n"
                    f"[VISUAL HEADER DETECTED]\n" 
                    f"CONTENT: {clean_text}\n"
                    f"</CRITICAL_WARNING>\n"
                )
                page_content_builder.append(formatted_block)
            else:
                page_content_builder.append(clean_text)

        return "\n\n".join(page_content_builder)