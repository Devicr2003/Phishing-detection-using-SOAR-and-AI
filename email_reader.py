from plyer import notification
from email.header import decode_header
import imaplib
import email
import pickle
import requests

EMAIL = "xxxx@gmail.com"
PASSWORD = "xxxxxxxxxxxxxxxxxx"

# Load AI model
model = pickle.load(open("phishing_model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# Connect to Gmail
mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(EMAIL, PASSWORD)
mail.select("inbox")

status, messages = mail.search(None, "ALL")
mail_ids = messages[0].split()
latest_email_id = mail_ids[-1]
status, msg_data = mail.fetch(latest_email_id, "(RFC822)")

raw_email = msg_data[0][1]
msg = email.message_from_bytes(raw_email)

subject, encoding = decode_header(msg["subject"])[0]
if isinstance(subject, bytes):
    subject = subject.decode(encoding if encoding else "utf-8")

body = ""
if msg.is_multipart():
    for part in msg.walk():
        if part.get_content_type() == "text/plain":
            body = part.get_payload(decode=True).decode(errors="ignore")
            break
else:
    body = msg.get_payload(decode=True).decode(errors="ignore")

sender = msg.get("from")

print("Subject:", subject)
print("Body:", body)
print("Sender:", sender)

# Send email to AI HTTP endpoint
API_URL = "http://127.0.0.1:5000/scan"  # or ngrok URL
payload = {
    "subject": subject,
    "body": body,
    "email": sender
}

try:
    response = requests.post(API_URL, json=payload)
    response.raise_for_status()  # check HTTP errors

    try:
        result = response.json()
    except requests.JSONDecodeError:
        print("Error: AI endpoint returned invalid JSON")
        print(response.text)
        result = {"status": "unknown"}

except requests.exceptions.RequestException as e:
    print("Request error:", e)
    result = {"status": "unknown"}

# Send to Shuffle webhook
WEBHOOK_URL = "https://shuffler.io/api/v1/hooks/webhook_e8a35051-ba95-4d1d-9517-18b9c3b710db"
webhook_data = {
    "type": result.get("status", ""),
    "email": sender,
    "subject": subject,
    "message": body,
    "confidence": result.get("confidence", "high")
}
requests.post(WEBHOOK_URL, json=webhook_data)

# Phishing alert
if "phishing" in result.get("status", "").lower():
    print("⚠️ PHISHING EMAIL DETECTED")
    try:
        notification.notify(
            title="Phishing Alert 🚨",
            message=f"Suspicious email detected from {sender}",
            timeout=5
        )
        print("Popup sent")
    except Exception as e:
        print("Popup error:", e)

    # Move email to Quarantine
    try:
        mail.copy(latest_email_id, "Quarantine")
        mail.store(latest_email_id, '+FLAGS', '\\Deleted')
        mail.expunge()
    except Exception as e:
        print("Quarantine error:", e)

else:
    print("✅ SAFE EMAIL")