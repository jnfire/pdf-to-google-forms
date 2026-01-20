import json
from config_loader import load_config
from core.pdf_parser import extract_pdf_text, parse_questions, parse_answers
from core.google_form_creator import generate_batch_requests


def main():
    patterns = load_config()
    q_text = extract_pdf_text('cuestionarios/examen-2.pdf')
    a_text = extract_pdf_text('cuestionarios/examen-2-respuestas.pdf')

    parsed_questions = parse_questions(q_text, patterns)
    correct_answers = parse_answers(a_text, patterns)

    requests = generate_batch_requests(parsed_questions, is_quiz=True, correct_answers=correct_answers, is_required=False)

    print(json.dumps({'parsed_questions': parsed_questions, 'correct_answers': correct_answers, 'requests': requests}, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
