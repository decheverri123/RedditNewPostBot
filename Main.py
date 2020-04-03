# hook up reddit api
# constantly crawl chosen subreddits
# when a new post is created, send an email to 8644514161@txt.att.net
# (this will send a text to me)
# subject should be [H], message should have [W]
# link to post should be included
# have all this run on the cloud

# nice to haves
# exlude messages that where [H] is paypal

import sys
import time

from helper_functions import send_email
import praw
import local_settings


if __name__ == "__main__":

    subreddits = ["GameDeals", "buildapcsales", "hardwareswap", "consoledeals"]

    reddit = praw.Reddit(client_id=local_settings.client_id,
                         client_secret=local_settings.client_secret,
                         password=local_settings.password,
                         username="decheverri123",
                         user_agent="test script")

    seen_posts = []
    first = True

    def check_new_posts(sub):
        for submission in reddit.subreddit(sub).new(limit=1):

            link = "https://reddit.com{0}".format(submission.permalink)

            if first is True:
                print("New notification from {0}. {1} \n{2}\n".format(
                    sub, submission.title, link))
                seen_posts.append(submission.id)
                send_email(submission.id, submission.title, link)

            elif submission.id not in seen_posts:
                send_email(submission.id, submission.title, link)
                print("New notification from {0}. {1} \n{2}\n".format(
                    sub, submission.title, link))
                seen_posts.append(submission.id)

            else:
                print("Already seen: {0}\n".format(submission.title))

    while True:
        try:
            for sub in subreddits:
                check_new_posts(sub)
                time.sleep(5)
                first = False

        except KeyboardInterrupt:
            print('\n')
            sys.exit(0)

        except Exception as e:
            print('Error:', e)
            time.sleep(5)
