# Documentación de Uso

### ✨ Características Principales
- **Creación Dual**: Genera tanto exámenes con puntuación y respuestas correctas como encuestas simples.
- **Extracción Automática de Título**: Extrae automáticamente el título del formulario desde el contenido del PDF, el cual puede ser sobreescrito con un argumento en la línea de comandos.
- **Extractor Configurable**: Utiliza un archivo `config.json` para definir patrones de extracción, permitiendo adaptar el script a diferentes formatos de PDF sin modificar el código.
- **Automatización Completa**: Lee los PDF, crea el formulario, lo configura y añade todas las preguntas de forma automática.
- **Autenticación Segura**: Usa el flujo de autenticación OAuth 2.0 de Google para gestionar el acceso de forma segura.

### 📋 Requisitos
- Python 3.7 o superior.
- Una cuenta de Google.
- Haber habilitado la Google Forms API en un proyecto de Google Cloud y haber descargado el archivo `credentials.json`.

### ⚙️ Instalación
1.  **Clona el repositorio:**
    ```bash
    git clone https://github.com/tu_usuario/pdf-to-google-forms.git
    cd pdf-to-google-forms
    ```
2.  **Instala las dependencias:** Se recomienda crear un entorno virtual.
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

### 🛠️ Configuración
1.  **Credenciales de la API**: Coloca tu archivo `credentials.json` descargado de Google Cloud en la raíz del proyecto. La primera vez que ejecutes el script, se te pedirá que autorices el acceso a tu cuenta de Google en el navegador. Se creará un archivo `token.json` para futuras ejecuciones.

2.  **Archivo de Configuración (`config.json`)**: Este archivo define cómo el script encuentra el título, las preguntas y las respuestas en tus PDF usando expresiones regulares. Modifícalo si el formato de tus archivos es diferente.
    ```json
    {
      "extractor_patterns": {
        "title": "Cuestionario de Evaluación - (.*)",
        "question": "\\n(?=\\d+\\.\\s)",
        "options": "^[a-d]\\)",
        "answer": "(\\d+)\\.\\s+Respuesta Correcta:\\s+([A-Da-d])"
      }
    }
    ```

Aquí tienes algunos ejemplos de patrones que puedes usar en tu archivo `config.json`, dependiendo del formato de tu PDF:

| Caso de Uso               | Patrón                                      | Descripción                                                                   |
| ------------------------- | ------------------------------------------- | ----------------------------------------------------------------------------- |
| **Título**                |                                             |                                                                               |
| Título con un prefijo     | `"Cuestionario de Evaluación - (.*)"`         | Extrae el título que viene después de "Cuestionario de Evaluación - ".         |
| **Preguntas**             |                                             |                                                                               |
| Preguntas numeradas (1., 2.) | `"\\n(?=\\d+\\.\\s)"`                   | Divide el texto en preguntas basándose en un número seguido de un punto y un espacio. |
| Preguntas con un prefijo  | `"\n(?=Pregunta:\s\d+)"`             | Divide por "Pregunta:" seguido de un número.                                  |
| Preguntas multilínea (separadas por línea en blanco) | `"(?m)^\d+\.\s(?!\n\n)"` | Divide las preguntas que pueden ocupar varias líneas, buscando un número seguido de un punto, pero no si le sigue una línea en blanco. |
| **Opciones**              |                                             |                                                                               |
| Opciones con letra (a), b)) | `"^[a-d]\\)"`                             | Coincide con líneas que comienzan con una letra de la a a la d seguida de un paréntesis. |
| Opciones con letra (a., b.) | `"^[a-d]\\."`                             | Coincide con líneas que comienzan con una letra de la a a la d seguida de un punto.   |
| **Respuestas**            |                                             |                                                                               |
| "1. Respuesta Correcta: A" | `"(\\d+)\\.\\s+Respuesta Correcta:\\s+([A-Da-d])"` | Captura el número de la pregunta y la letra de la respuesta correcta.         |
| "Respuesta 1: A"          | `"Respuesta\\s+(\\d+):\\s+([A-Da-d])"`      | Captura el número de la pregunta y la letra correcta en un formato diferente. |


### 🚀 Uso
Ejecuta el script desde tu terminal, proporcionando los archivos PDF como argumentos.

**Para crear un Examen (con respuestas):**
Necesitas un PDF de preguntas y otro de respuestas.
```bash
python main.py "ruta/a/preguntas.pdf" "ruta/a/respuestas.pdf" --type quiz
```

**Para crear una Encuesta (sin respuestas):**
Solo necesitas el PDF de preguntas.
```bash
python main.py "ruta/a/preguntas.pdf" --type survey
```

**Sobrescribir el título:**
Por defecto, el script intentará extraer el título desde el PDF. Si quieres especificar un título personalizado, puedes usar el argumento `--title`:
```bash
python main.py "ruta/a/preguntas.pdf" --title "Mi Título Personalizado"
```

Al finalizar, el script te proporcionará los enlaces para editar y responder el formulario recién creado.
