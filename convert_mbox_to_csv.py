import mailbox
import pandas as pd

files = [
    "phishing_2025",
    "phishing_2024",
    "phishing_2023",
    "phishing_2022"
]

emails = []

for file in files:
    mbox = mailbox.mbox(file)

    for message in mbox:
        subject = message['subject']
        body = ""

        if message.is_multipart():
            for part in message.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True)
                    if body:
                        body = body.decode(errors="ignore")
        else:
            body = message.get_payload(decode=True)
            if body:
                body = body.decode(errors="ignore")

        text = str(subject) + " " + str(body)

        emails.append({
            "text": text,
            "label": 1
        })

df = pd.DataFrame(emails)
df.to_csv("phishing_dataset.csv", index=False)

print("Dataset created successfully")