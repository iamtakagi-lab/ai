import os
import markovify
import MeCab

def generate_model():
    try:
        dict_path = os.getenv("MECAB_DICTIONARY_PATH", "/usr/lib64/mecab/dic/mecab-ipadic-neologd")
        m = MeCab.Tagger(f"-d {dict_path} -Owakati")
    except Exception:
        m = MeCab.Tagger("-Owakati")

    with open("data/tweets.txt", "r") as f:
        data = f.read()

    corpus = "".join([m.parse(s) for s in data.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace(
        "?", "？").replace("!", "！").replace("，", "、").replace("．", "。").replace("。", "。\n")
        .split("\n") if s != ""])
    model = markovify.NewlineText(corpus, state_size=3).to_json()

    with open("data/model.json", "w") as f:
        f.write(model)
