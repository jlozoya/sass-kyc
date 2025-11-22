from dataclasses import dataclass

RISKY_EMAIL_DOMAINS = {"mailinator.com", "tempmail.com", "yopmail.com"}
RESTRICTED_COUNTRIES = {"IR", "KP", "SY", "CU", "RU"}


@dataclass
class RiskResult:
    score: int
    level: str  # "low" | "medium" | "high"


def compute_risk(email: str, country: str, document_number: str) -> RiskResult:
    score = 0

    domain = email.split("@")[-1].lower()
    if domain in RISKY_EMAIL_DOMAINS:
        score += 40

    if country.upper() in RESTRICTED_COUNTRIES:
        score += 40

    if len(document_number.strip()) < 6:
        score += 30

    if score <= 30:
        level = "low"
    elif score <= 70:
        level = "medium"
    else:
        level = "high"

    return RiskResult(score=score, level=level)
