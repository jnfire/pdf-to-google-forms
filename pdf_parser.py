import fitz  # PyMuPDF
import re

def extract_pdf_text(pdf_path):
    """Extracts text from a PDF file."""
    try:
        with fitz.open(pdf_path) as doc:
            return "".join(page.get_text("text") for page in doc)
    except Exception as e:
        print(f"Error reading PDF file {pdf_path}: {e}")
        return None

def extract_title(text, patterns):
    """Extracts the title from the text using the patterns from the config."""
    match = re.search(patterns['title'], text)
    if match:
        return match.group(1).strip()
    return "Cuestionario sin título"


def parse_questions(text, patterns):
    """Parses the questions text using the patterns from the config."""
    questions = []
    blocks = re.split(patterns['question'], '\n' + text.strip())

    for block in blocks:
        block = block.strip()
        if not block: continue

        lines = block.split('\n')
        question_title = lines[0]
        options = [line.strip() for line in lines[1:] if re.match(patterns['options'], line.strip())]

        if question_title and options:
            questions.append({"title": question_title, "options": options})

    return questions

def parse_answers(text, patterns):
    """Parses the answers text using the patterns from the config."""
    answers = {}
    matches = re.findall(patterns['answer'], text)
    for match in matches:
        answers[int(match[0])] = match[1].upper()
    return answers
