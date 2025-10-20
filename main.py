import argparse
from config_loader import load_config
from pdf_parser import extract_pdf_text, parse_questions, parse_answers, extract_title
from google_form_creator import authenticate, create_form, batch_update_form

def main():
    """Main function to run the script."""
    parser = argparse.ArgumentParser(description="Create a Google Form from PDF files.")
    parser.add_argument("questions_pdf", help="Path to the PDF file with the questions.")
    parser.add_argument("answers_pdf", nargs='?', default=None, help="(Optional) Path to the PDF with the answers for quiz mode.")
    parser.add_argument("--type", choices=['quiz', 'survey'], default='quiz', help="Defines if the form is a 'quiz' (with answers) or a 'survey' (without answers).")
    parser.add_argument("--title", default=None, help="Title of the Google Form.")
    args = parser.parse_args()

    if args.type == 'quiz' and not args.answers_pdf:
        parser.error("The 'quiz' type requires an answer file.")

    patterns = load_config()
    forms_service = authenticate()

    print("Reading and processing PDF files...")
    questions_text = extract_pdf_text(args.questions_pdf)

    form_title = args.title
    if not form_title:
        extracted_title = extract_title(questions_text, patterns)
        if extracted_title:
            form_title = extracted_title

    parsed_questions = parse_questions(questions_text, patterns=patterns)

    correct_answers = {}
    if args.type == 'quiz':
        answers_text = extract_pdf_text(args.answers_pdf)
        correct_answers = parse_answers(answers_text, patterns)

    print(f"Creating a form of type: '{args.type}'...")
    form_result = create_form(forms_service, title=form_title)
    form_id = form_result['formId']

    requests = []
    if args.type == 'quiz':
        requests.append({"updateSettings": {"settings": {"quizSettings": {"isQuiz": True}}, "updateMask": "quizSettings.isQuiz"}})

    for i, q in enumerate(parsed_questions):
        options = [{'value': opt.split(')', 1)[1].strip()} for opt in q['options']]

        question_body = {
            "required": True,
            "choiceQuestion": {"type": "RADIO", "options": options}
        }

        if args.type == 'quiz':
            correct_letter = correct_answers.get(i + 1)
            if correct_letter:
                correct_index = ord(correct_letter) - ord('A')
                if 0 <= correct_index < len(options):
                    question_body["grading"] = {
                        "pointValue": 1,
                        "correctAnswers": {"answers": [{"value": options[correct_index]['value']}]}
                    }

        requests.append({
            "createItem": {
                "item": {"title": q['title'], "questionItem": {"question": question_body}},
                "location": {"index": i},
            }
        })

    batch_update_form(forms_service, form_id, requests)

    print("\nForm created successfully! 🚀")
    print(f"You can respond to it here: {form_result['responderUri']}")

if __name__ == "__main__":
    main()
