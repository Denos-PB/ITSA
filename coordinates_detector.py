import fitz  # PyMuPDF

def check_header_coordinates(pdf_path):
    """
    Detect a coordinates where noise and text starting so we can just cut off messy data
    on top of each page

    Args:
        pdf_path:str -> path to a pdf

    Return:
        coordinates of messy headers
    """
    doc = fitz.open(pdf_path)
    
    target_pages = [0, 20, 89] 
    
    for p_num in target_pages:
        if p_num >= len(doc): continue
        
        page = doc[p_num]
        blocks = page.get_text("blocks")

        blocks.sort(key=lambda b: b[1]) 
        
        print(f"\n--- Top Elements on Page {p_num+1} ---")
        
        found_any = False
        for b in blocks:
            y_top = b[1]   # Top edge of text
            y_bottom = b[3] # Bottom edge of text
            text = b[4].strip().replace("\n", " ")
            
            # Only show items in the top 100 pixels
            if y_bottom < 150:
                print(f"Y-Range: {y_top:.1f} to {y_bottom:.1f} | Text: {text}")
                found_any = True
            else:
                # Stop looking once we go past the header area
                break
        
        if not found_any:
            print("(No text found in the top 150 pixels)")

file_path = r"data\Caterpillar 797F Operation and Maintenance Manual.pdf"
check_header_coordinates(file_path)