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


def has_paypal(title):
    start = title.find("[H]")
    end = title.find("[W]")
    target = title[start:end].lower()

    if "paypal" in target or "cash" in target:
        return True

    return False


def process_hardwareswap_submission(sub, submission, link):
    """if a submission from hardwareswap has paypal/cash in [H],ignore it else,
        send notificaiton
    Arguments:
        sub {} -- subreddit
        submission {submission} -- submission
        link {link} -- full link to submission
    """
    if has_paypal(submission.title):
        print("Has Paypal/Cash, ignoring. {0}\n".format(submission.title))

    else:
        send_email(submission.id, submission.title, link)
        print("New notification from {0}. {1} \n{2}\n".format(
            sub, submission.title, link))


def process_submission(sub, submission, link):
    send_email(submission.id, submission.title, link)
    print("New notification from {0}. {1} \n{2}\n".format(
        sub, submission.title, link))
