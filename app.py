from flask import Flask, request, jsonify

app = Flask(__name__)

# Example AI model function (replace with your real AI logic)
def predict_email(email_subject, email_body, sender):
    """
    Fake AI model: detects phishing emails
    Replace this with your real AI model logic
    """
    phishing_keywords = ["urgent", "password", "bank", "click", "verify"]
    combined_text = (email_subject + " " + email_body).lower()
    for word in phishing_keywords:
        if word in combined_text:
            return "phishing", "high"
    return "legitimate", "low"

@app.route("/scan", methods=["POST"])
def scan_email():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400

        email_subject = data.get("subject", "")
        email_body = data.get("body", "")
        email_sender = data.get("email", "")

        status, confidence = predict_email(email_subject, email_body, email_sender)

        return jsonify({
            "status": status,
            "confidence": confidence,
            "subject": email_subject,
            "email": email_sender
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000)