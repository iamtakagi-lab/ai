from apscheduler.schedulers.background import BackgroundScheduler
from generateModel import generate_model
from makeSentence import make_sentence
from myTweets import fetch_tweets, load_tweets
from tweet import tweet
import tweepy
import logging
from constants import API
from replyStream import ReplyStream
from constants import AUTH
from flask_cors import CORS
from flask import Flask, jsonify, render_template
import os
import numpy as np
import threading

logging.basicConfig(level=logging.DEBUG)

sched = BackgroundScheduler(daemon=True)

# Regular tweet; 15 min interval
@sched.scheduled_job('cron', id='tweet', minute='*/15')
def cron_tweet():
    tweet()

# Reply streaming
@sched.scheduled_job('interval', id='reply_stream', seconds=60)
def reply_stream():
    client = ReplyStream(bearer_token=os.environ["TWITTER_BEARER"])
    client.add_rules(tweepy.StreamRule("@{} -from:{} -filter:retweets".format(API.verify_credentials().screen_name, API.verify_credentials().screen_name)))
    client.filter(expansions=["author_id", "referenced_tweets.id", "in_reply_to_user_id"], tweet_fields=["author_id", "conversation_id"])


sched.start()


# Flask app for JSON api, etc.
app = Flask(__name__)
CORS(app)

@app.get("/")
def home():
    return render_template('index.html', me=API.verify_credentials().screen_name)

# Endpoint for `/api/make_sentence`
@app.get("/api/make_sentence")
def api_make_sentence():
    if not load_tweets():
        fetch_tweets()
        generate_model()
    return jsonify({'sentence': make_sentence()})

# Endpoint for `/api/me`
@app.get("/api/me")
def api_me():
    return jsonify({'screen_name': API.verify_credentials().screen_name})


# Run Flask app
app.run(
    threaded=True,
    host=os.environ["HOST"],
    port=os.environ["PORT"],
    debug=False
)
