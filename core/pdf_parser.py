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

    # If a title end marker is defined, use it to split the title
    title_end_marker = patterns.get('title_end_marker')
    if title_end_marker:
        # Split the text at the title end marker, case-insensitively
        parts = re.split(title_end_marker, title_text, maxsplit=1, flags=re.IGNORECASE)
        if len(parts) > 1:
            title_text = parts[0]

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
    """Parses the answers text using the patterns from the config.

    Now supports a configurable list `answer_patterns` in the config file. If
    `answer_patterns` exists it is tried in order; otherwise, the function will
    attempt the single `answer` pattern (for backward compatibility), and then
    a set of internal fallback patterns.
    """
    answers = {}
    if not text:
        return answers

    # Build the list of patterns to try in priority order
    patterns_to_try = []
    cfg_patterns = patterns.get('answer_patterns')
    if isinstance(cfg_patterns, list) and cfg_patterns:
        patterns_to_try.extend(cfg_patterns)
    # Backwards compatibility: single `answer` key
    primary = patterns.get('answer')
    if primary and primary not in patterns_to_try:
        patterns_to_try.append(primary)

    # Add internal fallback patterns if nothing matched from config
    internal_fallbacks = [
        r"(\d+)\.\s*Respuesta:\s*([A-Da-d])",
        r"Respuesta\s+(\d+):\s*([A-Da-d])",
        r"(\d+)\.\s*([A-Da-d])\b",
    ]

    # Try each pattern in order
    for p in patterns_to_try + internal_fallbacks:
        found = re.findall(p, text)
        if found:
            for match in found:
                try:
                    answers[int(match[0])] = match[1].upper()
                except Exception:
                    continue
            if answers:
                return answers

    return answers
