# have all this run on the cloud

import time

from helper_functions import get_new_posts

if __name__ == "__main__":

    subreddits = ["GameDeals", "buildapcsales",
                  "hardwareswap", "consoledeals", "NintendoSwitchDeals"]

    while True:
        try:
            for sub in subreddits:
                get_new_posts(sub)
                time.sleep(5)

        except Exception as e:
            print('Error:', e)
            time.sleep(5)
