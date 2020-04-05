import smtplib
import ssl
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import praw

import local_settings

seen_posts = local_settings.seen_posts


def get_new_posts(sub):
    reddit = setup_reddit_api()

    for submission in reddit.subreddit(sub).new(limit=1):

        if not seen_posts or submission.id not in seen_posts:
            # if sub == "hardwareswap":
            #     process_hardwareswap_submission(sub, submission)
            #     seen_posts.append(submission.id)

            # else:
            #     process_submission(sub, submission)
            #     seen_posts.append(submission.id)
            link = "https://reddit.com{0}".format(submission.permalink)

            start = submission.title.find("[H]")
            end = submission.title.find("[W]")
            target = submission.title[start:end].lower()

            if "switch" in target:
                process_submission(sub, submission)
                seen_posts.append(submission.id)
            elif sub != "hardwareswap":
                process_submission(sub, submission)
                seen_posts.append(submission.id)
            else:
                print("Not Switch. {0}".format(submission.title))
                print(str(link)+"\n")
                seen_posts.append(submission.id)


def process_hardwareswap_submission(sub, submission):
    """ if a submission from hardwareswap has paypal/cash in [H],ignore it else,
        send notificaiton
    Arguments:
        sub {} -- subreddit
        submission {submission} -- submission
        link {link} -- full link to submission
    """

    link = "https://reddit.com{0}".format(submission.permalink)

    if has_paypal(submission.title):
        print("Has Paypal/Cash, ignoring. {0}".format(submission.title))
        print(str(link)+"\n")

    else:
        send_email(submission.title, link)
        print("New notification from {0}. {1} \n{2}\n".format(
            sub, submission.title, link))


def process_submission(sub, submission):

    link = "https://reddit.com{0}".format(submission.permalink)

    send_email(submission.title, link)

    time_created = unix_to_dt(submission.created_utc)
    print("{3} New notification from {0}. {1} \n{2}\n".format(
        sub, submission.title, link, time_created))


def unix_to_dt(utc_time):
    dt_time = datetime.fromtimestamp(utc_time)
    return dt_time


def setup_email(title, link):

    sender_email = local_settings.sender_email
    receiver_email = local_settings.receiver_email

    message = MIMEMultipart("alternative")
    message["Subject"] = title
    message["From"] = sender_email
    message["To"] = receiver_email

    part1 = MIMEText(link, "plain")
    message.attach(part1)

    return sender_email, receiver_email, message


def send_email(title, link):
    sender_email, receiver_email, message = setup_email(title, link)

    port = 465
    context = ssl.create_default_context()

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


def setup_reddit_api():
    reddit = praw.Reddit(client_id=local_settings.client_id,
                         client_secret=local_settings.client_secret,
                         password=local_settings.password,
                         username="decheverri123",
                         user_agent="test script")
    return reddit
