# Developer Documentation

This document provides information for developers working on this project.

## Project Structure

The project is structured as follows:

```
.
├── docs/
│   ├── DEVELOPMENT.md
│   ├── DEVELOPMENT.es.md
│   ├── USAGE.md
│   └── USAGE.es.md
├── tests/
│   └── test_pdf_parser.py
├── .gitignore
├── config.json
├── config_loader.py
├── core/
│   ├── pdf_parser.py
│   └── google_form_creator.py
├── LICENSE
├── main.py
├── README.md
└── requirements.txt
```

### Modules

- **`main.py`**: The main entry point of the script. It handles command-line arguments and orchestrates the form creation process. New: supports a `--debug` flag that prints the parsed questions, detected correct answers and the requests payload without authenticating or calling Google APIs.
- **`config_loader.py`**: Responsible for loading the extraction patterns from the `config.json` file.
- **`core/pdf_parser.py`**: Contains the logic for extracting text from PDF files and parsing questions and answers. Updated to support a configurable list `answer_patterns` read from `config.json` and fallbacks.
- **`core/google_form_creator.py`**: Handles the authentication with the Google API and the creation of the Google Form.

### Configuration

The `config.json` file contains an `extractor_patterns` mapping. Notable keys:
- `title`, `question`, `options` — same as before.
- `answer` — legacy/single pattern supported for backward compatibility.
- `answer_patterns` — new: a list of regular expressions (strings) that will be tried in order to extract answers. The parser uses the first pattern that returns matches.

This makes supporting various answer PDF formats configurable without changing code.

### Testing and Debugging

- Unit tests: the project uses Python's `unittest` framework. Tests are in `tests/`.

Run all tests:

```bash
python -m unittest discover -v
```

- Debugging extraction: use the `--debug` flag on `main.py` to inspect the parser output and the exact `requests` payload that would be sent to the Google Forms API, without performing authentication or network calls. This is useful to iterate on `config.json` patterns quickly.

Example:

```bash
python main.py "cuestionarios/examen-2.pdf" "cuestionarios/examen-2-respuestas.pdf" --type quiz --debug
```

### Quick OAuth troubleshooting
If you encounter OAuth errors like `invalid_grant`, remove `token.json` and run again to force re-authentication in your browser.

```bash
rm token.json
python main.py "cuestionarios/examen-2.pdf" "cuestionarios/examen-2-respuestas.pdf" --type quiz
```


### Notes for contributors
- Keep `config.json` entries escaped (JSON double-escaped backslashes) when writing regex patterns.
- When adding tests for new extraction patterns, provide a small `test_config.json` and sample text so tests do not rely on the developer's local `config.json`.
