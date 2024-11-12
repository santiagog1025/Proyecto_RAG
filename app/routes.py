# app/routes.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from app.utils import leer_pdf
from app.models.optimizations import optimizar_cv

# Crear el enrutador
router = APIRouter()

@router.post("/upload_cv/")
async def upload_cv(file: UploadFile = File(...)):
    """
    Endpoint para subir un archivo de currículum en PDF y extraer el texto.
    """
    try:
        # Leer el contenido del archivo PDF
        texto_cv = leer_pdf(file)
        return {"texto_cv": texto_cv}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el PDF: {str(e)}")


@router.post("/optimize_cv/")
async def optimize_cv(file: UploadFile = File(...), job_position: str = ""):
    """
    Endpoint para optimizar el currículum en función de un cargo específico.
    """
    if not job_position:
        raise HTTPException(status_code=400, detail="Debe especificar el cargo deseado.")

    try:
        # Leer el contenido del archivo PDF
        texto_cv = leer_pdf(file)

        # Optimizar el currículum en función del cargo deseado
        optimizaciones = optimizar_cv(texto_cv, job_position)
        return {"optimizaciones": optimizaciones}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al optimizar el CV: {str(e)}")
