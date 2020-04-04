# have all this run on the cloud

import time

import praw

import local_settings
from helper_functions import (process_hardwareswap_submission,
                              process_submission)


if __name__ == "__main__":

    subreddits = ["GameDeals", "buildapcsales", "hardwareswap", "consoledeals"]

    reddit = praw.Reddit(client_id=local_settings.client_id,
                         client_secret=local_settings.client_secret,
                         password=local_settings.password,
                         username="decheverri123",
                         user_agent="test script")

    seen_posts = []

    def check_new_posts(sub):
        for submission in reddit.subreddit(sub).new(limit=1):

            link = "https://reddit.com{0}".format(submission.permalink)

            if not seen_posts or submission.id not in seen_posts:
                if sub == "hardwareswap":
                    process_hardwareswap_submission(sub, submission, link)
                    seen_posts.append(submission.id)

                else:
                    process_submission(sub, submission, link)
                    seen_posts.append(submission.id)

    while True:
        try:
            for sub in subreddits:
                check_new_posts(sub)
                time.sleep(5)

        except Exception as e:
            print('Error:', e)
            time.sleep(5)
