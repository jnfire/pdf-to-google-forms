# Documentación de Uso

### ✨ Características Principales
- **Creación Dual**: Genera tanto exámenes con puntuación y respuestas correctas como encuestas simples.
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

2.  **Archivo de Configuración (`config.json`)**: Este archivo define cómo el script encuentra las preguntas y respuestas en tus PDF usando expresiones regulares. Modifícalo si el formato de tus archivos es diferente.
    ```json
    {
      "extractor_patterns": {
        "question": "\n(?=\d+\.\s)",
        "options": "^[a-d]\)",
        "answer": "(\d+)\.\s+Correct Answer:\s+([A-Da-d])"
      }
    }
    ```

### 🚀 Uso
Ejecuta el script desde tu terminal, proporcionando los archivos PDF como argumentos.

**Para crear un Examen (con respuestas):**
Necesitas un PDF de preguntas y otro de respuestas.
```bash
python main.py "ruta/a/preguntas.pdf" "ruta/a/respuestas.pdf" --type examen
```

**Para crear una Encuesta (sin respuestas):**
Solo necesitas el PDF de preguntas.
```bash
python main.py "ruta/a/preguntas.pdf" --type encuesta
```
Al finalizar, el script te proporcionará los enlaces para editar y responder el formulario recién creado.
