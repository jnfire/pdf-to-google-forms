import unittest
from core.google_form_creator import generate_batch_requests

class TestGoogleFormCreator(unittest.TestCase):
    def setUp(self):
        self.parsed_questions = [
            {
                'title': 'Question 1',
                'options': ['a) Option A', 'b) Option B', 'c) Option C', 'd) Option D']
            }
        ]
        self.correct_answers = {1: 'B'}

    def test_generate_requests_survey_not_required(self):
        """Test generating requests for a survey where questions are not required."""
        requests = generate_batch_requests(self.parsed_questions, is_quiz=False, correct_answers={}, is_required=False)

        # Check that quiz settings are not present
        self.assertFalse(any("updateSettings" in r for r in requests))

        # Check question content
        create_item = requests[0]["createItem"]["item"]
        question_body = create_item["questionItem"]["question"]

        self.assertFalse(question_body["required"])
        self.assertEqual(len(question_body["choiceQuestion"]["options"]), 4)

    def test_generate_requests_survey_required(self):
        """Test generating requests for a survey where questions are required."""
        requests = generate_batch_requests(self.parsed_questions, is_quiz=False, correct_answers={}, is_required=True)

        create_item = requests[0]["createItem"]["item"]
        question_body = create_item["questionItem"]["question"]

        self.assertTrue(question_body["required"])

    def test_generate_requests_quiz_required(self):
        """Test generating requests for a quiz where questions are required."""
        requests = generate_batch_requests(self.parsed_questions, is_quiz=True, correct_answers=self.correct_answers, is_required=True)

        # Check quiz settings
        self.assertTrue(any("updateSettings" in r for r in requests))

        # Check question content
        # The first request is updateSettings, the second is createItem
        create_item = requests[1]["createItem"]["item"]
        question_body = create_item["questionItem"]["question"]

        self.assertTrue(question_body["required"])

        # Check grading
        self.assertIn("grading", question_body)
        self.assertEqual(question_body["grading"]["pointValue"], 1)
        self.assertEqual(question_body["grading"]["correctAnswers"]["answers"][0]["value"], "Option B")

    def test_generate_requests_quiz_not_required(self):
        """Test generating requests for a quiz where questions are not required."""
        requests = generate_batch_requests(self.parsed_questions, is_quiz=True, correct_answers=self.correct_answers, is_required=False)

        create_item = requests[1]["createItem"]["item"]
        question_body = create_item["questionItem"]["question"]

        self.assertFalse(question_body["required"])

if __name__ == '__main__':
    unittest.main()
