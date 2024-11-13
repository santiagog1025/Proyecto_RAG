# app/routes.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from models.optimizations import configurar_agente_rag

# Crear el enrutador
router = APIRouter()



@router.post("/optimize_cv/")
async def optimize_cv(file: UploadFile = File(...), job_position: str = ""):
    """
    Endpoint para optimizar el currículum en función de un cargo específico.
    """
    if not job_position:
        raise HTTPException(status_code=400, detail="Debe especificar el cargo deseado.")

    try:

        # Optimizar el currículum en función del cargo deseado
        optimizaciones = configurar_agente_rag(file.file, job_position)
        return {"optimizaciones": optimizaciones}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al optimizar el CV: {str(e)}")
