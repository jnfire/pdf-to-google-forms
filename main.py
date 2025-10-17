import argparse
from config_loader import load_config
from pdf_parser import extract_pdf_text, parse_questions, parse_answers, extract_title
from google_form_creator import authenticate, create_form, batch_update_form
from batch_processor import find_question_answer_pairs

def create_form_from_pdfs(questions_pdf, answers_pdf, form_type, title, patterns, forms_service):
    """Creates a single Google Form from a pair of PDF files."""
    print(f"Processing file: {questions_pdf}")
    questions_text = extract_pdf_text(questions_pdf)

    form_title = title
    if not form_title:
        extracted_title = extract_title(questions_text, patterns)
        if extracted_title:
            form_title = extracted_title
        else:
            form_title = "Automatically Generated Questionnaire"

    parsed_questions = parse_questions(questions_text, patterns=patterns)

    correct_answers = {}
    if form_type == 'quiz':
        answers_text = extract_pdf_text(answers_pdf)
        correct_answers = parse_answers(answers_text, patterns)

    print(f"Creating a form of type: '{form_type}' with title '{form_title}'...")
    form_result = create_form(forms_service, title=form_title)
    form_id = form_result['formId']

    requests = []
    if form_type == 'quiz':
        requests.append({"updateSettings": {"settings": {"quizSettings": {"isQuiz": True}}, "updateMask": "quizSettings.isQuiz"}})

    for i, q in enumerate(parsed_questions):
        options = [{'value': opt.split(')', 1)[1].strip()} for opt in q['options']]

        question_body = {
            "required": True,
            "choiceQuestion": {"type": "RADIO", "options": options}
        }

        if form_type == 'quiz':
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
    print(f"You can view and edit it here: {form_result['responderUri'].replace('viewform', 'edit')}")
    print(f"You can respond to it here: {form_result['responderUri']}")

def main():
    """Main function to run the script."""
    parser = argparse.ArgumentParser(description="Create a Google Form from PDF files.")
    parser.add_argument("--mode", choices=['single', 'batch'], default='single', help="Processing mode: 'single' for one form, 'batch' for multiple.")
    parser.add_argument("--input-dir", help="Directory containing PDF files for batch processing.")
    parser.add_argument("--answer-suffix", default='-soluciones', help="Suffix for answer files in batch mode.")
    parser.add_argument("--questions-pdf", help="Path to the PDF file with the questions (for single mode).")
    parser.add_argument("--answers-pdf", nargs='?', default=None, help="(Optional) Path to the PDF with the answers for quiz mode (for single mode).")
    parser.add_argument("--type", choices=['quiz', 'survey'], default='quiz', help="Defines if the form is a 'quiz' (with answers) or a 'survey' (without answers).")
    parser.add_argument("--title", default=None, help="Title of the Google Form. Overrides extracted title.")
    args = parser.parse_args()

    patterns = load_config()
    forms_service = authenticate()

    if args.mode == 'single':
        if not args.questions_pdf:
            parser.error("The 'single' mode requires a questions PDF file path.")
        if args.type == 'quiz' and not args.answers_pdf:
            parser.error("The 'quiz' type in 'single' mode requires an answer file.")
        create_form_from_pdfs(args.questions_pdf, args.answers_pdf, args.type, args.title, patterns, forms_service)
    
    elif args.mode == 'batch':
        if not args.input_dir:
            parser.error("The 'batch' mode requires an input directory.")
        
        pairs = find_question_answer_pairs(args.input_dir, args.answer_suffix)
        if not pairs:
            print("No question-answer pairs found in the specified directory.")
            return
            
        for q_pdf, a_pdf in pairs:
            create_form_from_pdfs(q_pdf, a_pdf, args.type, args.title, patterns, forms_service)

if __name__ == "__main__":
    main()