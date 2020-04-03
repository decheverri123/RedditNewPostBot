import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import local_settings


def send_email(id, title, link):
    port = 465
    context = ssl.create_default_context()

    sender_email = (local_settings.sender_email)
    receiver_email = local_settings.receiver_email

    message = MIMEMultipart("alternative")
    message["Subject"] = title
    message["From"] = sender_email
    message["To"] = receiver_email

    part1 = MIMEText(link, "plain")
    message.attach(part1)

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(local_settings.sender_email,
                     local_settings.email_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
