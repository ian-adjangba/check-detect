import pandas as pd

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    featured = df.copy()
    featured["high_material_risk"] = (featured["material_score"] < 0.70).astype(int)
    featured["high_geo_risk"] = (featured["geo_risk_score"] > 0.50).astype(int)
    featured["return_history_flag"] = (featured["prior_return_count"] > 0).astype(int)
    return featured
