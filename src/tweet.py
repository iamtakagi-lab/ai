from myTweets import fetch_tweets
from generateModel import generate_model
from constants import API
from makeSentence import make_sentence

import numpy as np
import json

def tweet():
    # generate tweet by using markov or original tweet
    selection = np.random.choice(["markov", "original"], p=["0.95", "0.05"])
    
    if selection == "markov":
        fetch_tweets()
        generate_model()

        API.update_status(
                status = make_sentence()
            )
    else:
        API.update_status(
                status = make_sentence()
            )