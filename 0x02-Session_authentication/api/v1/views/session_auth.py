#!/usr/bin/env python3
'''
view for all routes for session authenticaation
'''
from flask import request, jsonify, abort
from api.v1.views import app_views
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    '''view for authorised user with valid session'''
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or len(email) == 0:
        return jsonify({"error": "email missing"}), 400

    if not password or len(password) == 0:
        return jsonify({"error": "password missing"}), 400

    users = User.search({'email': email})
    if not users or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({'error': 'wrong password'}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())

    session_name = os.getenv('SESSION_NAME', '_my_session_id')
    response.set_cookie(session_name, session_id)

    return response


@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    '''Deleting session and logging out user'''
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
