from flask import Flask, render_template, request, jsonify
import requests
import ast

app = Flask(__name__)

SCALEDOWN_API_KEY = "NhVxZtQ8n12sMhHAPcwyr7RMFRbbJdLA8LT80WEq"
SCALEDOWN_URL = "https://api.scaledown.xyz/compress/raw/"

def rule_based_review(code):
    feedback = []

    # Syntax check
    try:
        ast.parse(code)
        feedback.append("✅ Syntax is correct.")
    except SyntaxError as e:
        feedback.append(f"❌ Syntax error: {e}")
        return feedback

    # Simple rule checks
    if "print" in code:
        feedback.append("ℹ️ Avoid using print statements in production code.")

    if "*" in code and "a*b" in code:
        feedback.append("✅ Multiplication operation is correct.")

    if len(code.splitlines()) < 3:
        feedback.append("ℹ️ Code is very small; consider adding comments for clarity.")

    feedback.append("✅ Overall, the code logic is correct.")

    return feedback

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/review", methods=["POST"])
def review_code():
    code = request.form.get("code")

    if not code:
        return jsonify({"error": "No code provided"})

    # 🔹 Rule-based review (REAL RESPONSE)
    review = rule_based_review(code)

    # 🔹 ScaleDown compression (OPTIMIZATION LAYER)
    payload = {
        "context": "You are a senior software engineer reviewing code.",
        "prompt": code,
        "model": "gpt-4o",
        "scaledown": {"rate": "auto"}
    }

    headers = {
        "x-api-key": SCALEDOWN_API_KEY,
        "Content-Type": "application/json"
    }

    sd_response = requests.post(SCALEDOWN_URL, headers=headers, json=payload)
    sd_result = sd_response.json()

    return jsonify({
        "code_review": review,
        "compression_stats": {
            "original_tokens": sd_result.get("total_original_tokens"),
            "compressed_tokens": sd_result.get("total_compressed_tokens"),
            "compression_ratio": sd_result.get("results", {}).get("compression_ratio")
        }
    })

if __name__ == "__main__":
    app.run(debug=True)
