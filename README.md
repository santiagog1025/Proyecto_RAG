# Optimización de Currículum con IA y RAG

Este proyecto utiliza **FastAPI**, **Streamlit** y **LangChain** para optimizar currículums en formato PDF según los requisitos de un puesto de trabajo específico. El sistema emplea un modelo de **Optimización de Currículum** que utiliza **RAG** (Retrieval-Augmented Generation) para extraer la información relevante del currículum y adaptarlo al puesto solicitado.

## Estructura del Proyecto

optimizacion_cv/ ├── app/ │ 

                 ├── main.py # Backend de FastAPI 
                 
                 │ └── models/ 
                 
                 │ └── optimizations.py # Lógica de optimización del currículum 
                 
                 ├── frontend/ │ └── streamlit_app.py # Interfaz de usuario en Streamlit 
                 
                 ├── requirements.txt # Dependencias del proyecto ├── README.md # Documentación del proyecto 
                 
                 ├── .gitignore # Archivos y carpetas a ignorar en Git 


## Tecnologías Utilizadas

- **FastAPI**: Framework moderno y rápido para construir APIs con Python 3.7+.
- **Streamlit**: Herramienta de desarrollo rápido para crear aplicaciones web interactivas.
- **LangChain**: Framework para el procesamiento de lenguaje natural (NLP) con modelos de lenguaje y RAG.
- **FAISS**: Biblioteca para búsqueda eficiente de vectores.
- **Hugging Face**: Modelos de embeddings para procesamiento de texto.

## Instalación

Sigue estos pasos para instalar y ejecutar el proyecto:

1. Clona el repositorio:

   ```bash
   git clone https://github.com/santiagog1025/Proyecto_RAG.git
   cd optimizacion_cv
Crea un entorno virtual (opcional pero recomendado):

En Linux/MacOS:

```bash
  python -m venv venv
  source venv/bin/activate
```
  En Windows:

```bash

  python -m venv venv
  venv\Scripts\activate
  Instala las dependencias:
```
```bash

pip install -r requirements.txt
Crea un archivo .env para configurar las claves de API necesarias (por ejemplo, GROQ_API_KEY).
```
Uso
Backend (FastAPI)
Inicia el servidor de FastAPI:

```bash
uvicorn app.main:app --reload
```
Esto iniciará la API en http://127.0.0.1:8000.

Frontend (Streamlit)
Ejecuta la interfaz de usuario de Streamlit:

```bash

streamlit run frontend/streamlit_app.py
```
Accede a la aplicación en http://localhost:8501 para cargar un currículum en formato PDF y especificar el puesto de trabajo deseado.

Sube un archivo PDF de tu currículum y especifica el puesto de trabajo.

Optimiza el CV: La aplicación enviará el archivo y el puesto a la API para que el sistema realice la optimización del currículum.

Ejemplo de Uso:
Currículum Subido: curriculum.pdf
Puesto de Trabajo: Data Scientist
La respuesta será un currículum optimizado que resalta la experiencia, habilidades, educación y logros más relevantes para el puesto de Data Scientist.


Contribuciones
¡Las contribuciones son bienvenidas! Si encuentras un error o tienes una idea para mejorar el proyecto, por favor abre un issue o envía un pull request.

Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.
