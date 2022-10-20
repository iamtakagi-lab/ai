from tweepy import Stream, StreamListener
from constants import API
from generateModel import generate_model
import re
import random
from makeSentence import make_sentence
import parse
import unicodedata
from myTweets import fetch_tweets, load_tweets, load_tweets_line

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
            elif re.compile(r"(びんご|ビンゴ)").search(status.text):
                if status.in_reply_to_status_id is None:
                    reply_msg = "@{} なにが？".format(status.user.screen_name)
                else:
                    bot_tweet = API.get_status(status.in_reply_to_status_id)
                    tweets = load_tweets_line()
                    
                    if bot_tweet.text in tweets:
                        reply_msg = "@{} オオアオ・・・".format(status.user.screen_name)
                    else:
                        reply_msg = "@{} ぶっぶーーーー！".format(status.user.screen_name)
            elif "@{} info".format(API.verify_credentials().screen_name) in status.text:
                if status.in_reply_to_status_id is None:
                    reply_msg = "@{} 取得先のツイートが存在しません。こちらから参照できるツイートに対して先程のようにリプライしてみてください。".format(status.user.screen_name)
                else:
                    this_tweet = API.get_status(status.in_reply_to_status_id)
                    if this_tweet is None:
                        reply_msg = "@{} ツイートの情報を取得できませんでした。".format(status.user.screen_name)
                    else:
                        reply_msg = """
                                    @{} ツイートの情報\n・ID: {}\n・日時: {}\n・クライアント: {}
                                    """.format(
                                        status.user.screen_name,
                                        this_tweet.id,
                                        str(this_tweet.created_at),
                                        this_tweet.source
                                    )
            elif re.compile(r"(割り勘|わりかん|わって|われ|わる|割って|割る|割れ)").search(status.text):
                unicodedata.normalize("NFKC", status.text)
                parsed = parse.parse("@{} {}を{}で{}", status.text)
                if parsed is None:
                    reply_msg = "@{} 使用法: 2130を5で割り勘".format(status.user.screen_name)
                else:
                    if parsed[1].isnumeric() and parsed[2].isnumeric():
                        reply_msg = "@{} 結果: 1人あたり".format(status.user.screen_name) + str(int(parsed[1]) / int(parsed[2])) + "円"
                    else:
                        reply_msg = "@{} 使用法: 2130を5で割り勘 変な値入れるな❗".format(status.user.screen_name)
            else:
                pass
            
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