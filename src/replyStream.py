from tweepy import StreamingClient
from constants import API, CLIENT
from generateReply import generate_reply
from utils import get_reference_code

class ReplyStream(StreamingClient):
    def on_tweet(self, tweet):

        # 取得したツイートの author がボット自身である場合、何も反応しない。
        if tweet.author_id == API.verify_credentials().id:
            pass
        else:
            # `!ignore` が付加されているツイートには、返信しない。
            if "!ignore" not in tweet.text:
                try:
                    reply_msg = generate_reply(tweet.text, tweet.conversation_id)
                except Exception as e:
                    reply_msg = "問題が発生しました ({}, 照会甩コード: {}".format(e.args[0], get_reference_code())

                if reply_msg is None:
                    print("[info] reply_msg is None. Skipping.")

                # Truncate reply message if it exceeds 130 chars
                if (len(reply_msg) > 130):
                    reply_msg = reply_msg[:120] + " ... (省略されました)"

                else:
                    API.update_status(reply_msg, in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
                    print("Sent tweet: {}".format(reply_msg))

            # 返信しない場合は、いいね で反応する。
            else:
                CLIENT.like(tweet_id=tweet.id)

        return True
