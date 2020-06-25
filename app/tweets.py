#app/tweets.py

import csv
import os
import json

import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("SECRET_API_KEY")


request_url = f"https://api.twitter.com/1.1/search/tweets.json?q=%40twitterapi"

response = requests.get(request_url)
        
parsed_response = json.loads(response.text) #>Parse response.text into a dictionary
        
print(parsed_response)