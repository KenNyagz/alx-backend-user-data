#!/usr/bin/env python3
'''
module to integrate and test all parts of the app
'''
import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

BASE_URL = 'http://localhost:5000'


def register_user(email: str, password: str) -> None:
    '''test user registration'''
    data = {"email": email, "password": password}
    response = requests.post(f'{BASE_URL}/users', data=data)

    if response.status_code == 201:
        assert response.json() == {'email': email, "message": "user created"}
        print("User registration test passed")
    elif response.status_code == 400:
        assert response.json() == {"message": "email already registered"}
        print("User already registered passed")
    else:
        print("User registration failed")


def log_in_wrong_password(email: str, password: str) -> None:
    '''test for user login with wrong password'''
    data = {"email": email, "password": password}
    response = requests.post(f'{BASE_URL}/sessions', data=data)

    assert response.status_code == 401
    print("Test for wrong password login passed")


def log_in(email: str, password: str) -> str:
    '''testing user login'''
    data = {"email": email, "password": password}
    response = requests.post(f'{BASE_URL}/sessions', data=data)

    assert response.status_code == 200

    session_id = response.cookies.get('session_id')
    assert session_id is not None
    print("Login with correct password passed")

    return session_id


def profile_unlogged() -> None:
    '''test accessing the profile endpoint without being logged in
       - without session ID'''
    url = "{}/profile".format(BASE_URL)
    response = requests.get(url)

    assert response.status_code == 403
    print("Profile unlogged test approved")


def profile_logged(session_id: str) -> None:
    '''Test logged in user'''
    url = "{}/profile".format(BASE_URL)
    cookies = {"session_id": session_id}
    response = requests.get(url, cookies=cookies)

    assert response.status_code == 200

    assert "email" in response.json()
    print("Profile logged test passed")


def log_out(session_id: str) -> None:
    '''test logging out'''
    url = '{}/sessions'.format(BASE_URL)
    cookies = {'session_id': session_id}
    response = requests.delete(url, cookies=cookies)

    assert response.status_code == 200
    print('Logout test passed')


def reset_password_token(email: str) -> str:
    '''test reset password'''
    url = '{}/reset_password'.format(BASE_URL)
    form = {"email": email}
    response = requests.post(url, data=form)

    assert response.status_code == 200
    print('Reset password token test passed')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    '''testing update password'''
    url = '{}/reset_password'.format(BASE_URL)
    form_data = {"email": email, "reset_token": reset_token,
                 "new_password": new_password}
    response = requests.put(url, data=form_data)

    assert response.status_code == 200
    print('Resetting password test passed')


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
