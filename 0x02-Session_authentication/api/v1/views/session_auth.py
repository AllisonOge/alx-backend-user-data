#!/usr/bin/env python3
"""
Handles all routes for the Session Authentication
"""
from os import getenv
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """login with session authentication"""
    email = request.form.get("email")
    password = request.form.get("password")

    if not email:
        return jsonify({'error': 'email is missing'}), 400
    if not password:
        return jsonify({'error': 'password missing'}), 400
    searches = User.search(dict(email=email))
    if len(searches) == 0:
        return jsonify({'error': 'no user found for this email'}), 404
    user = searches[0]
    if not user.is_valid_password(password):
        return jsonify({'error': 'wrong password'}), 401
    # create a session id for user
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    session_key = getenv("SESSION_NAME", '_my_session_id')
    response = jsonify(user.to_json())
    response.set_cookie(session_key, session_id)
    return response


@app_views.route('/auth_session/logout',
                 methods=["DELETE"], strict_slashes=False)
def logout():
    """logout session authentication"""
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    else:
        return jsonify({}), 200
