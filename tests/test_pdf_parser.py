import unittest
import sys
import os

# Add the parent directory to the sys.path to allow imports from the main project folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pdf_parser import parse_questions, parse_answers

class TestPdfParser(unittest.TestCase):

    def setUp(self):
        """Set up test data before each test."""
        self.patterns = {
            "question": "\n(?=\d+\.\s)",
            "options": "^[a-d]\)",
            "answer": "(\d+)\.\s+Correct Answer:\s+([A-Da-d])"
        }
        self.sample_questions_text = """
1. What is the capital of France?
   a) London
   b) Paris
   c) Berlin
   d) Madrid

2. What is 2 + 2?
   a) 3
   b) 4
   c) 5
   d) 6
"""
        self.sample_answers_text = """
1. Correct Answer: B
2. Correct Answer: B
"""

    def test_parse_questions_success(self):
        """Test that questions are parsed correctly."""
        expected_questions = [
            {
                'title': '1. What is the capital of France?',
                'options': ['a) London', 'b) Paris', 'c) Berlin', 'd) Madrid']
            },
            {
                'title': '2. What is 2 + 2?',
                'options': ['a) 3', 'b) 4', 'c) 5', 'd) 6']
            }
        ]
        parsed_questions = parse_questions(self.sample_questions_text, self.patterns)
        self.assertEqual(parsed_questions, expected_questions)

    def test_parse_questions_empty_text(self):
        """Test parsing with empty text."""
        parsed_questions = parse_questions("", self.patterns)
        self.assertEqual(parsed_questions, [])

    def test_parse_answers_success(self):
        """Test that answers are parsed correctly."""
        expected_answers = {
            1: 'B',
            2: 'B'
        }
        parsed_answers = parse_answers(self.sample_answers_text, self.patterns)
        self.assertEqual(parsed_answers, expected_answers)

    def test_parse_answers_empty_text(self):
        """Test parsing answers with empty text."""
        parsed_answers = parse_answers("", self.patterns)
        self.assertEqual(parsed_answers, {})

if __name__ == '__main__':
    unittest.main()