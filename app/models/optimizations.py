from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains import LLMChain
import os

def leer_pdf(file) -> str:
    """
    Lee un archivo PDF usando LangChain y extrae su contenido como texto.

    Args:
        file (UploadFile): Archivo PDF cargado.

    Returns:
        str: Texto extraído del PDF.
    """
    try:
        loader = PyPDFLoader(file)
        
        # Cargar el documento
        documento = loader.load()
        return documento

    except Exception as e:
        raise ValueError(f"Error al leer el archivo PDF: {str(e)}")

# Configuración de RAG
def configurar_rag(documento, puesto) -> RetrievalQA:
    """
    Configura la cadena RAG para el modelo de optimización de CV.

    Args:
        documentos (list): Lista de textos de referencia para el almacenamiento vectorial.

    Returns:
        RetrievalQA: Cadena RAG configurada.
    """
    # Configurar embeddings y vector store
    documento = leer_pdf(documento)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    docs = text_splitter.split_documents(documento)
    
    # Crear embeddings
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    vector_store = FAISS.from_documents(docs, embeddings)
    
    # Configurar el modelo de lenguaje y el prompt
    prompt_template =f"""
            "Lee el siguiente currículum y extrae las partes más importantes relacionadas con la consulta del usuario. Proporciona detalles clave como la experiencia laboral, habilidades técnicas, formación académica, logros, certificaciones y cualquier otra información relevante que responda directamente a la consulta. Asegúrate de que la información extraída sea específica y organizada, y destaca las secciones que se ajusten mejor a lo que está buscando el usuario.

            Consulta del usuario: {puesto}


            Responde con la información más relevante relacionada con la consulta que debería estar relacionada al puesto de trabajo al que aspira el usuario. ten en cuenta que tienes un máximo de 1000 tokens para responder"
    """
    # Crear la cadena RAG
    llm = ChatGroq(model_name="mixtral-8x7b-32768", groq_api_key=os.getenv("GROQ_API_KEY"), temperature= 0, max_tokens=1000)
    rag_chain = RetrievalQA.from_chain_type(
        retriever=vector_store.as_retriever(),
        return_source_documents=True,
        llm=llm
    )
    response = rag_chain.invoke(prompt_template)
    return response['result']

# Definir un agente que reciba la salida de la herramienta RAG y genere una respuesta en español
def configurar_agente_rag(documento, puesto):
    """
    Configura el agente LangChain que toma la respuesta de la herramienta RAG y genera una respuesta optimizada en español.

    Args:
        documento (str): Ruta del documento PDF.
        puesto (str): Nombre del puesto de trabajo objetivo.
    
    Returns:
        str: Respuesta generada por el agente en español.
    """
    # Obtener la respuesta de la herramienta RAG
    resultado_rag = configurar_rag(documento, puesto)
    
    # Definir un prompt para el agente LangChain
    prompt_template = f"""
    Rol: Eres un asistente virtual especializado en optimización de currículums, utilizando técnicas avanzadas para mejorar la presentación y alineación del perfil del candidato con los requisitos de un puesto específico. Tu tarea es analizar el currículum proporcionado por el usuario para el puesto de trabajo {puesto} y ofrecer recomendaciones detalladas para optimizar el perfil del candidato.

    Información proporcionada:
    
    Análisis del currículum: {resultado_rag}
    Puesto de trabajo: {puesto}
    Instrucciones:
    
    Revisa cuidadosamente el currículum y compáralo con los requisitos del puesto proporcionado.
    Utiliza técnicas de optimización de currículums para mejorar la efectividad del perfil del candidato. Algunas técnicas incluyen:
    Resaltar logros cuantificables.
    Asegurar la inclusión de palabras clave relevantes para el puesto.
    Optimizar la estructura para facilitar la lectura y destacar las secciones más importantes.
    Usar un formato atractivo y profesional que facilite el escaneo rápido por los reclutadores.
    Proporciona recomendaciones específicas para mejorar el currículum, basándote en las áreas que necesitan mayor ajuste para alinearse mejor con el puesto de trabajo.
    Haz énfasis en los siguientes aspectos:
    Experiencia laboral: Sugiere cómo resaltar logros clave o responsabilidades relevantes, utilizando verbos de acción y cifras cuantificables.
    Habilidades técnicas: Identifica habilidades faltantes que podrían ser incluidas, si el candidato las posee, y cómo presentarlas de manera efectiva.
    Educación y formación: Señala cómo resaltar títulos o certificaciones relevantes para el puesto, destacando cualquier formación adicional pertinente.
    Logros y competencias adicionales: Recomendaciones sobre cómo mejorar la sección de logros y habilidades blandas, utilizando ejemplos concretos cuando sea posible.
    Personaliza la respuesta si el candidato menciona su nombre, utilizando un tono amigable y motivacional.
    Objetivo: Ayudar al candidato a mejorar su currículum para aumentar sus posibilidades de éxito en la postulación al puesto de {puesto}, utilizando técnicas de optimización de currículums que lo hagan destacar entre otros postulantes."""



    # Crear un modelo de lenguaje de LangChain 
    llm = ChatGroq(model="gemma2-9b-it", groq_api_key=os.getenv("GROQ_API_KEY"), max_tokens=1000) 

    # Crear un LLMChain con el prompt y el modelo
    llm_chain = LLMChain(prompt=PromptTemplate.from_template(prompt_template), llm=llm)

    # Ejecutar el agente para generar la respuesta
    respuesta = llm_chain.run(prompt= puesto)
    
    return respuesta

