import os
from glob import glob

def find_question_answer_pairs(input_dir, answer_suffix='-soluciones'):
    """
    Finds pairs of question and answer PDF files in a directory.

    Args:
        input_dir (str): The directory to search for PDF files.
        answer_suffix (str): The suffix to identify answer files.

    Returns:
        list: A list of tuples, where each tuple contains the path to a question PDF
              and its corresponding answer PDF.
    """
    pdf_files = glob(os.path.join(input_dir, '*.pdf'))
    
    question_files = [f for f in pdf_files if answer_suffix not in f]
    answer_files = [f for f in pdf_files if answer_suffix in f]
    
    pairs = []
    for q_file in question_files:
        expected_a_file = q_file.replace('.pdf', f'{answer_suffix}.pdf')
        if expected_a_file in answer_files:
            pairs.append((q_file, expected_a_file))
            
    return pairs
