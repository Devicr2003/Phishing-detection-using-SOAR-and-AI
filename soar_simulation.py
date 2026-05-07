import datetime

def alert(email):
    print("🚨 ALERT: Phishing email detected!")
    print("Email content:", email)

def quarantine(email):

    with open("quarantine/quarantined_emails.txt", "a") as f:
        f.write(email + "\n")

    print("📁 Email moved to quarantine.")

def log_incident(email):

    time = datetime.datetime.now()

    with open("logs.txt", "a") as log:
        log.write(f"{time} - Phishing detected: {email}\n")

    print("📝 Incident logged.")

def soar_response(email):

    alert(email)
    quarantine(email)
    log_incident(email)