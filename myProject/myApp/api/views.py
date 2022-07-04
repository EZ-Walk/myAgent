# from msilib.schema import Error
from os import stat
from flask import Blueprint, current_app, jsonify
from flask.globals import request
from flask_restful import Api
from itsdangerous import json
from marshmallow import ValidationError
from myApp.extensions import apispec
from myApp.api.resources import UserResource, UserList
from myApp.api.schemas import UserSchema

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(blueprint)


api.add_resource(UserResource, "/users/<int:user_id>", endpoint="user_by_id")
api.add_resource(UserList, "/users", endpoint="users")


@blueprint.before_app_first_request
def register_views():
    apispec.spec.components.schema("UserSchema", schema=UserSchema)
    apispec.spec.path(view=UserResource, app=current_app)
    apispec.spec.path(view=UserList, app=current_app)


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    """Return json error for marshmallow validation errors.

    This will avoid having to try/catch ValidationErrors in all endpoints, returning
    correct JSON response with associated HTTP 400 Status (https://tools.ietf.org/html/rfc7231#section-6.5.1)
    """
    return jsonify(e.messages), 400

@blueprint.route('/test', methods=['GET'])
def test_route():
    print('Testing...')
    print('Request is json: ', request.is_json)
    print([i for i in request.form.items()])
    print('Done')
    return jsonify(dict(status=200, message='check logs for form data'))


@blueprint.route('/clone', methods=['POST'])
def clone_playlist():
    """_summary_
    This is the OG function. Takes a URL of a playlist to copy and a name to give the copy. 
    
    Requires:
    Auth token to use the spotipy API.

    Returns:
        _type_: _description_
    """

    req_data = request.form # unload the request data into a convenient variable

    # Collect the necessary attributes of the request and validate them
    name = req_data.get('name')
    url = req_data.get('url')
    
    if name and url: # True: necessary request elements are present
        print('Required parameters received. Creating "{}"...'.format(name))
        #TODO: get an authenticated apiAgent from myApp/auth/spotifyAuth.py
        try:
            import myApp.auth.spotifyAuth as auth
            sp = auth.request_token()
            
        except Exception as e:
            print(e)
            print('aaaaaaahh, couldnt get an agent to do our bidding')
            return response(500, 'Failed to acquire authenticated agent.')
        
        # Alright fuck it im just gonna do the whole clone function in one view
        # TODO: Make this pretty jajajajajaj
        # this should start by getting the playlist's track's URIs with the endpoint below and saving that list of track_uris
        # GET https://api.spotify.com/v1/playlists/{playlist_id}/tracks
        # https://open.spotify.com/playlist/37i9dQZF1E37JNnK3FvjlV?si=m-9df_-HQlqrYHtfvx3NXA
        contents = []
        try:
            pID = url.split('/')[-1].split('?')[0]
            print('Looking for playlist with ID: "{}"'.format(pID))
            daily1Tracks = sp.playlist(pID, fields=['tracks'])

        except Exception as e:
            print('Error finding the playilist with the link: {}\nplaylist ID: "{}"'.format(url, pID))
            return response(500, "Couldn't find a playlist with the link provided.")
        
        for t in daily1Tracks['tracks']['items']: # Traverse to the 
            contents.append(t['track']['external_urls']['spotify'])
        # == contents is now a populated list of 50 track URIs. Done

        # Create a new playlist named SavedDaily{N} or something like that. Use this endpoint to create a playlist
        # POST https://api.spotify.com/v1/users/{user_id}/playlists
        import datetime as dt
        g = 1
        newSavedName = u'{}'.format(name)
        savedFromName = sp.playlist(url)['name']
        date = dt.date.today().strftime('%B %d, %Y') # Date like: June 30, 2022
        creationResp = sp.user_playlist_create('wakerXD', newSavedName, description='A snapshot of {} from {}'.format(savedFromName, date))
        savedDailyID = creationResp['id']

        # Next it should take this list of tracks found in the targeted DailyMix and add them to SavedDaily{N} with this endpoint
        # POST https://api.spotify.com/v1/playlists/{playlist_id}/tracks
        # This takes in a list of URIs to add
        sp.user_playlist_add_tracks('wakerXD', savedDailyID, contents)
            
        return response(200, 'Playlist named "{}" is going to be created!'.format(name))
    else:
        return response(400, 'Invalid parameters passed to /clone.')
    # ==


def response(code, message):
    return jsonify(dict(status=code, message=message))