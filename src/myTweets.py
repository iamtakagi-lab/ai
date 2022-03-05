from constants import users, api

def fetch_tweets():
    tweets = []

    for sn in users:
        max_id = None

        while True:
            if max_id:
                tw = api.user_timeline(
                    screen_name=sn, trim_user=True, include_rts=False, count=100, max_id=max_id)
            else:
                tw = api.user_timeline(
                    screen_name=sn, trim_user=True, include_rts=False, count=100)

            if len(tw) < 1:
                break
            max_id = tw[-1].id - 1

            [tweets.append(tweet.text)
                for tweet in tw if "http" not in tweet.text and "@" not in tweet.text]
        print(f"{sn} done")

    print(f"{len(tweets)}tweets")

    with open("data/tweets.txt", "w") as f:
        f.write("\n".join(tweets))

def load_tweets():
    with open("data/tweets.txt", "r") as f:
        tweets = f.read()
    return tweets