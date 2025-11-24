from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Literal

RequestStatus = Literal["pending", "approved", "rejected", "requires_info"]
RiskLevel = Literal["low", "medium", "high"]

class VerificationRequestBase(BaseModel):
    full_name: str = Field(..., min_length=3)
    email: EmailStr
    phone: str
    country: str
    document_type: str
    document_number: str
    document_image_url: str
    original_document_filename: str

class VerificationRequestCreate(VerificationRequestBase):
    pass

class VerificationRequestUpdateStatus(BaseModel):
    status: RequestStatus

class VerificationRequestOut(VerificationRequestBase):
    id: str
    status: RequestStatus
    risk_score: int
    risk_level: RiskLevel
    created_at: datetime
