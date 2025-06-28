from datetime import datetime, timezone
import random
from utils import send_email, load_csv, save_csv
from templates import TEMPLATES
from config import MAX_EMAILS_PER_DAY, FROM_EMAIL, APP_PASSWORD, SIGNATURE
from check_reply import has_replied
from config import MAX_EMAILS_PER_RUN

SUBJECTS = {
    1: "Quick question",
    2: "Thoughts?",
    3: "I'll stop bugging you now."
}

now = datetime.now(timezone.utc)
print(f"🕒 Current UTC hour: {now.hour}") # added UTC hour print debug

if not (15 <= now.hour < 18):  # 8am–10am PT in UTC
    print("⏸️ Current time outside sending window. Exiting.")
    exit()

today = datetime.today().date()
leads = load_csv("leads.csv")
log = load_csv("email_log.csv")
log_dict = {entry['Email']: entry for entry in log}
sent_today = 0

for lead in leads:
    email = lead['Email']
    record = log_dict.get(email)

    try:
        if record:
            stage = int(record['Stage'])
            last_sent = datetime.strptime(record['LastSent'], "%Y-%m-%d").date()
            days_since = (today - last_sent).days

            try:
                if has_replied(email, last_sent, FROM_EMAIL, APP_PASSWORD):
                    print(f"⏸️ Skipping {email} — replied already.")
                    continue
            except Exception as e:
                print(f"⚠️ Reply check failed for {email}: {e}")
                continue

            if stage < 3 and days_since >= [0, 3, 4][stage]:
                try:
                    msg = random.choice(TEMPLATES[stage + 1]).format(**lead) + "\n\n" + SIGNATURE
                    subject = SUBJECTS[stage + 1]
                    send_email(email, subject, msg)
                    record['Stage'] = str(stage + 1)
                    record['LastSent'] = today.isoformat()
                    sent_today += 1
                except Exception as e:
                    print(f"❌ Failed to send stage {stage + 1} email to {email}: {e}")
        else:
            try:
                subject = SUBJECTS[1]
                msg = random.choice(TEMPLATES[1]).format(**lead) + "\n\n" + SIGNATURE
                send_email(email, subject, msg)
                log_dict[email] = {
                    "Email": email,
                    "Stage": "1",
                    "LastSent": today.isoformat()
                }
                sent_today += 1
            except Exception as e:
                print(f"❌ Failed to send initial email to {email}: {e}")

        if sent_today >= MAX_EMAILS_PER_RUN:
            break

    except Exception as e:
        print(f"⚠️ General failure processing lead {email}: {e}")

save_csv("email_log.csv", list(log_dict.values()), fieldnames=["Email", "Stage", "LastSent"])
print(f"✅ Sent {sent_today} emails today.")
