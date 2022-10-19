from myTweets import fetch_tweets
from generateModel import generate_model
from constants import API
from makeSentence import make_sentence

import json

def remover(result):
  # Load banned.json
  json_open = open('data/banned.json', 'r')
  json_load = json.load(json_open)
  for w in json_load['words']:
    result = result.replace(w, '')
  return result

def tweet():
    fetch_tweets()
    generate_model()
    API.update_status(
            status = remover(
                    make_sentence()
                )
        )