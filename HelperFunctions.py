from email.mime.text import MIMEText
import praw
from praw import reddit
from email.mime.multipart import MIMEMultipart
import smtplib
import ssl
import local_settings

def getNewPosts(subreddit):

    reddit = praw.Reddit(client_id=local_settings.client_id,
                     client_secret=local_settings.client_secret,
                     password=local_settings.password,
                     username="decheverri123",
                     user_agent="test script")

    currPost = []

    for submission in reddit.subreddit(subreddit).new(limit=1):
        link = "https://reddit.com{0}".format(submission.permalink)
        if not currPost or currPost.pop()[0] != submission.id:
            currPost.pop() if currPost else None
            currPost.append([submission.id, submission.title, link])
        else:
            return None
    
    return currPost
        
def sendEmail(id, title, link):

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
        server.login(local_settings.sender_email, local_settings.email_password)
        server.sendmail(sender_email, receiver_email, message.as_string())