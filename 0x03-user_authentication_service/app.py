#!/usr/bin/env python3	
'''
basic flask app
'''
from flask import Flask, jsonify, request, abort, make_response, redirect
from flask import url_for
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/')
def welcome():
    '''returns a JSON payload of form'''
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    '''register a new user'''
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return jsonify({"message": "email and password required"}), 400

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 201
    except ValueError as e:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    '''handles user sessions'''
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        abort(401)

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    if not session_id:
        abort(401)

    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)
    return response


@app.route('/sessions', methods=['DELETE'])
def logout():
    '''deletes user session and logs them out'''
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)

    AUTH.destroy_session(user.id)
    # response =  make_response(redirect(url_for('welcome')))
    # response.set_cookie("session_id", "", expires=0)
    # response.status_code = 302
    # return response
    return redirect('/')


@app.route('/profile')
def profile():
    '''logs in a user based on the session_id'''
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    return jsonify({"email": f"{user.email}"}), 200


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    '''generate a token '''
    email = request.form.get('email')
    if not email:
        print('Email required')

    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token})
    except NoResultFound:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password():
    '''endpoint for updating user password'''
    email = request.form.get('email')
    new_password = request.form.get('new_password')

    if not email or not new_password:
        return jsonify({'message': 'email, reset_token and password are required'})
    try:
        reset_token = AUTH.get_reset_password_token(email)
    
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        return jsonify ({"message": "Invalid reset token"}), 403


if __name__ == '__main__':
    app.run(host='0.0.0.0', port="5000")
