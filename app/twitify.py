#app/twitify.py

import json
import os
from datetime import datetime, timedelta, time
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


SCOPE = 'playlist-modify-public playlist-modify-private playlist-read-collaborative'

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

#Old Code
# tweets = []
# for m in mentions:
#     if str(" // ") not in m["text"]:
#         try:
#             api.PostUpdate(status=f"@{m['user']['screen_name']} Please separate Artist and Title with a '//' :)", in_reply_to_status_id=m['id'])
#         except:
#             pass
#         #found that username must be included in reply tweet from https://developer.twitter.com/en/docs/tweets/post-and-engage/api-reference/post-statuses-update
#     else:
#         pass
#     filtered_tweet = m["text"].replace("@Twitify2335 ", "") #.replace method via https://stackoverflow.com/questions/3939361/remove-specific-characters-from-a-string-in-python
#     if "//" in filtered_tweet:
#         tweets.append(filtered_tweet)


#New Code to so that only tweets under 0.5 days are replied if incorrect format.  
tweets = []
for m in mentions:
    if str("//") not in m["text"]:
        try:
            if (datetime.datetime.now(datetime.timezone.utc) - (datetime.datetime.strptime(m["created_at"], "%a %b %d %H:%M:%S %z %Y"))) < timedelta(days=0.5):
                api.PostUpdate(status=f"@{m['user']['screen_name']} Please separate Artist and Title with a '//' :)", in_reply_to_status_id=m['id'])
            #got datetime.now to be "aware" using the .utc argument from https://stackoverflow.com/questions/4530069/how-do-i-get-a-value-of-datetime-today-in-python-that-is-timezone-aware
            else:
                pass
        except:
            pass
        #found that username must be included in reply tweet from https://developer.twitter.com/en/docs/tweets/post-and-engage/api-reference/post-statuses-update
    else:
        pass
    filtered_tweet = m["text"].replace("@Twitify2335 ", "") #.replace method via https://stackoverflow.com/questions/3939361/remove-specific-characters-from-a-string-in-python
    if "//" in filtered_tweet:
        if filtered_tweet.count("//") == 1: #inputs must only contain 1 "//".  No Twitter Reply for this format yet.  
            tweets.append(filtered_tweet)



#Assembling Dictionary of Artists/Titles using Pandas
text = []
for t in tweets:
    text.append(t.split("//"))
df = pd.DataFrame(text)
df.columns = ["Artist", "Title"]
tracks_to_search = df.to_dict("records")

#Step 2: Search spotify for songs (https://developer.spotify.com/console/get-search-item/)

#Defining Function to obtain Spotify Web API token
def init_spotify_client():
    try:
        spotify_client = spotipy.Spotify(auth=token)
        print('Spotify Connection Successful!')
        return spotify_client
    except:
        print('Spotify Connection Failed')



#Defining Function to Find Spotify Songs
def get_spotify_uri(song, artist):
    query = "https://api.spotify.com/v1/search?q={}%20{}&type=track%2Cartist&market=US&limit=10&offset=0".format(song,artist)

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

#Obtaining Spotify Token
print("")
print('Initialising Spotify Connection...')
spotify_client = init_spotify_client()

# How to read items from a playlist via spotipy
#https://github.com/XDGFX/spotr/blob/master/spotr.py

data = spotify_client.user_playlist(SPOTIFY_USERNAME, playlist_id, fields="tracks")
tracks = data['tracks']['items']

#list of songs by Spotify URI already on playlist
existing_songs = []
for t in tracks:
    existing_songs.append(t["track"]["id"])


#adding songs to playlist via Custom Function get_spotify_uri
print("Pulling Twitter Song Requests via Twittify")
print("...")
print("..")
print(".")
print("")
uri_to_search = []
success_songs = []
skipped_songs = []
error_songs = []
for search in tracks_to_search:
    try:
        spotify_uri = get_spotify_uri(search["Title"], search["Artist"])
        track_uri = str(spotify_uri.replace("spotify:track:", ""))
        if track_uri in existing_songs:
            skipped_songs.append(search)
        else:  
            success_songs.append(search)
            uri_to_search.append(track_uri)
    except:
        error_songs.append(search)
        pass


#Pushing Songs to Playlist
#https://spotipy.readthedocs.io/en/2.12.0/
spotify_client.trace = False
print("")
print("-----------------------------------")
if uri_to_search != []:
    results = spotify_client.user_playlist_add_tracks(SPOTIFY_USERNAME, playlist_id, uri_to_search)
    print("Your Twitify2335 Playlist have been successfully updated.")
    print("Your Snapshot ID: ", results["snapshot_id"])
    print("Your Summary below:  ")
    print("-----------------------------------")
    print("The following new songs from your feed were successfully added:  ")
    for success in success_songs:
        print("Success!" , success["Artist"],"//", success["Title"])
    print("-----------------------------------")
    print("The following songs from your feed were already on your playlist:  ")
    for skip in skipped_songs:
        print("*Skip*" , skip["Artist"],"//", skip["Title"])
    print("-----------------------------------")
    print("The following songs requests from your feed were not found on Spotify:  ")
    for error in error_songs:
        print("*Error*", error["Artist"],"//", error["Title"])   
else:
    print("No new songs to add from your feed at this time!")
    print("Tweet some more song requests @ your Twitify Account")
print("-----------------------------------")
print("THANK YOU FOR TRYING TWITIFY!")
print("")

