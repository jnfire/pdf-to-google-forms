# Developer Documentation

This document provides information for developers working on this project.

## Project Structure

The project is structured as follows:

```
.
.
├── docs/
│   ├── DEVELOPMENT.md
│   ├── DEVELOPMENT.es.md
│   ├── USAGE.md
│   └── USAGE.es.md
├── tests/
│   └── test_pdf_parser.py
├── core/
│   └── google_form_creator.py
│   └── pdf_parser.py
├── .gitignore
├── config.json
├── config_loader.py
├── LICENSE
├── main.py
├── README.md
└── requirements.txt
```

### Modules

- **`main.py`**: The main entry point of the script. It handles command-line arguments and orchestrates the form creation process.
- **`config_loader.py`**: Responsible for loading the extraction patterns from the `config.json` file.
- **`pdf_parser.py`**: Contains the logic for extracting text from PDF files and parsing questions and answers.
- **`google_form_creator.py`**: Handles the authentication with the Google API and the creation of the Google Form.

### Testing

The project uses Python's built-in `unittest` framework for testing. The tests are located in the `tests` directory.

To run the tests, execute the following command from the root of the project:

```bash
python -m unittest discover tests
```
