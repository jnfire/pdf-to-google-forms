# Documentación para Desarrolladores

Este documento proporciona información para los desarrolladores que trabajan en este proyecto.

## Estructura del Proyecto

El proyecto está estructurado de la siguiente manera:

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

### Módulos

- **`main.py`**: El punto de entrada principal del script. Maneja los argumentos de la línea de comandos y orquesta el proceso de creación de formularios. Nuevo: soporta la opción `--debug` que imprime las preguntas parseadas, las respuestas detectadas y el payload de `requests` sin autenticar ni llamar a la API de Google.
- **`config_loader.py`**: Responsable de cargar los patrones de extracción desde el archivo `config.json`.
- **`core/pdf_parser.py`**: Contiene la lógica para extraer texto de archivos PDF y analizar las preguntas y respuestas. Actualizado para soportar una lista configurable `answer_patterns` leída desde `config.json` y patrones de respaldo.
- **`core/google_form_creator.py`**: Maneja la autenticación con la API de Google y la creación del formulario de Google.

### Configuración

El archivo `config.json` contiene un mapeo `extractor_patterns`. Claves destacadas:
- `title`, `question`, `options` — igual que antes.
- `answer` — patrón único legado (compatibilidad hacia atrás).
- `answer_patterns` — nuevo: lista de expresiones regulares (strings) que se probarán en orden para extraer respuestas. El parser usa el primer patrón que devuelve coincidencias.

Esto hace que la compatibilidad con distintos formatos de PDFs de respuestas sea configurable sin cambiar el código.

### Pruebas y depuración

- Pruebas unitarias: el proyecto usa el framework `unittest` de Python. Las pruebas están en `tests/`.

Ejecuta todas las pruebas:

```bash
python -m unittest discover -v
```

- Depuración de extracción: usa la opción `--debug` en `main.py` para inspeccionar la salida del parser y el payload exacto de `requests` que se enviaría a la API de Google Forms, sin realizar autenticación ni llamadas de red. Esto es útil para iterar en los patrones de `config.json` rápidamente.

Ejemplo:

```bash
python main.py "cuestionarios/examen-2.pdf" "cuestionarios/examen-2-respuestas.pdf" --type quiz --debug
```

### Re-autenticación rápida (OAuth)
Si encuentras errores de OAuth como `invalid_grant`, elimina `token.json` y ejecuta de nuevo para forzar la re-autenticación en tu navegador.

```bash
rm token.json
python main.py "cuestionarios/examen-2.pdf" "cuestionarios/examen-2-respuestas.pdf" --type quiz
```


### Notas para contribuyentes
- Mantén las entradas de `config.json` con barras escapadas (backslashes dobles) al escribir patrones regex en JSON.
- Al añadir pruebas para nuevos patrones de extracción, proporciona un `test_config.json` pequeño y un texto de ejemplo para que las pruebas no dependan del `config.json` del desarrollador.
