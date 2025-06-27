from dotenv import load_dotenv
import os

load_dotenv()

FROM_EMAIL = os.getenv("FROM_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
MAX_EMAILS_PER_DAY = int(os.getenv("MAX_EMAILS_PER_DAY", "15"))