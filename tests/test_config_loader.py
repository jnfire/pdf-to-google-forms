import unittest
import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config_loader import load_config

class TestConfigLoader(unittest.TestCase):

    def setUp(self):
        """Set up test data before each test."""
        self.config_path = 'config.json'

    def tearDown(self):
        """Clean up after each test."""
        if os.path.exists(self.config_path):
            os.remove(self.config_path)

    def create_config_file(self, data):
        """Helper function to create a config file."""
        with open(self.config_path, 'w') as f:
            json.dump(data, f)

    def test_load_config_success(self):
        """Test that the config is loaded correctly."""
        config_data = {
            "extractor_patterns": {
                "question": "\n(?=\d+\.\s)",
                "options": "^[a-d]\)",
                "answer": "(\d+)\.\s+Correct Answer:\s+([A-Da-d])"
            }
        }
        self.create_config_file(config_data)
        loaded_patterns = load_config()
        self.assertEqual(loaded_patterns, config_data['extractor_patterns'])

    def test_load_config_file_not_found(self):
        """Test that a FileNotFoundError is raised when the config file is not found."""
        # The test will run in the root of the project, so the config.json will be found.
        # I will remove the file before running the test.
        if os.path.exists(self.config_path):
            os.remove(self.config_path)
        with self.assertRaises(FileNotFoundError):
            load_config()

    def test_load_config_invalid_json(self):
        """Test that a json.JSONDecodeError is raised when the config file is not valid JSON."""
        with open(self.config_path, 'w') as f:
            f.write("{'invalid_json':}")
        with self.assertRaises(json.JSONDecodeError):
            load_config()

    def test_load_config_with_question_prefix(self):
        """Test loading config with a question prefix pattern."""
        config_data = {
            "extractor_patterns": {
                "question": "\n(?=Question:\s\d+)"
            }
        }
        self.create_config_file(config_data)
        loaded_patterns = load_config()
        self.assertEqual(loaded_patterns, config_data['extractor_patterns'])

    def test_load_config_with_lettered_options_dot(self):
        """Test loading config with lettered options ending in a dot."""
        config_data = {
            "extractor_patterns": {
                "options": "^[a-d]\."
            }
        }
        self.create_config_file(config_data)
        loaded_patterns = load_config()
        self.assertEqual(loaded_patterns, config_data['extractor_patterns'])

    def test_load_config_with_answer_prefix(self):
        """Test loading config with an answer prefix pattern."""
        config_data = {
            "extractor_patterns": {
                "answer": "Answer\s+(\d+):\s+([A-Da-d])"
            }
        }
        self.create_config_file(config_data)
        loaded_patterns = load_config()
        self.assertEqual(loaded_patterns, config_data['extractor_patterns'])

if __name__ == '__main__':
    unittest.main()
