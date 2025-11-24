from fastapi import APIRouter, Depends, HTTPException, Query
from bson import ObjectId
from datetime import datetime, timezone

from app.core.db import get_collection
from app.schemas.request import (
    VerificationRequestCreate,
    VerificationRequestUpdateStatus,
    VerificationRequestOut,
)
from app.services.risk_engine import compute_risk

router = APIRouter(prefix="/requests", tags=["requests"])


def serialize_request(doc) -> VerificationRequestOut:
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
    return get_collection()


@router.post("", response_model=VerificationRequestOut)
async def create_request(
    payload: VerificationRequestCreate,
    col=Depends(get_requests_collection),
):
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
