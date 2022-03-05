import os
import tweepy

users = os.getenv("USERS", "iam_takagi").split(",")

auth = tweepy.OAuthHandler(os.environ["TWITTER_CK"],
                           os.environ["TWITTER_CS"])
auth.set_access_token(os.environ["TWITTER_AT"],
                      os.environ["TWITTER_ATS"])

api = tweepy.API(auth)