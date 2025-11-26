# User Documentation

### ✨ Key Features
- **Dual Mode**: Creates both self-grading quizzes with correct answers and simple surveys.
- **Automatic Title Extraction**: Automatically extracts the form title from the PDF content, which can be overridden with a command-line argument.
- **Configurable Extractor**: Uses a `config.json` file to define extraction patterns, allowing you to adapt the script to different PDF formats without changing the code.
- **Full Automation**: Reads the PDFs, creates the form, configures it, and adds all the questions automatically.
- **Secure Authentication**: Uses Google's OAuth 2.0 authentication flow for secure access management.

### 📋 Requirements
- Python 3.7 or higher.
- A Google Account.
- You must have the Google Forms API enabled in a Google Cloud project and have downloaded your `credentials.json` file.

### ⚙️ Installation
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your_username/pdf-to-google-forms.git
    cd pdf-to-google-forms
    ```
2.  **Install dependencies:** It is recommended to use a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

### 🛠️ Configuration
1.  **API Credentials**: Place your downloaded `credentials.json` file from Google Cloud in the project's root directory. The first time you run the script, you will be prompted to authorize access to your Google Account in your browser. A `token.json` file will be created to store credentials for future runs.

2.  **Configuration File (`config.json`)**: This file defines how the script finds the title, questions, and answers in your PDFs using regular expressions. Modify it if your file format is different.
    ```json
    {
      "extractor_patterns": {
        "title": "Cuestionario de Evaluación - (.*)",
        "question": "\\n(?=\\d+\\.\\s)",
        "options": "^[a-d]\\)",
        "answer": "(\\d+)\\.\\s+Correct Answer:\\s+([A-Da-d])"
      }
    }
    ```

Here are some examples of patterns you can use in your `config.json` file, depending on the format of your PDF:

| Use Case                  | Pattern                                     | Description                                                                 |
| ------------------------- | ------------------------------------------- | --------------------------------------------------------------------------- |
| **Title**                 |                                             |                                                                             |
| Title with a prefix       | `"Cuestionario de Evaluación - (.*)"`         | Extracts the title that comes after "Cuestionario de Evaluación - ".         |
| **Questions**             |                                             |                                                                             |
| Numbered questions (1., 2.) | `"\\n(?=\\d+\\.\\s)"`                   | Splits the text into questions based on a number followed by a dot and a space. |
| Questions with a prefix   | `"\n(?=Question:\s\d+)"`              | Splits by "Question:" followed by a number.                                 |
| Multi-line questions (separated by a blank line) | `"(?m)^\d+\.\s(?!\n\n)"` | Splits questions that may span multiple lines, looking for a number followed by a dot, but not if followed by a blank line. |
| **Options**               |                                             |                                                                             |
| Lettered options (a), b)) | `"^[a-d]\\)"`                             | Matches lines starting with a letter from a to d followed by a parenthesis. |
| Lettered options (a., b.) | `"^[a-d]\\."`                             | Matches lines starting with a letter from a to d followed by a dot.         |
| **Answers**               |                                             |                                                                             |
| "1. Correct Answer: A"    | `"(\\d+)\\.\\s+Correct Answer:\\s+([A-Da-d])"` | Captures the question number and the correct letter.                        |
| "Answer 1: A"             | `"Answer\\s+(\\d+):\\s+([A-Da-d])"`         | Captures the question number and the correct letter in a different format.  |


### 🚀 Usage
Run the script from your terminal, providing the PDF files as arguments.

**To create a Quiz (with answers):**
You need a PDF for questions and another for the answers.
```bash
python main.py "path/to/questions.pdf" "path/to/answers.pdf" --type quiz
```

**To create a Survey (without answers):**
You only need the questions PDF.
```bash
python main.py "path/to/questions.pdf" --type survey
```

**Overriding the title:**
By default, the script will try to extract the title from the PDF. If you want to specify a custom title, you can use the `--title` argument:
```bash
python main.py "path/to/questions.pdf" --title "My Custom Title"
```

**Making questions required:**
By default, questions are not mandatory. To make all questions required, use the `--required` flag:
```bash
python main.py "path/to/questions.pdf" --required
```

Upon completion, the script will provide you with the links to edit and view the newly created form.
