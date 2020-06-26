#app/twitify.py


import os
from dotenv import load_dotenv
import requests
import spotipy
import spotipy.util as util


#https://github.com/nikhilgaba001/YoutubeToSpotify/blob/master/YoutubeToSpotify.py
#https://stackoverflow.com/questions/49418717/spotify-api-illegal-redirect-uri

#Add token info - Validating Connection
load_dotenv()
SPOTIFY_USERNAME = os.environ.get('user_id')
CLIENT_ID = os.environ.get('spotify_client_id')
CLIENT_SECRET = os.environ.get('spotify_client_secret')
playlist_id = os.environ.get('playlist')


SCOPE = 'playlist-modify-private'
track_ids = ["1lKS7SZQ7r5vOChLwJurmm","13X42np3KJr0o2LkK1MG76"]

token = util.prompt_for_user_token(SPOTIFY_USERNAME, SCOPE,
                                           client_id=CLIENT_ID,
                                           client_secret=CLIENT_SECRET,
                                           redirect_uri='http://localhost:8888/callback/')

def init_spotify_client():
    try:
        print('Initialising Spotify Client....')
        spotify_client = spotipy.Spotify(auth=token)
        print('Spotify Connection Successful!')
        return spotify_client
    except:
        sys('Spotify Connection Failed')

spotify_client = init_spotify_client()

breakpoint()

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

    return response_json["tracks"]["items"][0]["uri"]

get_spotify_uri("My Love", "Justin Timberlake")

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

#Adding Songs to Playlist
#https://spotipy.readthedocs.io/en/2.12.0/
spotify_client.trace = False
results = spotify_client.user_playlist_add_tracks(SPOTIFY_USERNAME, playlist_id, track_ids)
print(results)