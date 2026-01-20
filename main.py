import argparse
import json
from config_loader import load_config
from core.pdf_parser import extract_pdf_text, parse_questions, parse_answers, extract_title
from core.google_form_creator import authenticate, create_form, batch_update_form, generate_batch_requests


def main():
    """Main function to run the script."""
    parser = argparse.ArgumentParser(description="Create a Google Form from PDF files.")
    parser.add_argument("questions_pdf", help="Path to the PDF file with the questions.")
    parser.add_argument("answers_pdf", nargs='?', default=None, help="(Optional) Path to the PDF with the answers for quiz mode.")
    parser.add_argument("--type", choices=['quiz', 'survey'], default='quiz', help="Defines if the form is a 'quiz' (with answers) or a 'survey' (without answers).")
    parser.add_argument("--title", default=None, help="Title of the Google Form.")
    parser.add_argument("--required", action="store_true", help="If set, questions will be mandatory.")
    parser.add_argument("--debug", action="store_true", help="Print parsed questions, answers and requests and exit (no API calls).")
    args = parser.parse_args()

    if args.type == 'quiz' and not args.answers_pdf:
        parser.error("The 'quiz' type requires an answer file.")

    patterns = load_config()

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

    requests = generate_batch_requests(parsed_questions, args.type == 'quiz', correct_answers, args.required)

    if args.debug:
        # Print the parsed data and the requests in JSON and exit without calling Google API
        output = {
            'title': form_title,
            'parsed_questions': parsed_questions,
            'correct_answers': correct_answers,
            'requests': requests
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
        return

    # Only authenticate and create the form when not in debug mode
    forms_service = authenticate()

    print(f"Creating a form of type: '{args.type}'...")
    form_result = create_form(forms_service, title=form_title)
    form_id = form_result['formId']

    batch_update_form(forms_service, form_id, requests)

    print("\nForm created successfully! 🚀")
    print(f"You can respond to it here: {form_result['responderUri']}")

if __name__ == "__main__":
    main()
