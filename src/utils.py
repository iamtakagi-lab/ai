import random
import string
import platform
import os
from twitter_text import parse_tweet
from hash import get_hash

def get_reference_code(length=10):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def get_version_string():
    result = "🤖 ai (https://github.com/yuderobot/ai {})\n- 環境: {}\n- Python 実装: {}\n- Python バージョン: {}".format(get_hash(), platform.platform(), platform.python_implementation(), platform.python_version())

    if os.getenv("FLY_APP_NAME") is not None:
        result += "\n- fly.io リージョン: {}".format(os.environ["FLY_REGION"])

    return result

def get_twitter_text_count(text):
    try:
        result = parse_tweet(text).asdict()["weightedLength"]
    except Exception:
        result = 280
    return result
