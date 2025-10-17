import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pdf_parser import extract_title

class TestExtractTitle(unittest.TestCase):

    def setUp(self):
        """Set up test data before each test."""
        self.patterns = {
            "title": "Cuestionario de Evaluación - (.*)"
        }
        self.sample_text_with_title = """
Cuestionario de Evaluación - Tema 1: Informática Básica y Ofimática
1. What is the capital of France?
   a) London
   b) Paris
   c) Berlin
   d) Madrid
"""
        self.sample_text_without_title = """
1. What is the capital of France?
   a) London
   b) Paris
   c) Berlin
   d) Madrid
"""

    def test_extract_title_success(self):
        """Test that the title is extracted correctly."""
        expected_title = "Tema 1: Informática Básica y Ofimática"
        parsed_title = extract_title(self.sample_text_with_title, self.patterns)
        self.assertEqual(parsed_title, expected_title)

    def test_extract_title_no_title(self):
        """Test that a default title is returned when no title is found."""
        expected_title = "Cuestionario sin título"
        parsed_title = extract_title(self.sample_text_without_title, self.patterns)
        self.assertEqual(parsed_title, expected_title)

if __name__ == '__main__':
    unittest.main()
