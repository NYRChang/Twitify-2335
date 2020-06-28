# Twitify-2335

To run Twitify:

1. Clone this repo from https://github.com/NYRChang/Twitify-2335 to your Github desktop

2. Open the repo in your text editor and set up a .env file in your cloned repo 

3. Get your Twitter and Spotify API keys set equal to the following environment variables in your .env file: 

    Spotify username:

        user_id
    
    Spotify API Keys via https://developer.spotify.com/dashboard/login

        spotify_client_id
        spotify_client_secret
        playlist

    Twitter API Keys and Access tokens via https://developer.twitter.com/en/

        APP_KEY
        APP_SECRET
        ACCESS_TOKEN
        ACCESS_TOKEN_SECRET

4. Set up a virtual environment via the following commands:

    conda create -n twitify-env python=3.7 #(first time only)

    conda activate twitify-env

5. Install the package requirements via the requirements.txt file:

    pip install -r requirements.txt

6. Log into Twitter and Tweet a song @Twitify2335 in the format

    "Artist" // "Songname"

    #> If you do not use this fomrat, Twitify will reply to your tweet

7. Run the script via apps/twitify.py