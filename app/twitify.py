#app/twitify.py

import sys
import csv
import os
from dotenv import load_dotenv
import requests
import spotipy
import spotipy.util as util

#user_id = os.environ.get("spotify_username")
#playlist_scope = os.environ.get("scope")
#spotify_client_id = os.environ.get("client_id")
#spotify_client_secret = os.environ.get("client_secret")

#username = sys.argv[1]
#playlist_id = sys.argv[2]
#track_ids = sys.argv[3:]

#https://github.com/nikhilgaba001/YoutubeToSpotify/blob/master/YoutubeToSpotify.py
#https://stackoverflow.com/questions/49418717/spotify-api-illegal-redirect-uri

#Validating Spotify Connection 

SPOTIFY_USERNAME = 'ssjmusashi'
CLIENT_ID = 'bb23555d00c74343851e1bd782fd1731'
CLIENT_SECRET = 'bf206e3b6d604b7b88d3afd9e739ec0f'
SCOPE = 'playlist-modify-private'
playlist_id = '5yeB2JFf09vQ6Na9003kMo'
track_ids = ["1lKS7SZQ7r5vOChLwJurmm"]

def init_spotify_client():
    try:
        print('Initialising Spotify Client....')
        token = util.prompt_for_user_token(SPOTIFY_USERNAME, SCOPE,
                                           client_id=CLIENT_ID,
                                           client_secret=CLIENT_SECRET,
                                           redirect_uri='http://localhost:8888/callback/')
        spotify_client = spotipy.Spotify(auth=token)
        print('\nClient initialised!\n')
        return spotify_client
    except:
        sys('\nError initialising Spotify Client!\n')

spotify_client = init_spotify_client()

#Adding Songs to Playlist
#https://spotipy.readthedocs.io/en/2.12.0/
spotify_client.trace = False
results = spotify_client.user_playlist_add_tracks(SPOTIFY_USERNAME, playlist_id, track_ids)
print(results)

#scope = 'playlist-modify-public'
#token = util.prompt_for_user_token(username, scope)


""" 
#https://spotipy.readthedocs.io/en/2.12.0/

#app/twitify.py

from dotenv import load_dotenv
import json
import requests
import os

###to do: add token info

#Step 1: Pull data from the twitter account

#Step 2: Search spotify for songs (https://developer.spotify.com/console/get-search-item/)

# def get_spotify_uri(song, artist):
#     query = "https://api.spotify.com/v1/search?q={}%20{}&type=track%2Cartist&market=US&limit=10&offset=5".format(song,artist)

#     response = requests.get(
#         query,
#         headers={
#             "Content-Type": "application/json",
#             "Authorization: Bearer {}".format(token)
#         }
#     )
#     response_json = response.json()
    
#     return respons_json["tracks"]["items"][0]["uri"]

#Step 3: Create a new playlist (https://developer.spotify.com/console/post-playlists/)

# def create_playlist():
#     request_body - json.dumps({
#         "name": "Twitify Playlist",
#         "description": "New Twitify playlist",
#         "public": True
#     })

#     query = "https://api.spotify.com/v1/users/{}/playlists".format(user_id)

#     response = requests.post(
#         query,
#         data=request_body,
#         headers={
#             "Content-Type": "application/json",
#             "Authorization: Bearer {}".format(token)
#         }
#     )
#     response_json = response.json()

#     return response_json["id"]"

#Step 4: Add song to playlist

uris = "spotify:track:62bOmKYxYg7dhrC6gH9vFn"
playlist_id = "5yeB2JFf09vQ6Na9003kMo"

 """