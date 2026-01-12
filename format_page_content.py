import fitz

def format_page_content(page,blocks):
    """
    Passthrough the pages and looking for a WARNING statement and parse it
    to readable format for a agent.

    Args:
        pdf_path:str -> path to a pdf
    
    Return:
        string that contains WARNING info
    """
    image_rects = []
    for img in page.get_images():
        xref = img[0]
        for r in page.get_image_rects(xref):
            image_rects.append(r)
    
    content_builder = []

    for b in blocks:
        x0, y0, x1, y1, text, block_no, block_type = b
        clean_text = text.strip()
        if not clean_text: continue

        is_visual_warning = False
        
        for img_r in image_rects:
            vertical_gap = y0 - img_r.y1
            if (0 < vertical_gap < 40) and (x0 < img_r.x1) and (x1 > img_r.x0):
                is_visual_warning = True
                break

        if is_visual_warning:
            formatted_block = (
                f"\n <CRITICAL_WARNING>\n"
                f"[VISUAL HEADER DETECTED]\n" 
                f"CONTENT: {clean_text}\n"
                f"</CRITICAL_WARNING>\n"
            )
            content_builder.append(formatted_block)
            
        elif clean_text.upper().startswith("NOTICE"):
            formatted_block = f"\n<NOTICE>\n{clean_text}\n</NOTICE>\n"
            content_builder.append(formatted_block)
            
        else:
            content_builder.append(clean_text)

    return "\n\n".join(content_builder)