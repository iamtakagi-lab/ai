from myTweets import fetch_tweets
from generateModel import generate_model
from constants import API
from makeSentence import make_sentence

def tweet():
    fetch_tweets()
    generate_model()
    API.update_status(status = make_sentence())
    API.update_status(status = make_sentence())