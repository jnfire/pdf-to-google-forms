# User Documentation

### ✨ Key Features
- **Dual Mode**: Creates both self-grading quizzes with correct answers and simple surveys.
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

2.  **Configuration File (`config.json`)**: This file defines how the script finds questions and answers in your PDFs using regular expressions. Modify it if your file format is different.
    ```json
    {
      "extractor_patterns": {
        "question": "\\n(?=\\d+\\.\\s)",
        "options": "^[a-d]\\)",
        "answer": "(\\d+)\\.\\s+Correct Answer:\\s+([A-Da-d])"
      }
    }
    ```

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
Upon completion, the script will provide you with the links to edit and view the newly created form.
