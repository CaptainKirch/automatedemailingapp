import csv
from email.message import EmailMessage
import smtplib
from config import FROM_EMAIL, APP_PASSWORD, SMTP_SERVER, SMTP_PORT

def send_email(to_email, subject, body):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = FROM_EMAIL
    msg['To'] = to_email
    msg.set_content(body)

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(FROM_EMAIL, APP_PASSWORD)
        server.send_message(msg)

def load_csv(filename):
    try:
        with open(filename) as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        return []

def save_csv(filename, data, fieldnames):
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
