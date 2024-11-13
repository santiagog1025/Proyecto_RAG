from fastapi import FastAPI, File, UploadFile, HTTPException
import os
from tempfile import NamedTemporaryFile
from models.optimizations import configurar_agente_rag

app = FastAPI()

@app.post("/optimize_cv/")
async def optimize_cv(file: UploadFile = File(...), job_position: str = ""):
    """
    Endpoint para optimizar el currículum en función de un cargo específico.
    """
    print(f"Recibido job_position: {job_position}")
    print(f"Recibido archivo: {file.filename}")
    
    try:
        # Guardar el archivo temporalmente
        with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name
        
        # Optimizar el currículum usando la ruta temporal
        optimizaciones = configurar_agente_rag(tmp_path, job_position)
        
        # Borrar el archivo temporal después de su uso
        os.remove(tmp_path)
        
        return {"optimizaciones": optimizaciones}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al optimizar el CV: {str(e)}")
