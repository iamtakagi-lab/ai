from constants import USERS, API
import os

def fetch_tweets():
    tweets = []

    for sn in USERS:
        max_id = None

        while True:
            if max_id:
                tw = API.user_timeline(
                    screen_name=sn, trim_user=True, include_rts=False, count=200, max_id=max_id)
            else:
                tw = API.user_timeline(
                    screen_name=sn, trim_user=True, include_rts=False, count=200)

            if len(tw) < 1:
                break
            max_id = tw[-1].id - 1

            [tweets.append(tweet.text)
                for tweet in tw if "http" not in tweet.text and "@" not in tweet.text]
        print(f"{sn} done")

    print(f"{len(tweets)}tweets")

    if os.path.isfile("data/tweets.txt"):
        with open("data/tweets.txt", mode = 'r+') as current:
            current.truncate(0)
            current.close()
    
    with open("data/tweets.txt", "w") as f:
        f.write("\n".join(tweets))

def load_tweets():
    if not os.path.isfile("data/tweets.txt"):
        return []
    with open("data/tweets.txt", "r") as f:
        tweets = f.read()
    return tweets

def load_tweets_line():
    if not os.path.isfile("data/tweets.txt"):
        return []
    with open("data/tweets.txt", "r") as f:
        tweets = [s.strip() for s in f.readlines()]
    return tweets