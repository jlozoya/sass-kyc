from fastapi import APIRouter, Depends, HTTPException, Query
from bson import ObjectId
from datetime import datetime, timezone
from pathlib import Path
from app.core.db import get_collection
from app.schemas.request import (
    VerificationRequestCreate,
    VerificationRequestUpdateStatus,
    VerificationRequestOut,
)
from app.services.risk_engine import compute_risk

router = APIRouter(prefix="/requests", tags=["requests"])

UPLOAD_BASE_DIR = Path("static")


def serialize_request(doc) -> VerificationRequestOut:
    """
    Normaliza un documento de la base de datos MongoDB al esquema
    `VerificationRequestOut` usado por las respuestas de la API.

    - Convierte `_id` de ObjectId a `str`.
    - Asegura que `original_document_filename` exista (string vacío por defecto).
    """
    return VerificationRequestOut(
        id=str(doc["_id"]),
        full_name=doc["full_name"],
        email=doc["email"],
        phone=doc["phone"],
        country=doc["country"],
        document_type=doc["document_type"],
        document_number=doc["document_number"],
        document_image_url=doc["document_image_url"],
        original_document_filename=doc.get("original_document_filename", ""),
        status=doc["status"],
        risk_score=doc["risk_score"],
        risk_level=doc["risk_level"],
        created_at=doc["created_at"],
    )


async def get_requests_collection():
    """
    Devuelve la colección de MongoDB donde se almacenan las solicitudes KYC.

    Esta función se usa como dependencia de FastAPI para inyectar la colección
    en cada handler.
    """
    return get_collection()


@router.post("", response_model=VerificationRequestOut)
async def create_request(
    payload: VerificationRequestCreate,
    col=Depends(get_requests_collection),
):
    """
    Crea una nueva solicitud de verificación (KYC).

    - Calcula el riesgo con `compute_risk` usando email, país y número de documento.
    - Guarda la solicitud en la colección con estado inicial `pending`.
    - Persiste también el nombre original del archivo y la URL del documento subido.
    - Devuelve la solicitud recién creada normalizada al esquema `VerificationRequestOut`.
    """
    risk = compute_risk(
        email=payload.email,
        country=payload.country,
        document_number=payload.document_number,
    )

    now = datetime.now(timezone.utc)

    doc = {
        "full_name": payload.full_name,
        "email": payload.email,
        "phone": payload.phone,
        "country": payload.country,
        "document_type": payload.document_type,
        "document_number": payload.document_number,
        "document_image_url": payload.document_image_url,
        "original_document_filename": payload.original_document_filename,
        "status": "pending",
        "risk_score": risk.score,
        "risk_level": risk.level,
        "created_at": now,
        "updated_at": now,
    }

    result = await col.insert_one(doc)
    created = await col.find_one({"_id": result.inserted_id})
    return serialize_request(created)


@router.get("", response_model=list[VerificationRequestOut])
async def list_requests(
    col=Depends(get_requests_collection),
    name: str | None = Query(default=None),
    status: str | None = Query(default=None),
):
    """
    Lista las solicitudes de verificación.

    Filtros opcionales:
    - `name`: filtra por nombre completo usando una búsqueda parcial
      (case-insensitive) sobre `full_name`.
    - `status`: filtra por estado exacto (`pending`, `approved`, `rejected`, etc.).

    Las solicitudes se devuelven ordenadas por `created_at` descendente
    (las más recientes primero).
    """
    query: dict = {}
    if name:
        # búsqueda simple por nombre (case-insensitive)
        query["full_name"] = {"$regex": name, "$options": "i"}
    if status:
        query["status"] = status

    cursor = col.find(query).sort("created_at", -1)
    items: list[VerificationRequestOut] = []
    async for doc in cursor:
        items.append(serialize_request(doc))
    return items


@router.get("/{request_id}", response_model=VerificationRequestOut)
async def get_request(request_id: str, col=Depends(get_requests_collection)):
    """
    Obtiene el detalle de una solicitud de verificación por su ID.

    - `request_id`: string con el ObjectId de MongoDB.
    - Si el ID no es válido, devuelve 400.
    - Si no se encuentra ninguna solicitud, devuelve 404.
    """
    try:
        oid = ObjectId(request_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID")

    doc = await col.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Request not found")
    return serialize_request(doc)


@router.patch("/{request_id}/status", response_model=VerificationRequestOut)
async def update_status(
    request_id: str,
    payload: VerificationRequestUpdateStatus,
    col=Depends(get_requests_collection),
):
    """
    Actualiza únicamente el estado (`status`) de una solicitud existente.

    - `request_id`: ID de la solicitud (ObjectId en string).
    - `payload.status`: nuevo estado (`pending`, `approved`, `rejected`, `requires_info`, etc.).
    - También actualiza el campo `updated_at` a la hora actual en UTC.
    - Si el ID no es válido, devuelve 400.
    - Si la solicitud no existe, devuelve 404.
    """
    try:
        oid = ObjectId(request_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID")

    result = await col.find_one_and_update(
        {"_id": oid},
        {"$set": {"status": payload.status, "updated_at": datetime.now(timezone.utc)}},
        return_document=True,
    )

    if not result:
        raise HTTPException(status_code=404, detail="Request not found")

    return serialize_request(result)


@router.delete("/{request_id}", status_code=204)
async def delete_request(request_id: str, col=Depends(get_requests_collection)):
    """
    Elimina una solicitud de verificación y, si aplica, el archivo asociado.

    - `request_id`: ID de la solicitud (ObjectId en string).
    - Si el ID no es válido, devuelve 400.
    - Si la solicitud no existe, devuelve 404.
    - Si la solicitud tiene `document_image_url` apuntando a `/static/...`,
      intenta eliminar el archivo físico del sistema de archivos.
    - Devuelve 204 (sin contenido) en caso de éxito.
    """
    try:
        oid = ObjectId(request_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID")

    doc = await col.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Request not found")

    await col.delete_one({"_id": oid})

    url = doc.get("document_image_url")
    if isinstance(url, str) and url.startswith("/static/"):
        try:
            # Construimos la ruta completa a partir de la URL almacenada
            relative_path = url.lstrip("/")
            file_path = Path(relative_path)

            full_path = UPLOAD_BASE_DIR.parent / file_path
            if full_path.is_file():
                full_path.unlink()
        except Exception:
            # En caso de error al borrar el archivo, no interrumpimos la respuesta
            pass

    return
