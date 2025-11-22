from app.schemas.request import VerificationRequestCreate
from app.services.request_service import build_request_document


def test_build_request_document_sets_pending_status_and_fields():
    payload = VerificationRequestCreate(
        full_name="Juan",
        email="juan@gmail.com",
        phone="55555555",
        country="MX",
        document_type="INE",
        document_number="ABC123456",
        document_image_url="https://example.com/doc.png",
    )

    doc = build_request_document(payload)

    assert doc["status"] == "pending"
    assert "risk_score" in doc
    assert "risk_level" in doc
    assert "created_at" in doc
