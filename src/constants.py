import os
import tweepy
import datetime

# Load markov-chain target users. Split by comma and store as array.
USERS = os.getenv("USERS", "yude_jp").split(",")

# Twitter credentials
AUTH = tweepy.OAuthHandler(os.environ["TWITTER_CK"],
                           os.environ["TWITTER_CS"])
AUTH.set_access_token(os.environ["TWITTER_AT"],
                      os.environ["TWITTER_ATS"])

# Tweepy API handler as global
API = tweepy.API(AUTH)

# The datetime app started
STARTED = datetime.datetime.utcnow()