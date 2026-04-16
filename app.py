from flask import Flask, jsonify
from src.ingest import load_synthetic_dataset
from src.scorer import score_check

app = Flask(__name__)

@app.route("/")
def home():
    return {
        "project": "Check Detect",
        "message": "AI-assisted suspicious check review tool for teller decision support."
    }

@app.route("/demo-score")
def demo_score():
    df = load_synthetic_dataset()
    row = df.iloc[1]
    result = score_check(row)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
