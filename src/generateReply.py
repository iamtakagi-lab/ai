import re

import os
import random
from myTweets import fetch_tweets, load_tweets

from uptime import get_uptime_fmt
from makeSentence import make_sentence
from constants import API
from utils import get_version_string
from bingo import get_bingo
from tweetInfo import get_tweet_info
from warikan import get_warikan
from generateModel import generate_model
from dice import get_dice

def generate_reply(text, source_conversation_id=None):
    # じゃんけん
    if re.compile(r"(?:[✊👊✌✋🖐]|[ぐぱグパ]ー|ちょき|チョキ|じゃんけん|ジャンケン)").search(text):
        reply_msg = random.choice(("ぐー", "ちょき", "ぱ"))

    # ビンゴ
    elif re.compile(r"(びんご|ビンゴ|ダウト|だうと)").search(text):
        reply_msg = get_bingo(source_conversation_id)

    # Retrieve tweet information
    elif "info" in text:
        reply_msg = get_tweet_info(source_conversation_id)

    # 割り勘
    elif re.compile(r"(割り勘|わりかん|わって|われ|わる|割って|割る|割れ)").search(text):
        reply_msg = get_warikan(text)

    # Dice rolling
    elif re.compile(r"\d{1,2}d\d{1,3}|\d{1,2}D\d{1,3}").search(text):
        reply_msg = get_dice(text)

    # Version info
    elif "ver" in text:
        reply_msg = get_version_string()

    # Uptime
    elif "up" in text:
        reply_msg = get_uptime_fmt()

    else:
        if not load_tweets():
            fetch_tweets()
            generate_model()
        reply_msg = make_sentence()

    return reply_msg
