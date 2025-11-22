from datetime import datetime
from .risk_engine import compute_risk
from app.schemas.request import VerificationRequestCreate


def build_request_document(payload: VerificationRequestCreate) -> dict:
    risk = compute_risk(
        email=payload.email,
        country=payload.country,
        document_number=payload.document_number,
    )
    now = datetime.utcnow()
    return {
        "full_name": payload.full_name,
        "email": payload.email,
        "phone": payload.phone,
        "country": payload.country,
        "document_type": payload.document_type,
        "document_number": payload.document_number,
        "document_image_url": payload.document_image_url,
        "status": "pending",
        "risk_score": risk.score,
        "risk_level": risk.level,
        "created_at": now,
        "updated_at": now,
    }
