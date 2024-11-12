# app/models/optimizations_rag.py

from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from app.models.embeddings_model import crear_vector_store
from typing import List, Dict

def optimizar_cv_rag(texto_cv: str, job_position: str, documentos: List[str]) -> Dict[str, List[str]]:
    """
    Optimiza el currículum en función de un cargo específico, sugiriendo mejoras usando RAG.

    Args:
        texto_cv (str): Texto extraído del currículum.
        job_position (str): Cargo al cual se quiere postular.
        documentos (List[str]): Lista de textos/documentos para contexto adicional.

    Returns:
        dict: Diccionario con sugerencias de optimización para mejorar el CV.
    """
    # Crear la base de datos de embeddings con Chroma
    vector_store = crear_vector_store(documentos)

    # Configurar el modelo de lenguaje y la plantilla de prompt
    llm = ChatGroq(model_name="mixtral-8x7b-32768")
    prompt_template = PromptTemplate(
        input_variables=["context", "cv_text", "job_position"],
        template=(
  "Contexto del puesto de trabajo:\n"
    "{context}\n\n"
    "Currículum:\n"
    "{cv_text}\n\n"
    "Puesto objetivo:\n"
    "{job_position}\n\n"
    "Instrucciones:\n"
    "1. Analiza el currículum proporcionado en relación con los requisitos y responsabilidades del puesto de trabajo descrito.\n"
    "2. Identifica las competencias clave, habilidades y experiencias requeridas para el puesto.\n"
    "3. Proporciona una lista de sugerencias de mejora para optimizar el currículum, destacando cómo resaltar las habilidades más relevantes, experiencias previas y logros de manera que se alineen mejor con las expectativas del empleador.\n"
    "4. Asegúrate de que las sugerencias estén enfocadas en mejorar la claridad, relevancia y impacto del perfil del candidato para que se ajuste al puesto de trabajo objetivo."
        )
    )

    # Crear la cadena RAG con LangChain
    cadena_rag = RetrievalQA(
        retriever=vector_store.as_retriever(),
        llm=llm,
        prompt=prompt_template
    )

    # Generar el contexto y hacer la consulta al modelo LLM
    context = vector_store.similarity_search(texto_cv, k=5)
    context_text = " ".join([doc.page_content for doc in context])  # Concatenar el contexto recuperado

    # Formatear el prompt y obtener sugerencias
    prompt_final = prompt_template.format(context=context_text, cv_text=texto_cv, job_position=job_position)

    try:
        # Llamar al modelo de lenguaje con el prompt y generar sugerencias
        respuesta = cadena_rag({"question": prompt_final})
        sugerencias = respuesta['answer'].split("\n")
        return {"sugerencias": [s.strip() for s in sugerencias if s.strip()]}  # Filtrar sugerencias vacías
    except Exception as e:
        raise ValueError(f"Error al generar sugerencias de optimización con RAG: {str(e)}")
