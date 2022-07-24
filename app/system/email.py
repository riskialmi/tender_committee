import smtplib
import ssl
import email
from email import encoders
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.system.config import SMTP_SERVER, EMAIL_PORT, EMAIL_PASSWORD, SENDER_EMAIL
import base64

def send_email(to: [], subject: str, message: str, attach_bytes: [bytes], file_name: [str]):
    context = ssl.create_default_context()
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = ", ".join(to)

    part = MIMEText(message, "html")
    msg.attach(part)

    if attach_bytes:
        for (attach, name) in zip(attach_bytes, file_name):
            part = MIMEApplication(
                    _data=base64.b64decode(attach),
                    _subtype="docx")
            part.add_header('Content-Disposition', 'attachment', filename=name)
            msg.attach(part)

    try:
        server = smtplib.SMTP(SMTP_SERVER, EMAIL_PORT)
        server.starttls(context=context)
        server.login(SENDER_EMAIL, EMAIL_PASSWORD)
        server.sendmail(SENDER_EMAIL, to, msg.as_string())
    except Exception as e:
        print("Error Email: ", e)
    finally:
        server.quit()
