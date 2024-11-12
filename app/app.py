# streamlit_app.py

import streamlit as st
import requests

# Configuración de la aplicación de Streamlit
st.set_page_config(page_title="Optimizador de Currículums", layout="centered")

# Encabezado de la aplicación
st.title("Optimizador de Currículums")
st.write("Sube tu currículum en PDF y recibe sugerencias para optimizarlo según el cargo deseado.")

# Cargar el archivo PDF
uploaded_file = st.file_uploader("Cargar currículum en PDF", type=["pdf"])

# Campo para ingresar el cargo deseado
job_position = st.text_input("Cargo al que deseas aplicar")

# Botón para procesar el currículum
if st.button("Optimizar Currículum"):
    # Verificar que se haya cargado un archivo y especificado el cargo
    if uploaded_file is not None and job_position:
        # Enviar el archivo PDF y el cargo a la API
        try:
            # Enviar el archivo a la API para extraer el texto
            files = {"file": uploaded_file.getvalue()}
            response = requests.post("http://localhost:8000/upload_cv/", files=files)

            if response.status_code == 200:
                texto_cv = response.json().get("texto_cv", "")

                # Enviar el texto y cargo para obtener las sugerencias de optimización
                data = {"file": uploaded_file.getvalue(), "job_position": job_position}
                optimize_response = requests.post("http://localhost:8000/optimize_cv/", files=files, data={"job_position": job_position})

                if optimize_response.status_code == 200:
                    sugerencias = optimize_response.json().get("optimizaciones", {}).get("sugerencias", [])

                    # Mostrar las sugerencias
                    st.subheader("Sugerencias de Optimización:")
                    for idx, sugerencia in enumerate(sugerencias, 1):
                        st.write(f"{idx}. {sugerencia}")
                else:
                    st.error("Error al optimizar el currículum. Inténtalo de nuevo.")
            else:
                st.error("Error al leer el archivo PDF. Asegúrate de que esté en el formato correcto.")
        except Exception as e:
            st.error(f"Ocurrió un error: {str(e)}")
    else:
        st.warning("Por favor, carga un currículum y especifica el cargo.")
