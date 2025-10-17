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
├── google_form_creator.py
├── LICENSE
├── main.py
├── pdf_parser.py
├── README.md
└── requirements.txt
```

### Módulos

- **`main.py`**: El punto de entrada principal del script. Maneja los argumentos de la línea de comandos y orquesta el proceso de creación de formularios.
- **`config_loader.py`**: Responsable de cargar los patrones de extracción desde el archivo `config.json`.
- **`pdf_parser.py`**: Contiene la lógica para extraer texto de archivos PDF y analizar las preguntas y respuestas.
- **`google_form_creator.py`**: Maneja la autenticación con la API de Google y la creación del formulario de Google.

### Pruebas

El proyecto utiliza el framework de pruebas integrado de Python `unittest`. Las pruebas se encuentran en el directorio `tests`.

Para ejecutar las pruebas, ejecuta el siguiente comando desde la raíz del proyecto:

```bash
python -m unittest discover tests
```
