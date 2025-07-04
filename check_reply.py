import imaplib, email
from datetime import datetime

def has_replied(lead_email, since_date, gmail_user, gmail_pass):
    since_str = since_date.strftime("%d-%b-%Y")

    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(gmail_user, gmail_pass)
    mail.select('"[Gmail]/All Mail"')

    # Search for replies FROM lead TO your address AFTER the send date
    result, data = mail.search(
        None,
        f'(FROM "{lead_email}" SINCE "{since_str}")'
    )

    mail.logout()
    return bool(data[0].split())
