#app/twitify.py

import sys
import csv
import os
from dotenv import load_dotenv
import requests
import spotipy
import spotipy.util as util

user_id = os.environ.get("spotify_username")
playlist_scope = os.environ.get("scope")
spotify_client_id = os.environ.get("client_id")
spotify_client_secret = os.environ.get("client_secret")



#https://spotipy.readthedocs.io/en/2.12.0/

#app/twitify.py

from dotenv import load_dotenv
import json
import requests
import os

###to do: add token info

#Step 1: Pull data from the twitter account

#Step 2: Search spotify for songs (https://developer.spotify.com/console/get-search-item/)

def get_spotify_uri(song, artist):
    query = "https://api.spotify.com/v1/search?q={}%20{}&type=track%2Cartist&market=US&limit=10&offset=5".format(song,artist)

    response = requests.get(
        query,
        headers={
            "Content-Type": "application/json",
            "Authorization: Bearer {}".format(token)
        }
    )
    response_json = response.json()
    
    return respons_json["tracks"]["items"][0]["uri"]

#Step 3: Create a new playlist (https://developer.spotify.com/console/post-playlists/)

def create_playlist():
    request_body - json.dumps({
        "name": "Twitify Playlist",
        "description": "New Twitify playlist",
        "public": True
    })

    query = "https://api.spotify.com/v1/users/{}/playlists".format(user_id)

    response = requests.post(
        query,
        data=request_body,
        headers={
            "Content-Type": "application/json",
            "Authorization: Bearer {}".format(token)
        }
    )
    response_json = response.json()

    return response_json["id"]

#Step 4: Add song to playlist
