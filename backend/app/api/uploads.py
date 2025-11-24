from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
import uuid

router = APIRouter(prefix="/uploads", tags=["uploads"])

UPLOAD_DIR = Path("static/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

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
        "url": url,                 # para preview / abrir
        "filename": file.filename,  # nombre original
        "stored_name": filename,    # ⬅️ nombre físico (UUID + ext)
        "content_type": file.content_type,
    }


@router.get("/download/{stored_name}")
async def download_document(stored_name: str):
    """
    Fuerza la descarga del archivo guardado en static/uploads/{stored_name}.
    stored_name es el nombre que generamos con UUID.
    """
    file_path = UPLOAD_DIR / stored_name

    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

    # application/octet-stream para forzar descarga
    return FileResponse(
        path=file_path,
        media_type="application/octet-stream",
        filename=stored_name,      # o podrías buscar el nombre original si lo guardas en BD
    )
