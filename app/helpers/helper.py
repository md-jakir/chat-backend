from fastapi import Request, HTTPException
from starlette.responses import JSONResponse
import secrets
import string
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
# import random

async def http_error_handler(request: Request, exc: HTTPException):
    print(exc)
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": str(exc.detail)},
    )

def custom_response_handler(status_code: int, message: str, data=None):
    if data is None:
        return {
            "status_code": status_code,
            "message": message,
        }
    else:
        return {
            "status_code": status_code,
            "message": message,
            "data": data,
        }

def generate_otp(length=6):
    return ''.join(secrets.choice(string.digits) for _ in range(length))

def send_email(recipient_email, subject, body):
    SENDER_EMAIL = os.getenv("SENDER_EMAIL")
    SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
    EMAIL_HOST = os.getenv("EMAIL_HOST")
    EMAIL_PORT = os.getenv("EMAIL_PORT")

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email
    msg['Subject'] = subject
  
    msg.attach(MIMEText(body, 'html'))

    server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    text = msg.as_string()
    server.sendmail(SENDER_EMAIL, recipient_email, text)
    server.quit()


def generate_random_password():
    # password = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(8))
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(8))

    