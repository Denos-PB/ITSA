import fitz

def remove_headers(blocks, header_cutoff):
    """
    Removes any text block that starts above the cutoff Y-coordinate.
    Returns a filtered list of blocks.
    """

    clean_blocks = []

    for b in blocks:
        y_bottom = b[3]

        if y_bottom > header_cutoff:
            clean_blocks.append(b)

    return clean_blocks