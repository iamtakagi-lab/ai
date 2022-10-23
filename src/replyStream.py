from tweepy import StreamingClient
from constants import API, CLIENT
from generateModel import generate_model
import re
import random
from makeSentence import make_sentence
import parse
import platform
import unicodedata
import math
import Levenshtein
from dice import simple_dice
from myTweets import fetch_tweets, load_tweets, load_tweets_line
from hash import get_hash
import os
from uptime import get_uptime

class ReplyStream(StreamingClient):
    def on_tweet(self, tweet):

        # `!ignore` が付加されているツイートには、返信しない。
        if "!ignore" not in tweet.text:

            # じゃんけん
            if re.compile(r"(?:[✊👊✌✋🖐]|[ぐぱグパ]ー|ちょき|チョキ|じゃんけん|ジャンケン)").search(tweet.text):
                reply_msg = random.choice(("ぐー", "ちょき", "ぱ"))
            
            # Bingo
            elif re.compile(r"(びんご|ビンゴ)").search(tweet.text):
                if tweet.in_reply_to_status_id is None:
                    reply_msg = "なにが？"
                else:
                    bot_tweet = API.get_status(tweet.in_reply_to_status_id)
                    tweets = load_tweets_line()

                    if bot_tweet.text in tweets:
                        reply_msg = "オオアオ・・・"
                    else:
                        distance = math.inf
                        for tweet in tweets:
                            this_distance = Levenshtein.distance(tweet, bot_tweet.text)
                            if distance > this_distance:
                                distance = this_distance
                        reply_msg = "ぶっぶーーーー！\n(レーベンシュタイン距離: {})".format(distance)

            # Retrieve tweet information
            elif "@{} info".format(API.verify_credentials().screen_name) in tweet.text:
                if tweet.in_reply_to_status_id is None:
                    reply_msg = "取得先のツイートが存在しません。こちらから参照できるツイートに対して先程のようにリプライしてみてください。"
                else:
                    this_tweet = API.get_status(tweet.in_reply_to_status_id)
                    if this_tweet is None:
                        reply_msg = "ツイートの情報を取得できませんでした。"
                    else:
                        reply_msg = """
                                    ツイートの情報\n・ID: {}\n・日時: {}\n・クライアント: {}
                                    """.format(
                                        this_tweet.id,
                                        str(this_tweet.created_at),
                                        this_tweet.source
                                    )

            # 割り勘
            elif re.compile(r"(割り勘|わりかん|わって|われ|わる|割って|割る|割れ)").search(tweet.text):
                unicodedata.normalize("NFKC", tweet.text)
                parsed = parse.parse("@{} {}を{}で{}", tweet.text)
                if parsed is None:
                    reply_msg = "使用法: 2130を5で割り勘"
                else:
                    if parsed[1].isnumeric() and parsed[2].isnumeric():
                        reply_msg = "結果: 1人あたり" + str(int(parsed[1]) / int(parsed[2])) + "円"
                    else:
                        reply_msg = "使用法: 2130を5で割り勘 変な値入れるな❗"

            # Dice rolling
            elif re.compile(r"\d{1,2}d\d{1,3}|\d{1,2}D\d{1,3}").search(tweet.text):
                dice = parse.parse('@{} {}d{}', tweet.text)
                if dice is None:
                    dice = parse.parse('@{} {}D{}', tweet.text)
                
                reply_msg = simple_dice(dice[2], dice[1])

            # Version info
            elif "ver" in tweet.text:
                reply_msg = "🤖 ai (https://github.com/yuderobot/ai {}) on {}, {}, {}".format(get_hash(), platform.platform(), platform.python_implementation(), platform.python_version())

            # Uptime
            elif "up" in tweet.text:
                reply_msg = "⌚ 稼働時間: {}".format(get_uptime())

            else:
                if not load_tweets():
                    fetch_tweets()
                    generate_model()
                reply_msg = make_sentence()

                if reply_msg == None: pass
            
            # Truncate reply message if it exceeds 130 chars
            if (len(reply_msg) > 130):
                reply_msg = reply_msg[:120] + " ... (省略されました)"

            if tweet.author_id == API.verify_credentials().id:
                pass
            else:
                API.update_status(reply_msg, in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
                print("Sent tweet: {}".format(reply_msg))
        
        # 返信しない場合は、いいね で反応する。
        else:
            CLIENT.like(tweet_id=tweet.id)

        return True
