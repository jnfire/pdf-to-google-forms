import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.pdf_parser import extract_title

class TestExtractTitle(unittest.TestCase):

    def setUp(self):
        """Set up test data before each test."""
        self.patterns = {
            "title": "Cuestionario de Evaluación - (.*)",
            "question": "\n(?=\d+\.\s)"
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

    def test_extract_title_multiline_success(self):
        """Test that a multiline title is extracted correctly."""
        sample_text_with_multiline_title = '''
Cuestionario de Evaluación - Tema 2: Ofimática
y Bases de Datos
1. What is a database?
   a) A collection of data
   b) A software to manage data
   c) Both a and b
   d) None of the above
'''
        expected_title = "Tema 2: Ofimática y Bases de Datos"
        parsed_title = extract_title(sample_text_with_multiline_title, self.patterns)
        self.assertEqual(parsed_title, expected_title)

    def test_extract_title_with_end_marker(self):
        """Test that a title is extracted correctly using an end marker."""
        patterns_with_marker = self.patterns.copy()
        patterns_with_marker['title_end_marker'] = 'Instrucciones'
        sample_text_with_marker = '''
Cuestionario de Evaluación - Tema 3: Redes
y Seguridad
Instrucciones: Lea atentamente las siguientes preguntas.
1. What is a firewall?
   a) A hardware device
   b) A software device
   c) Both a and b
   d) None of the above
'''
        expected_title = "Tema 3: Redes y Seguridad"
        parsed_title = extract_title(sample_text_with_marker, patterns_with_marker)
        self.assertEqual(parsed_title, expected_title)

if __name__ == '__main__':
    unittest.main()
