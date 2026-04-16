from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from src.ingest import load_synthetic_dataset
from src.preprocess import clean_dataset
from src.features import engineer_features

def run_baseline_model() -> str:
    df = load_synthetic_dataset()
    df = clean_dataset(df)
    df = engineer_features(df)

    model_df = df[df["fraud_label"].isin([0, 1])].copy()
    model_df["fraud_binary"] = model_df["fraud_label"]

    feature_cols = [
        "amount",
        "material_score",
        "sequence_gap_flag",
        "routing_number_valid",
        "micr_match",
        "duplicate_check_flag",
        "geo_risk_score",
        "prior_return_count",
        "high_material_risk",
        "high_geo_risk",
        "return_history_flag",
    ]

    X = model_df[feature_cols]
    y = model_df["fraud_binary"]

    if len(model_df) < 4:
        return "Not enough data to run baseline model."

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.4, random_state=42
    )

    clf = RandomForestClassifier(random_state=42, n_estimators=50)
    clf.fit(X_train, y_train)
    predictions = clf.predict(X_test)

    return classification_report(y_test, predictions, zero_division=0)
