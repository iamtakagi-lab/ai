from apscheduler.schedulers.background import BackgroundScheduler
from generateModel import generate_model
from makeSentence import make_sentence
from myTweets import fetch_tweets, load_tweets
from tweet import tweet
import logging
from replyStream import ReplyStreamListener, ReplyStream
from constants import AUTH
from flask_cors import CORS
from flask import Flask, jsonify
import os
import numpy as np

logging.basicConfig(level=logging.DEBUG)

sched = BackgroundScheduler(daemon=True)

@sched.scheduled_job('cron', id='tweet', minute='*/15')
def cron_tweet():
    tweet()


# @sched.scheduled_job('interval', id='reply_stream', seconds=60)
# def reply_stream():
#     listener = ReplyStreamListener()
#     stream = ReplyStream(AUTH, listener)
#     stream.start()

sched.start()
app = Flask(__name__)
CORS(app)

@app.get("/api/make_sentence")
def api_make_sentence():
    if not load_tweets():
        fetch_tweets()
        generate_model()
    return jsonify({'sentence': make_sentence()})
    

app.run (
    threaded=True,
    host = os.environ["HOST"], 
    port = os.environ["PORT"], 
    debug=False
)