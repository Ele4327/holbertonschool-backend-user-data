#!/usr/bin/env python3
"""
    Route Module
"""

from flask import Flask, jsonify, request,  abort, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def status() -> str:
    """
        GET route ("/") and use flask.jsonify
        to return a JSON payload of the form
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def new_user() -> str:
    """
        POST route ("/users")
        return JSON payload
    """
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        new_user = AUTH.register_user(email, password)
        if new_user is not None:
            return jsonify({
                "email": new_user.email,
                "message": "user created"
            })
    except ValueError:
        return jsonify({
            "message": "email already registered"
            }), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """
        POST route ("/sessions")
        Create user and store as a cookie.
        Returns JSON payload
    """
    email = request.form.get("email")
    password = request.form.get("password")
    valid_user = AUTH.valid_login(email, password)

    if not valid_user:
        abort(401)
    session_id = AUTH.create_session(email)
    message = {"email": email, "message": "logged in"}
    response = jsonify(message)
    response.set_cookie("session_id", session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """
        DELETE route ("/sessions")
        Destroy the session
        Returns a redirect user to GET session
    """
    user_cookie = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(user_cookie)
    if user_cookie is None or user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """
        GET route ("/profile")
        Returns:
            session_id: session
            or 403 if session is not found or invalid
    """
    user_cookie = request.cookies.get("session_id", None)
    if user_cookie is None:
        abort(403)
    user = AUTH.get_user_from_session_id(user_cookie)
    if user is None:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """
        POST route ("/reset_password")
        Returns:
            A token generated
            or 403 if is not allowed or registered email
    """
    user_request = request.form
    user_email = user_request.get('email')
    is_registered = AUTH.create_session(user_email)

    if not is_registered:
        abort(403)

    token = AUTH.get_reset_password_token(user_email)
    message = {"email": user_email, "reset_token": token}
    return jsonify(message)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """
        PUT route ("/reset_password")
        Returns:
            Updated password
            or 403 if is not token valid
    """
    user_email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    try:
        AUTH.update_password(reset_token, new_password)
    except Exception:
        abort(403)

    message = {"email": user_email, "message": "Password updated"}
    return jsonify(message), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
