from myTweets import fetch_tweets, random_tweet
from generateModel import generate_model
from constants import API
from makeSentence import make_sentence

import tweepy
import numpy as np
import json

def tweet():
    # generate tweet by using markov or original tweet
    selection = np.random.choice(["markov", "original"], p=["0.95", "0.05"])
    new_tweet = ""
    
    if selection == "markov":
        fetch_tweets()
        generate_model()

        new_tweet = make_sentence()
    else:
        new_tweet = random_tweet()
    
    print("[INFO] Trying to tweet: \"{}\"".format(new_tweet))

    try:
        API.update_status(status = new_tweet)
    except tweepy.TweepError as error:
        if error.api.code == 187: # 187: "Status is a duplicate."
            tweet() # Re-try tweet by using another sentence
        else:
            raise error
    
