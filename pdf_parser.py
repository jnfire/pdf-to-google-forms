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
    # The title is everything before the first question.
    blocks = re.split(patterns['question'], '\n' + text.strip())
    title_text = blocks[0]

    # Replace newlines with spaces to handle multi-line titles
    title_text = title_text.replace('\n', ' ')

    match = re.search(patterns['title'], title_text)
    if match:
        return match.group(1).strip()
    return "Cuestionario sin título"


def parse_questions(text, patterns):
    """Parses the questions text using the patterns from the config."""
    questions = []
    # Add a newline at the beginning to handle the case where the text starts with a question
    blocks = re.split(patterns['question'], '\n' + text.strip())

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        lines = block.split('\n')

        first_option_index = -1
        # Find the index of the first line that looks like an option
        for i, line in enumerate(lines):
            if re.match(patterns['options'], line.strip()):
                first_option_index = i
                break

        if first_option_index != -1:
            # Everything before the first option is the question
            question_lines = lines[:first_option_index]
            # Everything from the first option on is potentially an option
            option_lines = lines[first_option_index:]

            # Join the question lines, replacing newlines with spaces
            question_title = ' '.join(line.strip() for line in question_lines).strip()
            # Filter the option lines to get the actual options
            options = [line.strip() for line in option_lines if re.match(patterns['options'], line.strip())]

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
