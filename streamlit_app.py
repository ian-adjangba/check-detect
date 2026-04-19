
import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Check Detect",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

BRANCH_OPTIONS = [
    "Retail Branch",
    "Drive-Through Branch",
    "Flagship Branch",
    "University Branch",
    "Downtown Branch",
    "Suburban Branch",
    "Call Center",
]

COUNTRY_OPTIONS = [
    "United States", "Canada", "United Kingdom", "Ghana", "Togo", "South Africa",
    "Nigeria", "Germany", "France", "Mexico", "Jamaica", "Brazil", "India",
    "China", "Japan", "Australia", "Ireland", "Kenya", "Liberia", "Italy"
]

TRANSACTION_TYPES = ["Cashing", "Depositing", "Cashback"]
DISCREPANCY_TYPES = ["Check Number", "Routing Number", "Payer Geography"]

DEFAULT_DATA_PATHS = [
    Path("data/synthetic/check_metadata_sample.csv"),
    Path("/kaggle/input/datasets/ianadjangba/check-metadata-sample-csv/check_metadata_sample.csv"),
    Path("/kaggle/input/check_metadata_sample.csv/check_metadata_sample.csv"),
]

def score_check(row: pd.Series) -> dict:
    score = 0.0
    reasons = []

    if float(row.get("material_score", 1.0)) < 0.70:
        score += 0.30
        reasons.append("Material score is below the expected threshold.")

    if int(row.get("sequence_gap_flag", 0)) == 1:
        score += 0.20
        reasons.append("Check number appears out of expected sequence.")

    if int(row.get("routing_number_valid", 1)) == 0:
        score += 0.20
        reasons.append("Routing number validation failed.")

    if int(row.get("micr_match", 1)) == 0:
        score += 0.15
        reasons.append("MICR inconsistency detected.")

    if int(row.get("duplicate_check_flag", 0)) == 1:
        score += 0.25
        reasons.append("Duplicate check pattern detected.")

    if float(row.get("geo_risk_score", 0.0)) > 0.50:
        score += 0.10
        reasons.append("Payer geography appears outside normal expectations.")

    if int(row.get("prior_return_count", 0)) > 0:
        score += 0.10
        reasons.append("Prior returned-check history increases concern.")

    score = min(score, 1.0)

    if score >= 0.70:
        recommendation = "Escalate for review"
        risk_level = "High Risk"
    elif score >= 0.40:
        recommendation = "Use caution"
        risk_level = "Medium Risk"
    else:
        recommendation = "Low immediate risk"
        risk_level = "Low Risk"

    return {
        "risk_score": round(score, 2),
        "risk_level": risk_level,
        "recommendation": recommendation,
        "reasons": reasons,
    }

def load_default_dataset() -> pd.DataFrame | None:
    for path in DEFAULT_DATA_PATHS:
        if path.exists():
            return pd.read_csv(path)
    return None

def score_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    scored_rows = []
    for _, row in df.iterrows():
        result = score_check(row)
        enriched = row.to_dict()
        enriched["risk_score"] = result["risk_score"]
        enriched["risk_level"] = result["risk_level"]
        enriched["recommendation"] = result["recommendation"]
        enriched["reasons"] = " | ".join(result["reasons"]) if result["reasons"] else "No major discrepancy detected."
        scored_rows.append(enriched)
    return pd.DataFrame(scored_rows)

def manual_input_to_row(
    transaction_type: str,
    discrepancy_type: str,
    branch_type: str,
    country: str,
    check_number: int,
    amount: float,
    material_score: float,
    routing_number_valid: bool,
    micr_match: bool,
    duplicate_check_flag: bool,
    geo_risk_score: float,
    prior_return_count: int,
):
    sequence_gap_flag = 1 if discrepancy_type == "Check Number" else 0
    routing_flag = 0 if discrepancy_type == "Routing Number" else int(routing_number_valid)
    geography_score = max(geo_risk_score, 0.65) if discrepancy_type == "Payer Geography" else geo_risk_score

    return pd.Series({
        "check_id": "MANUAL_REVIEW",
        "payer_id": "TELLER_INPUT",
        "payer_bank": branch_type,
        "payer_state": country,
        "check_number": check_number,
        "amount": amount,
        "material_score": material_score,
        "sequence_gap_flag": sequence_gap_flag,
        "routing_number_valid": routing_flag,
        "micr_match": int(micr_match),
        "duplicate_check_flag": int(duplicate_check_flag),
        "geo_risk_score": geography_score,
        "prior_return_count": prior_return_count,
        "transaction_type": transaction_type,
    })

st.sidebar.title("Check Detect")
st.sidebar.caption("User-friendly teller support for suspicious check review")

transaction_type = st.sidebar.selectbox(
    "Transaction type inquiry",
    TRANSACTION_TYPES,
    help="Select the teller transaction being reviewed."
)

discrepancy_type = st.sidebar.selectbox(
    "Discrepancy type inquiry",
    DISCREPANCY_TYPES,
    help="Select the primary discrepancy the teller noticed."
)

branch_type = st.sidebar.selectbox(
    "Branch inquiry",
    BRANCH_OPTIONS,
    help="Start typing to search branch type or call center options."
)

country = st.sidebar.selectbox(
    "Country type inquiry",
    COUNTRY_OPTIONS,
    help="Start typing to search countries."
)

st.sidebar.markdown("---")
uploaded_file = st.sidebar.file_uploader(
    "Upload transaction/check dataset (CSV)",
    type=["csv"],
    help="Upload a CSV to score multiple checks at once."
)

st.title("🏦 Check Detect Dashboard")
st.write(
    "Check Detect is an AI-assisted decision-support tool designed for non-technical bank tellers. "
    "It highlights suspicious check indicators, gives a risk score, and suggests whether the check "
    "should be handled normally, with caution, or escalated for review."
)

tab1, tab2, tab3 = st.tabs(["Teller Review", "Dashboard", "About Check Detect"])

with tab1:
    st.subheader("Single Transaction Review")
    st.caption("Enter or adjust values below to review one transaction in real time.")

    col1, col2, col3 = st.columns(3)
    with col1:
        check_number = st.number_input("Check number", min_value=1, value=1001, step=1)
        amount = st.number_input("Check amount ($)", min_value=0.0, value=500.0, step=25.0)
        material_score = st.slider("Check material score", 0.0, 1.0, 0.85, 0.01)

    with col2:
        routing_number_valid = st.toggle("Routing number valid", value=True)
        micr_match = st.toggle("MICR match", value=True)
        duplicate_check_flag = st.toggle("Duplicate check pattern", value=False)

    with col3:
        geo_risk_score = st.slider("Payer geography risk score", 0.0, 1.0, 0.20, 0.01)
        prior_return_count = st.number_input("Prior returned checks", min_value=0, value=0, step=1)

    if st.button("Run Check Detect Review", use_container_width=True):
        manual_row = manual_input_to_row(
            transaction_type=transaction_type,
            discrepancy_type=discrepancy_type,
            branch_type=branch_type,
            country=country,
            check_number=int(check_number),
            amount=float(amount),
            material_score=float(material_score),
            routing_number_valid=bool(routing_number_valid),
            micr_match=bool(micr_match),
            duplicate_check_flag=bool(duplicate_check_flag),
            geo_risk_score=float(geo_risk_score),
            prior_return_count=int(prior_return_count),
        )

        result = score_check(manual_row)

        m1, m2, m3 = st.columns(3)
        m1.metric("Risk Score", result["risk_score"])
        m2.metric("Risk Level", result["risk_level"])
        m3.metric("Recommendation", result["recommendation"])

        st.markdown("### Teller-Friendly Explanation")
        if result["reasons"]:
            for reason in result["reasons"]:
                st.write(f"- {reason}")
        else:
            st.success("No major discrepancy detected.")

        st.info(
            f"Transaction Type: {transaction_type} | "
            f"Discrepancy Type: {discrepancy_type} | "
            f"Branch Inquiry: {branch_type} | "
            f"Country Inquiry: {country}"
        )

        st.warning(
            "Check Detect does not make the final transaction decision. "
            "It acts as a second set of eyes and supports teller judgment."
        )

with tab2:
    st.subheader("Portfolio / Batch Review Dashboard")
    st.caption("Use this section to review many checks at once from a CSV upload or the default sample dataset.")

    if uploaded_file is not None:
        base_df = pd.read_csv(uploaded_file)
        st.success("Uploaded dataset loaded successfully.")
    else:
        base_df = load_default_dataset()
        if base_df is not None:
            st.info("Using the default sample dataset.")
        else:
            base_df = None
            st.error("No dataset found. Upload a CSV in the sidebar to continue.")

    if base_df is not None:
        scored_df = score_dataframe(base_df)

        total_checks = len(scored_df)
        high_risk = int((scored_df["risk_level"] == "High Risk").sum())
        medium_risk = int((scored_df["risk_level"] == "Medium Risk").sum())
        low_risk = int((scored_df["risk_level"] == "Low Risk").sum())

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Total Checks", total_checks)
        k2.metric("High Risk", high_risk)
        k3.metric("Medium Risk", medium_risk)
        k4.metric("Low Risk", low_risk)

        chart_col, table_col = st.columns([1, 2])

        with chart_col:
            st.markdown("### Risk Distribution")
            risk_counts = scored_df["risk_level"].value_counts()
            st.bar_chart(risk_counts)

        with table_col:
            st.markdown("### Scored Check Results")
            display_cols = [c for c in [
                "check_id", "payer_bank", "payer_state", "check_number", "amount",
                "risk_score", "risk_level", "recommendation", "reasons"
            ] if c in scored_df.columns]
            st.dataframe(scored_df[display_cols], use_container_width=True)

        st.markdown("### Filters")
        f1, f2 = st.columns(2)
        with f1:
            selected_risk = st.multiselect(
                "Filter by risk level",
                options=sorted(scored_df["risk_level"].unique().tolist()),
                default=sorted(scored_df["risk_level"].unique().tolist())
            )
        with f2:
            min_score = st.slider("Minimum risk score", 0.0, 1.0, 0.0, 0.01)

        filtered_df = scored_df[
            scored_df["risk_level"].isin(selected_risk) &
            (scored_df["risk_score"] >= min_score)
        ]

        st.markdown("### Filtered Results")
        st.dataframe(filtered_df[display_cols], use_container_width=True)

        csv = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Filtered Results",
            data=csv,
            file_name="check_detect_scored_results.csv",
            mime="text/csv",
            use_container_width=True,
        )

with tab3:
    st.subheader("About Check Detect")
    st.write(
        "Check Detect uses a hybrid AI decision-support framework. It combines rule-based fraud scoring, "
        "structured transaction review, and machine learning concepts to help identify suspicious checks."
    )

    st.markdown("### What the app reviews")
    st.write("- Check material consistency")
    st.write("- Check number sequencing")
    st.write("- Routing and MICR issues")
    st.write("- Duplicate check behavior")
    st.write("- Payer geography as a contextual signal")
    st.write("- Prior returned-check history")

    st.markdown("### Built for usability")
    st.write(
        "The interface is designed for non-technical bank tellers. It uses a guided sidebar, simple dropdowns, "
        "clear metrics, teller-friendly explanations, and dashboard summaries."
    )

    st.markdown("### Important note")
    st.warning(
        "Check Detect does not automatically approve or deny a check. "
        "It is a second set of eyes and keeps the final decision with the teller."
    )
