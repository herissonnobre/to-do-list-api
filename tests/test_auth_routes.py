"""
Unit tests for authentication routes using pytest.

Fixtures:
    - testing_app: Setup and teardown for Flask application.
    - client: Creates a Flask test client.

Tests:
    - test_register: Valid user registration.
    - test_register_missing_password: Registration with missing password.
    - test_register_missing_email: Registration with missing email.
    - test_register_existing_user: Registration with an existing user.
    - test_login: Valid user login.
    - test_login_invalid_password: Login with invalid password.
    - test_login_invalid_email: Login with an unregistered email.
"""

from typing import Generator, Any

import pytest
from flask import Flask
from flask.testing import FlaskClient

from app.extensions import db
from app.routes import auth_blueprint


@pytest.fixture
def testing_app() -> Generator[Flask, Any, None]:
    """
    Set up and tear down the Flask application for testing.
    """
    flask_testing_app = Flask(__name__)
    flask_testing_app.config['TESTING'] = True
    flask_testing_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    db.init_app(flask_testing_app)
    flask_testing_app.register_blueprint(auth_blueprint)

    with flask_testing_app.app_context():
        db.create_all()
        yield flask_testing_app
        db.drop_all()


@pytest.fixture
def client(testing_app: Flask) -> FlaskClient:
    """
    Create a Flask test client.

    :param testing_app:fixture: The Flask testing application.
    :return: FlaskClient: A test client for the Flask testing application.
    """
    return testing_app.test_client()


def test_register(client: FlaskClient) -> None:
    """
    Test valid user registration.
    """
    response = client.post('/register', json={'email': 'test@example.com', 'password': 'password'})
    json_data = response.get_json()

    assert response.status_code == 201
    assert json_data['message'] == 'User registered successfully'


def test_register_missing_password(client: FlaskClient) -> None:
    """
    Test registration with missing password.
    """
    response = client.post('/register', json={'email': 'test@example.com'})
    json_data = response.get_json()

    assert response.status_code == 400
    assert json_data['message'] == 'Email and password are required'


def test_register_missing_email(client: FlaskClient) -> None:
    """
    Test registration with missing email.
    """
    response = client.post('/register', json={'password': 'password'})
    json_data = response.get_json()

    assert response.status_code == 400
    assert json_data['message'] == 'Email and password are required'


def test_register_existent_user(client: FlaskClient) -> None:
    """
    Test registration with existing user.
    """
    client.post('/register', json={'email': 'test@example.com', 'password': 'password'})
    response = client.post('/register', json={'email': 'test@example.com', 'password': 'password'})
    json_data = response.get_json()

    assert response.status_code == 400
    assert json_data['message'] == 'User already registered'


def test_login(client: FlaskClient) -> None:
    """
    Test valid user login.
    """
    client.post('/register', json={'email': 'test@example.com', 'password': 'password'})
    response = client.post('/login', json={'email': 'test@example.com', 'password': 'password'})
    json_data = response.get_json()

    assert response.status_code == 200
    assert 'token' in json_data


def test_login_invalid_password(client: FlaskClient) -> None:
    """
    Test login with invalid password.
    """
    client.post('/register', json={'email': 'test@example.com', 'password': 'password'})
    response = client.post('/login', json={'email': 'test@example.com', 'password': 'wrong-password'})
    json_data = response.get_json()

    assert response.status_code == 401
    assert json_data['message'] == 'Invalid email or password'


def test_login_invalid_email(client: FlaskClient) -> None:
    """
    Test login with unregistered email.
    """
    response = client.post('/login', json={'email': 'test@example.com', 'password': 'password'})
    json_data = response.get_json()

    assert response.status_code == 401
    assert json_data['message'] == 'Invalid email or password'
