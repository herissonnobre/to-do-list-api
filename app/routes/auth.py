"""
Authentication endpoints for user registration and login.

Functions:
    - register(): Registers a new user.
    - login(): Logs in a user and returns a JWT token.

Decorators:
    - @auth_blueprint.route(): Defines routes for registration and login.
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
    Registers a new user.

    Request body (JSON):
    - email (str): User's email.
    - password (str): User's password.

    Returns:
    - JSON: Success or error message.
    - Status Code: 201 (Created), 400 (Bad Request), 500 (Internal Server Error).
    """
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"message": "Email and password are required"}), 400

    if db.session.query(User).filter_by(email=data.get('email')).first():
        return jsonify({"message": "User already registered"}), 400

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
    Logs in a user and returns a JWT token.

    Request body (JSON):
    - email (str): User's email.
    - password (str): User's password.

    Returns:
    - JSON: Success message with the JWT token or error message.
    - Status Code: 200 (OK), 400 (Bad Request), 401 (Unauthorized).
    """
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"message": "Email and password are required"}), 400

    user = User.query.filter_by(email=data['email']).first()

    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({"message": "Invalid email or password"}), 401

    token = generate_token(user.id)

    return jsonify({"token": token}), 200
