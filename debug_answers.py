import re
from config_loader import load_config
from core.pdf_parser import extract_pdf_text

patterns = load_config()
answers_text = extract_pdf_text('cuestionarios/examen-2-respuestas.pdf')

print('--- Extracted answers text (repr, up to 5000 chars) ---')
print(repr(answers_text)[:5000])
print('\n--- Patterns used ---')
print(patterns)

print('\n--- re.findall using patterns["answer"] ---')
if answers_text:
    matches = re.findall(patterns['answer'], answers_text)
    print(matches)
else:
    print('No text extracted or empty string')

# Try additional common patterns to detect format
common_patterns = [
    r"(\d+)\.\s+Correct Answer:\s+([A-Da-d])",
    r"(\d+)\.\s+Respuesta Correcta:\s+([A-Da-d])",
    r"Respuesta\s+(\d+):\s+([A-Da-d])",
    r"(\d+)\)\s+\(?([A-Da-d])\)?",
    r"(\d+)\.\s*([A-Da-d])\b",
]
print('\n--- Testing common answer patterns ---')
if answers_text:
    for p in common_patterns:
        found = re.findall(p, answers_text)
        print(p, '->', found[:10])
else:
    print('Skipping common patterns: no text')
