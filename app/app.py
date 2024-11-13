import streamlit as st
import requests

# URL de tu API de FastAPI (ajusta la URL si es diferente)
API_URL = "http://127.0.0.1:8000/optimize_cv/"

def optimizar_cv(file, job_position):
    """Hace la solicitud POST a FastAPI para optimizar el CV."""
    # Leer el archivo PDF como bytes
    file_bytes = file.read()
    
    # Asegúrate de enviar el archivo como multipart/form-data
    files = {'file': ('curriculum.pdf', file_bytes, 'application/pdf')}
    data = {'job_position': job_position}

    # Mostrar los datos que se enviarán para depuración
    st.write("Enviando datos a FastAPI:")
    st.write(data)  # Imprime los datos enviados

    try:
        # Realizar la solicitud POST
        response = requests.post(API_URL, files=files, data=data)
        response.raise_for_status()  # Esto genera una excepción si el código de estado HTTP no es 2xx
        return response.json()  # Retorna la respuesta como JSON
    except requests.exceptions.RequestException as e:
        st.error(f"Error al hacer la solicitud: {e}")
        return None

# Título de la aplicación
st.title("Optimización de Currículum")

# Subir el archivo PDF
uploaded_file = st.file_uploader("Cargar tu currículum (PDF)", type="pdf")

# Especificar el puesto de trabajo
job_position = st.text_input("Especifica el cargo deseado", "")

# Verificar si el archivo y el puesto han sido cargados antes de habilitar el botón
if uploaded_file is not None and job_position.strip() != "":
    # Botón para optimizar el CV
    if st.button("Optimizar CV"):
        with st.spinner("Optimizando..."):
            result = optimizar_cv(uploaded_file, job_position)

            # Verificar si hay un resultado
            if result is not None:
                if "optimizaciones" in result:
                    st.success("¡Optimización completada!")
                    st.write(result["optimizaciones"])
                else:
                    st.error(f"Error en la optimización: {result.get('detail', 'Desconocido')}")
else:
    st.warning("Por favor, carga un currículum y especifica un cargo deseado.")
