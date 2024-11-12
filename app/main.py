# app/main.py

from fastapi import FastAPI
from routes import router

# Inicializar la aplicación de FastAPI
app = FastAPI(
    title="Optimizador de Currículums",
    description="Una API para optimizar currículums en función de los cargos deseados",
    version="1.0.0"
)

# Incluir las rutas desde el archivo routes.py
app.include_router(router)

# Ejecutar la aplicación de FastAPI (solo para desarrollo)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
