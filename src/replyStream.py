from tweepy import Stream, StreamListener
from constants import API
from generateModel import generate_model
import re
import random
from makeSentence import make_sentence
from myTweets import fetch_tweets, load_tweets

class ReplyStreamListener(StreamListener):

    def on_status(self, status):
        print("[Info] Retrieved tweet: ", status.text)
        if not load_tweets():
            fetch_tweets()
            generate_model()
        reply_msg = "@{} {}".format(status.user.screen_name, make_sentence())
        if reply_msg == None: pass
        if "@{}".format(API.verify_credentials().screen_name) in reply_msg:
            pass
            print("This tweet contains reply to @{}, skipped.".format(API.verify_credentials().screen_name))
        else:
            if re.compile(r"(?:[✊👊✌✋🖐]|[ぐぱグパ]ー|ちょき|チョキ|じゃんけん|ジャンケン)").search(status.text):
                reply_msg = "@{} {}".format(status.user.screen_name, random.choice(("ぐー", "ちょき", "ぱ")))
                API.update_status(reply_msg, in_reply_to_status_id=status.id)
            else:
                API.update_status(reply_msg, in_reply_to_status_id=status.id)
            print("Sent tweet: {}".format(reply_msg))
        return True

    def on_error(self, status_code):
        if status_code == 420:
            print('[Error] 420 Too Many Requests')
            return False
        else:
            print(f'[Error] {status_code}')
            return False

class ReplyStream():
    def __init__(self, auth, listener):
        self.stream = Stream(auth=auth, listener=listener)

    def start(self):
        print("[INFO] Started streaming: {}".format(API.verify_credentials().screen_name))
        self.stream.filter(track=["@{}".format(API.verify_credentials().screen_name)])