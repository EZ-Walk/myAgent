from flask import Blueprint, current_app, jsonify
from flask.globals import request
from flask_restful import Api
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
    print([i for i in request.form.items()])
    print('Done')
    return jsonify(dict(status=200, message='check logs for form data'))

@blueprint.route('clone', methods=['POST'])
def clone_playlist():
    req_data = request.form

    name = req_data.get('name')
    url = req_data.get('url')

    if name and url:
        pass
    else:
        pass

    return
