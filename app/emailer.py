import base64, os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content, Attachment, FileContent, FileName, FileType, Disposition
from .config import settings

def send_observation_email(to_email: str, subject: str, html_body: str, pdf_bytes: bytes) -> int:
    """
    EN: Sends an email using SendGrid.
    BR: Envia um e-mail usando SendGrid.
    """
   
    mail = Mail(
      from_email=Email(settings.MAILER_FROM_EMAIL),
    to_emails=To(to_email),
    subject=subject,
    html_content=Content("text/html", html_body),
    )
   
    b64 = base64.b64encode(pdf_bytes).decode("ascii")
    att = Attachment(
      FileContent(b64),
      FileName("observationfeedback.pdf"),
      FileType("application/pdf"),
      Disposition("attachment")
   )

    mail.add_attachment(att)
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.client.mail.send.post(request_body=mail.get())
        return response.status_code
    except Exception as e:
        print(f"sendgrid_error: {e}")
        return 500