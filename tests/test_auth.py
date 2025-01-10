"""
test
"""
import pytest
from flask import Flask

from app.extensions import db
from app.routes import auth_blueprint


@pytest.fixture
def testing_app():
    """
    test
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
def client(testing_app):
    """

    :param testing_app:
    :return:
    """
    return testing_app.test_client()


def test_register(client):
    response = client.post('/register', json={'email': 'test@example.com', 'password': 'testpassword'})
    json_data = response.get_json()

    assert response.status_code == 201
    assert json_data['message'] == 'User registered successfully'


def test_register_missing_fields(client):
    response = client.post('/register', json={'email': 'test@example.com'})
    json_data = response.get_json()

    assert response.status_code == 400
    assert json_data['message'] == 'Email and password are required'


def test_login(client):
    client.post('/register', json={'email': 'test@example.com', 'password': 'testpassword'})
    response = client.post('/login', json={'email': 'test@example.com', 'password': 'testpassword'})
    json_data = response.get_json()

    assert response.status_code == 200
    assert 'token' in json_data
