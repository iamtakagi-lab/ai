from myTweets import load_tweets_line
import math
import Levenshtein
from constants import API

def get_bingo(source_conversation_id=None):
    if source_conversation_id is None:
        reply_msg = "なにが？"
    else:
        bot_tweet = API.get_status(source_conversation_id)
        source_tweets = load_tweets_line()

        if bot_tweet.text in source_tweets:
            reply_msg = "オオアオ・・・"
        else:
            distance = math.inf
            for tweet in source_tweets:
                this_distance = Levenshtein.distance(tweet, bot_tweet)
                if distance > this_distance:
                    distance = this_distance
            reply_msg = "ぶっぶーーーー！\n(レーベンシュタイン距離: {})".format(distance)

    return reply_msg
