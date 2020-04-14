import smtplib
import ssl
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import praw

import local_settings

seen_posts = local_settings.seen_posts
sender_email = local_settings.sender_email
receiver_email = local_settings.receiver_email
email_password = local_settings.email_password


def setup_reddit_api():
    reddit = praw.Reddit(client_id=local_settings.client_id,
                         client_secret=local_settings.client_secret,
                         password=local_settings.password,
                         username="decheverri123",
                         user_agent="test script")
    return reddit


def get_new_posts(sub):
    reddit = setup_reddit_api()

    for submission in reddit.subreddit(sub).new(limit=1):

        if not seen_posts or submission.id not in seen_posts:
            if has_keyword(submission.title):
                process_submission(sub, submission)
                seen_posts.append(submission.id)

            else:
                print("No keyword. {0}".format(submission.title))

                link = "https://reddit.com{0}".format(submission.permalink)
                print(str(link)+"\n")

                seen_posts.append(submission.id)


def process_submission(sub, submission):
    link = "https://reddit.com{0}".format(submission.permalink)

    email = create_email(submission.title, link)
    send_email(email)

    time_created = unix_to_dt(submission.created_utc)
    print("{3} New notification from {0}. {1} \n{2}\n".format(
        sub, submission.title, link, time_created))


def create_email(title, link):
    """Creates message to be sent

    Arguments:
        title {str} -- title of submission
        link {str} -- link of submission

    Returns:
        message -- email message that will be sent
    """
    email = MIMEMultipart("alternative")
    email["Subject"] = title
    email["From"] = sender_email
    email["To"] = receiver_email
    part1 = MIMEText(link, "plain")
    email.attach(part1)

    return email


def send_email(message):
    """Initializes SMTP server and sends email message

    Arguments:
        message {MIME message} -- message to be sent
    """
    port = 465
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, email_password)
        server.sendmail(sender_email, receiver_email, message.as_string())


def has_keyword(title):
    """checks to see if the title mentions certain words, in this case, switch
    and 2080

    Arguments:
        title {str} -- submission title

    Returns:
        bool
    """
    # start = title.find("[H]")
    # end = title.find("[W]")
    # target = title[start:end].lower()
    keywords = ["switch", "pc", "steam", "eshop"]
    lowercase_title = title.lower()

    for keyword in keywords:
        if keyword in lowercase_title:
            return True
    return False


def unix_to_dt(utc_time):
    dt_time = datetime.fromtimestamp(utc_time)
    return dt_time
