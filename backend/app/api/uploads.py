from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
import uuid

router = APIRouter(prefix="/uploads", tags=["uploads"])

# Directorio base donde se guardan los archivos subidos.
UPLOAD_DIR = Path("static/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Tipos MIME permitidos para los documentos subidos.
ALLOWED_CONTENT_TYPES = {
    "image/png",
    "image/jpeg",
    "image/jpg",
    "image/webp",
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}


@router.post("/document")
async def upload_document(file: UploadFile = File(...)):
    """
    Sube un documento o imagen al servidor.

    - Valida que el `content_type` del archivo esté en `ALLOWED_CONTENT_TYPES`.
    - Genera un nombre físico único (`stored_name`) usando UUID + extensión original.
    - Guarda el archivo en `static/uploads/{stored_name}`.
    - Devuelve:
      - `url`: URL relativa para acceder/visualizar el archivo (por ejemplo: `/static/uploads/...`).
      - `filename`: nombre original del archivo enviado por el usuario.
      - `stored_name`: nombre físico generado (UUID).
      - `content_type`: tipo de contenido detectado por FastAPI.

    Esta respuesta se puede usar en el frontend para:
    - mostrar una vista previa (imágenes),
    - o generar un botón de descarga usando la ruta `/uploads/download/{stored_name}`.
    """
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Tipo de archivo no permitido: {file.content_type}",
        )

    ext = Path(file.filename).suffix or ""
    filename = f"{uuid.uuid4().hex}{ext}"
    filepath = UPLOAD_DIR / filename

    contents = await file.read()
    with open(filepath, "wb") as f:
        f.write(contents)

    url = f"/static/uploads/{filename}"

    return {
        "url": url,
        "filename": file.filename,
        "stored_name": filename,
        "content_type": file.content_type,
    }


@router.get("/download/{stored_name}")
async def download_document(stored_name: str):
    """
    Fuerza la descarga de un archivo previamente subido.

    - `stored_name`: nombre físico del archivo (UUID + extensión)
      tal como se guardó en `static/uploads/`.
    - Si el archivo no existe en disco, devuelve 404.

    La respuesta se envía como `application/octet-stream` para que el navegador
    trate el archivo como descarga directa.
    """
    file_path = UPLOAD_DIR / stored_name

    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

    # application/octet-stream para forzar descarga
    return FileResponse(
        path=file_path,
        media_type="application/octet-stream",
        filename=stored_name,
    )
