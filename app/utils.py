from langchain.document_loaders import PyMuPDFLoader
from fastapi import UploadFile
import io

def leer_pdf(file: UploadFile) -> str:
    """
    Lee un archivo PDF usando LangChain y extrae su contenido como texto.

    Args:
        file (UploadFile): Archivo PDF cargado.

    Returns:
        str: Texto extraído del PDF.
    """
    try:
        # Convertir el archivo UploadFile a un archivo tipo BytesIO y luego a PyMuPDFLoader
        pdf_bytes = io.BytesIO(file.file.read())
        loader = PyMuPDFLoader(pdf_bytes)
        
        # Cargar el documento
        documento = loader.load()
        
        # Concatenar el texto de todas las páginas
        texto = " ".join([page.page_content for page in documento])
        return texto

    except Exception as e:
        raise ValueError(f"Error al leer el archivo PDF: {str(e)}")

def extraer_datos(texto: str) -> dict:
    """
    Extrae datos clave del texto del currículum para facilitar la optimización.
    Esta función es un punto de partida y puede adaptarse según las necesidades.

    Args:
        texto (str): Texto extraído del currículum.

    Returns:
        dict: Diccionario con datos relevantes extraídos del texto.
    """
    datos_extraidos = {
        "experiencia": [],  # Lista de experiencias laborales
        "educacion": [],    # Lista de antecedentes académicos
        "habilidades": []   # Lista de habilidades
    }

    # Lógica de extracción (personalizable): Utiliza NLP o regex para identificar secciones específicas

    return datos_extraidos
