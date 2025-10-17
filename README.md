PDF to Google Forms Creator
🇬🇧 English version below

## Índice
- [Características](#✨-características-principales)
- [Instalación](#⚙️-instalación)
- [Configuración](#🛠️-configuración)
- [Uso](#🚀-uso)
- [Versiones](#versiones)
- [Licencia](#licencia)

🇪🇸 Documentación en Español
Este script de Python automatiza la creación de cuestionarios y encuestas en Google Forms a partir de archivos PDF. Extrae preguntas y respuestas de los documentos, y genera un formulario listo para usar a través de la API de Google Forms.

✨ Características Principales
Creación Dual: Genera tanto exámenes con puntuación y respuestas correctas como encuestas simples.

Extractor Configurable: Utiliza un archivo config.json para definir patrones de extracción, permitiendo adaptar el script a diferentes formatos de PDF sin modificar el código.

Automatización Completa: Lee los PDF, crea el formulario, lo configura y añade todas las preguntas de forma automática.

Autenticación Segura: Usa el flujo de autenticación OAuth 2.0 de Google para gestionar el acceso de forma segura.

📋 Requisitos
Python 3.7 o superior.

Una cuenta de Google.

Haber habilitado la Google Forms API en un proyecto de Google Cloud y haber descargado el archivo credentials.json.

⚙️ Instalación
Clona el repositorio:

```bash
git clone https://github.com/tu_usuario/pdf-to-google-forms.git
cd pdf-to-google-forms
```
Instala las dependencias: Se recomienda crear un entorno virtual.

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```
🛠️ Configuración
Credenciales de la API: Coloca tu archivo credentials.json descargado de Google Cloud en la raíz del proyecto. La primera vez que ejecutes el script, se te pedirá que autorices el acceso a tu cuenta de Google en el navegador. Se creará un archivo token.json para futuras ejecuciones.

Archivo de Configuración (config.json): Este archivo define cómo el script encuentra las preguntas y respuestas en tus PDF usando expresiones regulares. Modifícalo si el formato de tus archivos es diferente.

```json
{
  "extractor_patterns": {
    "question": "\\n(?=\\d+\\.\\s)",
    "options": "^[a-d]\\)",
    "response": "(\\d+)\\.\\s+Respuesta Correcta:\\s+([A-Da-d])\\)"
  }
}
```
🚀 Uso
Ejecuta el script desde tu terminal, proporcionando los archivos PDF como argumentos.

Para crear un Examen (con respuestas):
Necesitas un PDF de preguntas y otro de respuestas.

```bash
python crear_formulario.py "ruta/a/preguntas.pdf" "ruta/a/respuestas.pdf" --tipo examen
```
Para crear una Encuesta (sin respuestas):
Solo necesitas el PDF de preguntas.

```bash
python crear_formulario.py "ruta/a/preguntas.pdf" --tipo encuesta
```
Al finalizar, el script te proporcionará los enlaces para editar y responder el formulario recién creado.

## Versiones
- 0.1.0 - Versión inicial: extracción básica desde PDF, generación de formularios y compatibilidad con exámenes/encuestas.

## Licencia
Este proyecto se publica bajo la licencia MIT. Consulta el archivo `LICENSE` para el texto completo.

PDF to Google Forms Creator
🇬🇧 English Documentation
This Python script automates the creation of quizzes and surveys in Google Forms using PDF files as input. It extracts questions and answers from the documents and generates a ready-to-use form through the Google Forms API.

✨ Key Features
Dual Mode: Creates both self-grading quizzes with correct answers and simple surveys.

Configurable Extractor: Uses a config.json file to define extraction patterns, allowing you to adapt the script to different PDF formats without changing the code.

Full Automation: Reads the PDFs, creates the form, configures it, and adds all the questions automatically.

Secure Authentication: Uses Google's OAuth 2.0 authentication flow for secure access management.

📋 Requirements
Python 3.7 or higher.

A Google Account.

You must have the Google Forms API enabled in a Google Cloud project and have downloaded your credentials.json file.

⚙️ Installation
Clone the repository:

```bash
git clone https://github.com/your_username/pdf-to-google-forms.git
cd pdf-to-google-forms
```
Install dependencies: It is recommended to use a virtual environment.

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
🛠️ Configuration
API Credentials: Place your downloaded credentials.json file from Google Cloud in the project's root directory. The first time you run the script, you will be prompted to authorize access to your Google Account in your browser. A token.json file will be created to store credentials for future runs.

Configuration File (config.json): This file defines how the script finds questions and answers in your PDFs using regular expressions. Modify it if your file format is different.

```json
{
  "extractor_patterns": {
    "question": "\\n(?=\\d+\\.\\s)",
    "options": "^[a-d]\\)",
    "response": "(\\d+)\\.\\s+Respuesta Correcta:\\s+([A-Da-d])\\)"
  }
}
```
🚀 Usage
Run the script from your terminal, providing the PDF files as arguments.

To create a Quiz (with answers):
You need a PDF for questions and another for the answers.

```bash
python crear_formulario.py "path/to/questions.pdf" "path/to/answers.pdf" --tipo examen
```
To create a Survey (without answers):
You only need the questions PDF.

```bash
python crear_formulario.py "path/to/questions.pdf" --tipo encuesta
```
Upon completion, the script will provide you with the links to edit and view the newly created form.

## Versiones
- 0.1.0 - Initial version: basic extraction from PDF, form generation, and support for quizzes/surveys.

## Licencia
This project is licensed under the MIT License. See the `LICENSE` file for details.
