# Twitify-2335

To run Twitify:

1. Clone this repo from https://github.com/NYRChang/Twitify-2335 to your Github desktop

2. Set up a .env file in your cloned repo and get your Twitter and Spotify API keys set equal to the following environment variables: 

    Spotify API Keys via https://developer.spotify.com/dashboard/login

        user_id
        spotify_client_id
        spotify_client_secret
        playlist

    Twitter API Keys and Access tokens via https://developer.twitter.com/en/

        APP_KEY
        APP_SECRET
        ACCESS_TOKEN
        ACCESS_TOKEN_SECRET


3. Set up a virtual environment:

    conda create -n twitify-env python=3.7 # (first time only)
    conda activate twitify-env

4. Install the package requirements via the requirements.txt file:

    pip install -r requirements.txt

5. Log into Twitter and Tweet a song @Twitify2335 in the format 

    "Artist" // "Songname"

6. Run the script via apps/twitify.py