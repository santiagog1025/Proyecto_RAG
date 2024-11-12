from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from typing import List
import os

# Configuración de embeddings de OpenAI
def configurar_embeddings() -> HuggingFaceEmbeddings:
    """
    Configura el modelo de embeddings de OpenAI.

    Returns:
        OpenAIEmbeddings: Modelo de embeddings configurado.
    """
    # Configura la clave de la API de OpenAI desde las variables de entorno
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("La API key de OpenAI no está configurada en las variables de entorno.")
    
    return HuggingFaceEmbeddings()

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
