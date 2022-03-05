from myTweets import fetch_tweets
from generateModel import generate_model
from constants import api
from makeSentence import make_sentence

def tweet():
    fetch_tweets()
    generate_model()
    api.update_status(status = make_sentence())
    api.update_status(status = make_sentence())