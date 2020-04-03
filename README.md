# RedditNewPostBot
Sends a text message every time a new submission is made on selected subreddits. 

Uses PRAW to access the Reddit API and smtplib to send emails which then sends a text message.

You will need to register an app with the Reddit API to be able to use this. You will also need a number from AT&T to receive text messages. 

Create a local_settings.py file and create the variables used by the script to keep them hidden. 