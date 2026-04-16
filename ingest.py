from pathlib import Path
import pandas as pd

def load_synthetic_dataset(path: str | None = None) -> pd.DataFrame:
    if path is None:
        path = Path(__file__).resolve().parents[1] / "data" / "synthetic" / "check_metadata_sample.csv"
    return pd.read_csv(path)
