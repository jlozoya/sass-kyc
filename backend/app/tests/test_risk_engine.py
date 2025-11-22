from app.services.risk_engine import compute_risk


def test_low_risk():
    result = compute_risk("user@gmail.com", "MX", "ABC123456")
    assert result.level == "low"
    assert result.score == 0


def test_high_risk_temp_email_and_restricted_country():
    result = compute_risk("foo@mailinator.com", "IR", "123")
    assert result.score > 70
    assert result.level == "high"
