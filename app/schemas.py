from enum import Enum
from pydantic import BaseModel, EmailStr
from typing import Optional

class EmailStatus(str, Enum):
    queued = "queued"
    sent = "sent" # Reserved for later use - not used in MVP
    failed = "failed"

class ObservationEmailIn(BaseModel):

    to_email: EmailStr
    teacher_name: str
    obs_date: str
    department_name: Optional[str] = None
    class_name: Optional[str] = None
    focus_area: Optional[str] = None
    strengths: Optional[str] = None
    weaknesses: Optional[str] = None
    comments: Optional[str] = None

class EmailStatusOut(BaseModel):
    email_status: EmailStatus