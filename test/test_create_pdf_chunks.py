import sys
import os
import unittest
from unittest.mock import MagicMock, patch
import fitz

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from remove_headers import remove_headers 
from format_page_content import format_page_content
from create_pdf_chunks import create_pdf_chunks

class TestPdfPipeline(unittest.TestCase):

    def setUp(self):
        """Setup runs before every test."""
        self.header_block = (10, 10, 100, 50, "Maintenance Section", 0, 0)
        self.content_block = (10, 80, 100, 100, "Real Content", 1, 0)
        
    # --- TEST 1: Header Removal ---
    def test_remove_running_headers(self):
        blocks = [self.header_block, self.content_block]
        
        cleaned = remove_headers(blocks, header_cutoff=75)
        
        self.assertEqual(len(cleaned), 1)
        self.assertEqual(cleaned[0][4], "Real Content")

    # --- TEST 2: Visual Warning Detection ---
    def test_format_page_content_visual_warning(self):
        mock_page = MagicMock()
        mock_page.get_images.return_value = [(1, 0, 0)] 

        image_rect = fitz.Rect(10, 100, 50, 150) 
        mock_page.get_image_rects.return_value = [image_rect]

        warning_text_block = (10, 160, 100, 180, "Do not touch hot surface", 0, 0)
        blocks = [warning_text_block]

        result = format_page_content(mock_page, blocks)

        self.assertIn("<CRITICAL_WARNING>", result)
        self.assertIn("[VISUAL HEADER DETECTED]", result)

    # --- TEST 3: Full Integration ---
    @patch("create_pdf_chunks.fitz.open") 
    def test_create_pdf_chunks_integration(self, mock_fitz_open):

        mock_doc = MagicMock()
        mock_page = MagicMock()
        
        mock_doc.__len__.return_value = 1
        mock_doc.__getitem__.return_value = mock_page
        mock_doc.__iter__.return_value = iter([mock_page])

        mock_fitz_open.return_value = mock_doc

        mock_page.get_text.return_value = [
            (10, 100, 200, 120, "Normal manual text.", 0, 0)
        ]
        mock_page.get_images.return_value = [] 

        chunks = create_pdf_chunks("dummy.pdf")

        self.assertEqual(len(chunks), 1) # This should now pass
        self.assertIn("Normal manual text", chunks[0]["content"])
        self.assertFalse(chunks[0]["metadata"]["has_critical_warning"])