import pandas as pd
from src.features import engineer_features

def test_engineer_features_adds_expected_columns():
    df = pd.DataFrame([{
        "material_score": 0.5,
        "geo_risk_score": 0.7,
        "prior_return_count": 1
    }])
    result = engineer_features(df)
    assert "high_material_risk" in result.columns
    assert "high_geo_risk" in result.columns
    assert "return_history_flag" in result.columns
