# System Design

## Teller Workflow
1. Teller receives a check that appears questionable
2. Teller scans or enters check-related details
3. Check Detect evaluates metadata and visual indicators
4. System returns a risk score, recommendation, and flagged reasons
5. Teller decides whether to proceed, hold, or escalate

## Prototype Components
- Synthetic data store
- Feature engineering pipeline
- Rule-based scorer
- Baseline classifier
- Lightweight Flask demo app
