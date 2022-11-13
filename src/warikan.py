import unicodedata
import parse

def get_warikan(text):
    unicodedata.normalize("NFKC", text)
    parsed = parse.parse("@{} {}を{}で{}", text)
    if parsed is None:
        reply_msg = "使用法: 2130を5で割り勘"
    else:
        if parsed[1].isnumeric() and parsed[2].isnumeric():
            reply_msg = "結果: 1人あたり" + str(int(parsed[1]) / int(parsed[2])) + "円"
        else:
            reply_msg = "使用法: 2130を5で割り勘 変な値入れるな❗"

    return reply_msg
