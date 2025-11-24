from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.requests import router as requests_router
from app.api.uploads import router as uploads_router

app = FastAPI(
    title="KYC Verification API",
    description="""
API para gestionar solicitudes de verificación (KYC), subir documentos,
evaluar riesgo y administrar los archivos almacenados en el servidor.

Incluye:
- Creación, consulta, actualización y eliminación de solicitudes KYC.
- Carga y descarga segura de documentos.
- Exposición de archivos estáticos (imágenes, PDFs, etc.).
- Ruta de salud para monitoreo.
    """,
    version="1.0.0",
)

origins = [
    "https://sasskyc.lozoya.org",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)

app.include_router(requests_router)
app.include_router(uploads_router)

@app.get(
    "/health",
    summary="Health Check",
    description="Endpoint simple para verificar que la API está en ejecución.",
)
async def health():
    """
    Devuelve un estado básico para uso en herramientas de monitoreo
    como UptimeRobot, AWS Load Balancers, Docker Healthchecks, etc.
    """
    return {"status": "ok"}
