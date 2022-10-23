from constants import API

def get_tweet_info(source_conversation_id):
    if source_conversation_id is None:
        reply_msg = "取得先のツイートが存在しません。こちらから参照できるツイートに対して先程のようにリプライしてみてください。"
    else:
        this_tweet = API.get_status(source_conversation_id)
        if this_tweet is None:
            reply_msg = "ツイートの情報を取得できませんでした。"
        else:
            reply_msg = """
                ツイートの情報\n・ID: {}\n・日時: {}\n・クライアント: {}
                """.format(this_tweet.id, str(this_tweet.created_at), this_tweet.source)

    return reply_msg
