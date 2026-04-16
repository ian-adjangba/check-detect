# Dataset Plan for Check Detect

## Objective
Develop a prototype dataset to support an AI-assisted system for suspicious check detection in a teller environment.

## Dataset Components

### 1. Synthetic Metadata Dataset
A tabular dataset representing check transactions and fraud-related indicators.

#### Example fields
- check_id
- payer_id
- payer_bank
- payer_state
- check_number
- amount
- material_score
- sequence_gap_flag
- routing_number_valid
- micr_match
- duplicate_check_flag
- geo_risk_score
- prior_return_count
- fraud_label

### 2. Image Feature Dataset
Derived visual features from mock or sample check images.

#### Example fields
- paper_texture_similarity
- watermark_detected
- print_alignment_score
- ink_uniformity_score
- tamper_region_score
- logo_match_score

### 3. Labeling Strategy
Labels will be assigned using simulated scenarios:
- Legitimate
- Suspicious
- Fraudulent

## Data Creation Method
Because real check data is highly sensitive, the initial dataset will be generated synthetically using realistic banking scenarios and fraud patterns. This will allow model development without exposing customer financial data.

## Potential Fraud Patterns Simulated
- Non-sequential check numbers
- Repeated check numbers
- Amounts inconsistent with prior check behavior
- Invalid routing/MICR combinations
- Material inconsistency
- Missing watermark or security features
- Out-of-region payer anomalies
- Prior returned-check history

## Limitations
Synthetic data cannot fully replicate real banking fraud patterns. The prototype is intended for proof-of-concept use only and would require secure access to real institutional data for production deployment.

## Compliance Considerations
- No real customer PII will be used
- No bank account numbers will be stored in raw form
- Model outputs should remain advisory
- Human review remains required
