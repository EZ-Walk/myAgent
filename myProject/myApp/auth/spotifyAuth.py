"""
In this file we declare the methods needed for obtaining an authorization from the spotify API
"""
import os
import spotipy
import spotipy.util as util
import datetime as dt


# Set some environemnt variable used by the spotipy authenticator
# TODO: Pull these from an encrypted DB
os.environ['SPOTIPY_CLIENT_ID']='411ed1fc291749ccaf9523138836a2dd'
os.environ['SPOTIPY_CLIENT_SECRET']='d5597fa540c84aa9ade5859bba91b681'
os.environ['REDIRECT_URI']='http://trythis/callback'

# scopes to request from the API
# TODO: Determine which scopes are required by the request
scopes = 'user-read-currently-playing user-library-read playlist-modify-public'

# Declared variables that will be passed eventually
# TODO: This will be used to access the env variables
username = 'wakerxd'

# TODO: collect the token and return an authenticated Spotipy client
def request_token():
    try:
        token = util.prompt_for_user_token(
            username=username,
            scope=scopes,
            client_id=os.environ['SPOTIPY_CLIENT_ID'],
            client_secret=os.environ['SPOTIPY_CLIENT_SECRET'],
            redirect_uri='http://trythis/callback')
        
    except Exception as e:
        print('Unable to request token from spotify. Error: ', e)
        return 500

    if token:
        apiAgent = spotipy.Spotify(auth=token)
        print('Agent authenticated. Continuing...')
        return apiAgent
    else:
        return

