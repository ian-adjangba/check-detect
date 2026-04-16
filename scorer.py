import pandas as pd

def score_check(row: pd.Series) -> dict:
    score = 0.0
    reasons = []

    if row.get("material_score", 1) < 0.70:
        score += 0.30
        reasons.append("Material score is below expected threshold")

    if row.get("sequence_gap_flag", 0) == 1:
        score += 0.20
        reasons.append("Check number appears out of sequence")

    if row.get("routing_number_valid", 1) == 0:
        score += 0.20
        reasons.append("Routing number validation failed")

    if row.get("micr_match", 1) == 0:
        score += 0.15
        reasons.append("MICR line inconsistency detected")

    if row.get("duplicate_check_flag", 0) == 1:
        score += 0.25
        reasons.append("Duplicate check pattern detected")

    if row.get("geo_risk_score", 0) > 0.50:
        score += 0.10
        reasons.append("Geographic profile is outside normal expectations")

    if row.get("prior_return_count", 0) > 0:
        score += 0.10
        reasons.append("Payer has prior return history")

    score = min(score, 1.0)

    if score >= 0.70:
        recommendation = "Escalate for review"
    elif score >= 0.40:
        recommendation = "Use caution"
    else:
        recommendation = "Low immediate risk"

    return {
        "risk_score": round(score, 2),
        "recommendation": recommendation,
        "reasons": reasons,
    }
