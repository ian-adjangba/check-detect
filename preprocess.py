import pandas as pd

def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned["payer_state"] = cleaned["payer_state"].astype(str).str.upper().str.strip()
    cleaned["payer_bank"] = cleaned["payer_bank"].astype(str).str.strip()
    return cleaned
