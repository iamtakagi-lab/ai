from constants import USERS, API
import os
import random

def fetch_tweets():
    tweets = []

    for sn in USERS:
        max_id = None

        while True:
            tw = ""

            if max_id:
                # Ignoring this error, because Twitter sometimes returns internal error
                # for extreme random reason, and we want to tweet something regardless of success of
                # retrieving tweets
                try:
                    tw = API.user_timeline(
                        screen_name=sn, trim_user=True, include_rts=False, count=200, max_id=max_id)
                except Exception:
                    pass
            else:
                try:
                    tw = API.user_timeline(
                        screen_name=sn, trim_user=True, include_rts=False, count=200)
                except Exception:
                    pass

            if len(tw) < 1:
                break
            max_id = tw[-1].id - 1

            [tweets.append(tweet.text.replace("\n", ""))
                for tweet in tw if "http" not in tweet.text and "@" not in tweet.text]
        print(f"{sn} done")

    print(f"{len(tweets)}tweets")

    if os.path.isfile("data/tweets.txt"):
        with open("data/tweets.txt", mode='r+') as current:
            current.truncate(0)
            current.close()

    with open("data/tweets.txt", "w") as f:
        f.write("\n".join(tweets))

def load_tweets():  # Return tweets as string
    if not os.path.isfile("data/tweets.txt"):
        return []
    with open("data/tweets.txt", "r") as f:
        tweets = f.read()
    return tweets

def load_tweets_line():  # Return tweets as array
    if not os.path.isfile("data/tweets.txt"):
        return []
    with open("data/tweets.txt", "r") as f:
        tweets = [s.strip() for s in f.readlines()]
        tweets = list(filter(None, tweets))
        tweets = [t.replace(' ', '') for t in tweets]
    return tweets

def random_tweet():  # Return random one tweet as string
    return random.choice(load_tweets_line())
