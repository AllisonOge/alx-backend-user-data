#!/usr/bin/env python3
"""app.py"""
from flask import Flask, jsonify, request
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def root():
    """index"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def register_user():
    """register a user"""
    email = request.form.get("email")
    passwd = request.form.get("password")
    if email is None or passwd is None:
        return

    try:
        user = AUTH.register_user(email, passwd)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify(
            {"email": email, "message": "user created"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
