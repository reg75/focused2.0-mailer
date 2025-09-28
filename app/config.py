import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MAILER_API_KEY = os.getenv("MAILER_API_KEY", "")
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")
    MAILER_FROM_EMAIL = os.getenv("MAILER_FROM_EMAIL")
    LOG_LEVEL = os.getenv("LOG_LEVEL")

settings = Settings()