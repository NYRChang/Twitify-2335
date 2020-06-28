#app/twitify.py

import json
import os
from dotenv import load_dotenv
import requests
import spotipy
import spotipy.util as util
import twitter
from itertools import combinations
import pandas as pd


#https://github.com/nikhilgaba001/YoutubeToSpotify/blob/master/YoutubeToSpotify.py
#https://stackoverflow.com/questions/49418717/spotify-api-illegal-redirect-uri

#Add token info - Validating Connection
load_dotenv()
SPOTIFY_USERNAME = os.environ.get('user_id')
CLIENT_ID = os.environ.get('spotify_client_id')
CLIENT_SECRET = os.environ.get('spotify_client_secret')
playlist_id = os.environ.get('playlist')


SCOPE = 'playlist-modify-public'

token = util.prompt_for_user_token(SPOTIFY_USERNAME, SCOPE,
                                           client_id=CLIENT_ID,
                                           client_secret=CLIENT_SECRET,
                                           redirect_uri='http://localhost:8888/callback/')

#setup instructions from https://www.youtube.com/watch?v=dQG4mkD5Nd4&list=PLFf4kGVxRmKXFQgtSctIE0iYsQE26F1UM&index=4&t=0s

load_dotenv()

consumer_key = os.environ.get("APP_KEY")
consumer_secret = os.environ.get("APP_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_secret = os.environ.get("ACCESS_TOKEN_SECRET")

#Step 1: Pull data from the twitter account

#authenticate user via https://python-twitter.readthedocs.io/en/latest/getting_started.html
api = twitter.Api(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token_key=access_token,
    access_token_secret=access_secret)

#method and boolean parameter via https://python-twitter.readthedocs.io/en/latest/twitter.html#module-twitter.models
mentions = api.GetMentions(return_json=True)

tweets = []
for m in mentions:
    filtered_tweet = m["text"].replace("@Twitify2335 ", "") #.replace method via https://stackoverflow.com/questions/3939361/remove-specific-characters-from-a-string-in-python
    if "//" in filtered_tweet:
        tweets.append(filtered_tweet)
    else:  
        api.PostUpdate(status=f"@{mentions['user']['screen_name']} Please separate Artist and Title with a '//' :)", in_reply_to_status_id=mentions['id'])
#       #found that username must be included in reply tweet from https://developer.twitter.com/en/docs/tweets/post-and-engage/api-reference/post-statuses-update


#Reply Tweet if song was added to playlist
#tweets = []
#for m in mentions:
#    filtered_tweet = m["text"].replace("@Twitify2335 ", "") #.replace method via https://stackoverflow.com/questions/3939361/remove-specific-characters-from-a-string-in-python
#    if filtered_tweet not in tweets:
#        tweets.append(filtered_tweet)
#    else:
#        api.PostUpdate(status=f"@{mentions[0]['user']['screen_name']} This song was already added to the playlist! Please pick another :)", in_reply_to_status_id=mentions[0]['id'])
#        #found that username must be included in reply tweet from https://developer.twitter.com/en/docs/tweets/post-and-engage/api-reference/post-statuses-update


text = []
for t in tweets:
    text.append(t.split(" // "))

df = pd.DataFrame(text)

df.columns = ["Artist", "Title"]

tracks_to_search = df.to_dict("records")

#Step 2: Search spotify for songs (https://developer.spotify.com/console/get-search-item/)

def init_spotify_client():
    try:
        print('Initialising Spotify Client....')
        spotify_client = spotipy.Spotify(auth=token)
        print('Spotify Connection Successful!')
        return spotify_client
    except:
        sys('Spotify Connection Failed')

spotify_client = init_spotify_client()

def get_spotify_uri(song, artist):
    query = "https://api.spotify.com/v1/search?q={}%20{}&type=track%2Cartist&market=US&limit=10&offset=5".format(song,artist)

    response = requests.get(
        query,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(token)
        }
    )
    response_json = response.json()
    uri = response_json["tracks"]["items"][0]["uri"]
    return uri

uri_to_search = []
for search in tracks_to_search:
    spotify_uri = get_spotify_uri(search["Title"], search["Artist"])
    track_uri = str(spotify_uri.replace("spotify:track:", ""))
    uri_to_search.append(track_uri)


print(search)


#Adding Songs to Playlist
#https://spotipy.readthedocs.io/en/2.12.0/
spotify_client.trace = False
results = spotify_client.user_playlist_add_tracks(SPOTIFY_USERNAME, playlist_id, uri_to_search)
print(results)