"""
In this file we declare the methods needed for obtaining an authorization from the spotify API
"""
import os
import spotipy
import spotipy.util as util
import datetime as dt


# Set some environemnt variable used by the spotipy authenticator
os.environ['SPOTIPY_CLIENT_ID']='411ed1fc291749ccaf9523138836a2dd'
os.environ['SPOTIPY_CLIENT_SECRET']='d5597fa540c84aa9ade5859bba91b681'
os.environ['REDIRECT_URI']='http://trythis/callback'

# scopes to request from the API
scopes = 'user-read-currently-playing user-library-read playlist-modify-public'

# Declared variables that will be passed eventually
username = 'wakerxd'

def request_token(username,clinetID,clientSecret):
    try:
        token = util.prompt_for_user_token(username, scope=scopes, client_id=clinetID, client_secret=clientSecret, redirect_uri='http://trythis/callback')
    except Exception as e:
        print('Unable to request token from spotify. Error: ', e)

    if token:
        apiAgent = spotipy.Spotify(auth=token)
        print('Agent authenticated. Continuing...')
    else:
        return

