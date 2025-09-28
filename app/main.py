from dotenv import load_dotenv
from pathlib import Path


# Load ../.env relative to this file
ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)

# (optional but helpful) basic logging
import logging, os
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logging.info("[startup] .env path: %s  exists=%s", ENV_PATH, ENV_PATH.exists())
logging.info("[startup] MAILER_API_KEY len=%d", len(os.getenv("MAILER_API_KEY", "")))


from typing import Any

from fastapi import FastAPI, BackgroundTasks, HTTPException, Request, Security
from fastapi.security import APIKeyHeader
from .schemas import ObservationEmailIn, EmailStatusOut, EmailStatus
from .config import settings
from .pdf import build_observation_html, render_pdf_bytes
from .emailer import send_observation_email
from .security import verify_api_key

import os
print("[env] SENDGRID_API_KEY set? ", bool(os.getenv("SENDGRID_API_KEY")))
print("[env] MAILER_FROM_EMAIL=", os.getenv("MAILER_FROM_EMAIL"))
print("[env] MAILER_API_KEY set? ", bool(os.getenv("MAILER_API_KEY")))
print("[env] MAILER_API_KEY prefix:", (os.getenv("MAILER_API_KEY","")[:4] + "…"))


app = FastAPI()
app = FastAPI(
    title="FocusEd Mailer",
    version="0.1.0",
    swagger_ui_parameters={"persistAuthorization": True},  # remembers key between calls
)

@app.post("/mail/observation", response_model=EmailStatusOut)
def mail_observation(
    payload: ObservationEmailIn,
    request: Request,
    bg: BackgroundTasks,
    api_key: str = Security(verify_api_key)):
    

    if not settings.SENDGRID_API_KEY or not settings.MAILER_FROM_EMAIL:
        return {"email_status": EmailStatus.failed.value}  # ensure string value

    
    def worker(d: dict):
            html = build_observation_html(d)
            pdf = render_pdf_bytes(html)
            subject = f"Observation feedback — {d.get('teacher_name')} — {d.get('obs_date')}"
            status = send_observation_email(
                d["to_email"],
                subject,
                "Please find attached the feedback on your recent observation",
                pdf
             )
            
            # Outcome logging
            if status == 202:
                print({"evt": "mail_status", "status": "sent", "to": d["to_email"]})
            else:
                print({"evt": "mail_status", "status": "failed", "to": d["to_email"], "code": status})

    bg.add_task(worker, payload.model_dump())
    return {"email_status": EmailStatus.queued}
