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

# Returns a spotify client object
def init_spotify_client():
    try:
        print('Initialising Spotify Client....')
        token = util.prompt_for_user_token(user_id, playlist_scope,
                                           client_id=spotify_client_id,
                                           client_secret=spotify_client_secret,
                                           redirect_uri='http://localhost/')
        spotify_client = spotipy.Spotify(auth=token)
        print('\nClient initialised!\n')
        return spotify_client
    except:
        sys('\nError initialising Spotify Client!\n')

spotify_client = init_spotify_client()
