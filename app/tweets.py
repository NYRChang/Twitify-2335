#instructions from https://www.youtube.com/watch?v=dQG4mkD5Nd4&list=PLFf4kGVxRmKXFQgtSctIE0iYsQE26F1UM&index=4&t=0s

import os
import json
import requests 
import twitter
from dotenv import load_dotenv

load_dotenv()

consumer_key = os.environ.get("APP_KEY")
consumer_secret = os.environ.get("APP_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_secret = os.environ.get("ACCESS_TOKEN_SECRET")

#authenticate user via https://python-twitter.readthedocs.io/en/latest/getting_started.html

api = twitter.Api(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token_key=access_token,
    access_token_secret=access_secret)

mentions = api.GetMentions()
# print(type(mentions))
tweets = json.dumps(mentions)
print(tweets)