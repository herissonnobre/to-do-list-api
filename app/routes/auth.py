"""
This module provides authentication endpoints for user registration and login

Functions:
    - register(): Registers a new user
    - login(): Logs in a user and returns a JWT token
    - verify_request(): Verifies the JWT token in each request

Decorators:
    - @auth_blueprint.route(): Defines  the routes for registration and login endpoint
    - @auth_blueprint.before_request(): Verifies the JWT token before processing the request
"""
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db
from app.models import User
from app.utils.token import generate_token, verify_token

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/register', methods=['POST'])
def register():
    """
    Registers a new user with the provided credentials

    Request body (JSON):
    - email (str): Email of the new user
    - password (str): Password of the new user

    Returns:
    - JSON: Success or error message
    - HTTP Status Code: 201 (Created) if registration is successful, 400 (Bad Request) if data is missing, 500 (Internal Server Error) if an error occurs while saving the user to the database
    """
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"message": "Email and password are required"}), 400

    hashed_password = generate_password_hash(data['password'])
    new_user = User(email=data['email'], password=hashed_password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return jsonify({"message": f"An error occurred while registering the user: {e}"}), 500


@auth_blueprint.route('/login', methods=['POST'])
def login():
    """
    Logs in a user and returns a JWT token

    Request body (JSON):
    - email (str): Email of the user
    - password (str): Password of the user

    Returns:
    - JSON: Success message with the JWT token or error message
    - HTTP Status Code: 200 (Ok) if login is successful, 400 (Bad Request) if data is missing, 401 (Unauthorized) if the credentials are invalid
    """
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"message": "Email and password are required"}), 400

    user = User.query.filter_by(email=data['email']).first()

    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({"message": "Invalid email or password"}), 401

    token = generate_token(user.id)

    return jsonify({"token": token}), 200


@auth_blueprint.before_request
def verify_request():
    """
    Verifies the JWT token in each request before processing it.

    Returns:
    - None: If the request is for the registration or login routes.
    - JSON: Error message if the JWT token is missing or invalid.
    - HTTP Status Code: 401 (Unauthorized) if the JWT token is missing or invalid.
    """
    if request.endpoint == 'auth.register' or request.endpoint == 'auth.login':
        return None

    token = request.headers.get('Authorization')

    if not token or not verify_token(token):
        return jsonify({"message": "Token is missing or invalid"}), 401
