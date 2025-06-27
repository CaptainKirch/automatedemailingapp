from datetime import datetime
import random
from utils import send_email, load_csv, save_csv
from templates import TEMPLATES
from config import MAX_EMAILS_PER_DAY

today = datetime.today().date()
leads = load_csv("leads.csv")
log = load_csv("email_log.csv")
log_dict = {entry['Email']: entry for entry in log}
sent_today = 0

for lead in leads:
    email = lead['Email']
    record = log_dict.get(email)
    
    if record:
        stage = int(record['Stage'])
        last_sent = datetime.strptime(record['LastSent'], "%Y-%m-%d").date()
        days_since = (today - last_sent).days

        if stage < 3 and days_since >= [0, 3, 4][stage]:
            msg = random.choice(TEMPLATES[stage + 1]).format(**lead)
            send_email(email, f"Cleaning for {lead['Business']}", msg)
            record['Stage'] = str(stage + 1)
            record['LastSent'] = today.isoformat()
            sent_today += 1
    else:
        msg = random.choice(TEMPLATES[1]).format(**lead)
        send_email(email, f"Cleaning for {lead['Business']}", msg)
        log_dict[email] = {
            "Email": email,
            "Stage": "1",
            "LastSent": today.isoformat()
        }
        sent_today += 1

    if sent_today >= MAX_EMAILS_PER_DAY:
        break

save_csv("email_log.csv", list(log_dict.values()), fieldnames=["Email", "Stage", "LastSent"])
print(f"✅ Sent {sent_today} emails today.")
