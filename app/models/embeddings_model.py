from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from typing import List
import os

# Configuración de embeddings de Hugging Face
def configurar_embeddings() -> HuggingFaceEmbeddings:
    """
    Configura el modelo de embeddings de Hugging Face.

    Returns:
        HuggingFaceEmbeddings: Modelo de embeddings configurado.
    """
    # Configura la clave de la API de Hugging Face desde las variables de entorno
    hf_api_key = os.getenv("HUGGINGFACE_API_KEY")
    if not hf_api_key:
        raise ValueError("La API key de Hugging Face no está configurada en las variables de entorno.")
    
    # Asumiendo que se utiliza un modelo preentrenado de Hugging Face
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")  # Se puede personalizar según el modelo que se prefiera

# Crear la base de datos de embeddings con Chroma para búsquedas de similaridad
def crear_vector_store(documentos: List[str]) -> Chroma:
    """
    Crea una base de datos Chroma con embeddings para los documentos dados.

    Args:
        documentos (List[str]): Lista de textos a incluir en el almacenamiento de vectores.

    Returns:
        Chroma: Objeto Chroma con los documentos indexados.
    """
    embeddings = configurar_embeddings()
    # Crear la base de datos Chroma desde los textos
    vector_store = Chroma.from_texts(documentos, embeddings, collection_name="cv_optimizations")
    return vector_store
