import os
import tweepy

USERS = os.getenv("USERS", "iam_takagi").split(",")

AUTH = tweepy.OAuthHandler(os.environ["TWITTER_CK"],
                           os.environ["TWITTER_CS"])
AUTH.set_access_token(os.environ["TWITTER_AT"],
                      os.environ["TWITTER_ATS"])

API = tweepy.API(AUTH)