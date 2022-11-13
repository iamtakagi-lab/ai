from constants import API
from utils import datetime_format

def get_tweet_info(source_conversation_id):
    if source_conversation_id is None:
        reply_msg = "取得先のツイートが存在しません。こちらから参照できるツイートに対して先程のようにリプライしてみてください。"
    else:
        this_tweet = API.get_status(source_conversation_id)
        if this_tweet is None:
            reply_msg = "ツイートの情報を取得できませんでした。"
        else:
            reply_msg = """
                - ツイート ID: {}\n- 作者 ID: {}\n- 日時: {}\n- クライアント: {}
                """.format(this_tweet.id, this_tweet.user.id_str, datetime_format(this_tweet.created_at), this_tweet.source)

    return reply_msg
