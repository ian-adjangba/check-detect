import pandas as pd
from src.scorer import score_check

def test_score_check_returns_expected_keys():
    row = pd.Series({
        "material_score": 0.5,
        "sequence_gap_flag": 1,
        "routing_number_valid": 0,
        "micr_match": 0,
        "duplicate_check_flag": 1,
        "geo_risk_score": 0.8,
        "prior_return_count": 1,
    })
    result = score_check(row)
    assert "risk_score" in result
    assert "recommendation" in result
    assert "reasons" in result
