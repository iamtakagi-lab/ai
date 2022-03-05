from tweepy import Stream, StreamListener
from constants import api
from generateModel import generate_model
from makeSentence import make_sentence
from myTweets import fetch_tweets, load_tweets

class ReplyStreamListener(StreamListener):

    def on_status(self, status):
        print("[Info] Retrieved tweet: ", status.text)
        if not load_tweets():
            fetch_tweets()
            generate_model()
        reply_msg = make_sentence()
        if reply_msg == None: pass
        if "@takagi_ai" in reply_msg:
            pass
            print("This tweet contains reply to @iamtakagi_ai, skipped.")
        else:
            api.update_status(reply_msg, in_reply_to_status_id=status.id)
            print("Sent tweet: {}".format(reply_msg))
        return True

    def on_error(self, status_code):
        if status_code == 420:
            print('[Error] 420')
            return False
        else:
            print(f'[Error] {status_code}')
            return False

class ReplyStream():
    def __init__(self, auth, listener):
        self.stream = Stream(auth=auth, listener=listener)

    def start(self):
        self.stream.filter(track=["@iamtakagi_ai"])