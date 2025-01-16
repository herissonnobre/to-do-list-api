"""
Unit tests for tasks endpoints using pytest.

Fixtures:
    - app: Sets up and tears down the Flask testing application.
    - client: Creates a test client for the Flask testing application.
    - user: Registers and logs in a user, returning a JWT token.

Tests:
    - test_create_task: Tests creating a new task.
    - test_create_task_unauthenticated: Tests creating a new task without authentication.
    - test_get_tasks: Tests getting all tasks.
    - test_get_tasks_unauthenticated: Tests getting all tasks without authentication.
    - test_get_task_by_id: Tests getting a single task.
    - test_get_task_by_id_unauthenticated: Tests getting a single task without authentication.
    - test_get_task_by_id_not_exist: Tests getting a single task without an existing task with the given ID.
    - test_update_task: Tests updating a single task.
    - test_update_task_unauthenticated: Tests updating a single task without authentication.
    - test_update_task_not_exist: Tests updating a single task without an existing task.
    - test_delete_task: Tests deleting a single task.
    - test_delete_task_unauthenticated: Tests deleting a single task without authentication.
    - test_delete_task_not_exist: Tests deleting a single task without an existing task.
"""

import uuid

import pytest
from flask import Flask

from app.extensions import db
from app.routes import tasks_blueprint, auth_blueprint


@pytest.fixture
def app():
    """
    Set up and tear down the Flask testing application.
    """
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    db.init_app(app)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(tasks_blueprint, url_prefix='/tasks')

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """
    Create a test client for the Flask app.
    """
    return app.test_client()


@pytest.fixture
def user(client):
    """
    Register and log in a user, returning a JWT token.
    """
    client.post('/auth/register', json={'email': 'test@example.com', 'password': 'testpassword'})

    response = client.post('/auth/login', json={'email': 'test@example.com', 'password': 'testpassword'})

    json_data = response.get_json()

    return json_data['token']


def test_create_task(client, user):
    """
    Test creating a new task.
    """
    response = client.post('/tasks/', headers={'Authorization': user}, json={
        'title': 'New Task',
        'description': 'A new task',
    })

    json_data = response.get_json()

    assert response.status_code == 201
    assert json_data['title'] == 'New Task'
    assert json_data['description'] == 'A new task'


def test_create_task_unauthenticated(client):
    """
    Test creating a new task without authentication.
    """
    response = client.post('/tasks/', json={
        'title': 'New Task',
        'description': 'A new task',
    })

    assert response.status_code == 401


def test_get_tasks(client, user):
    """
    Test getting all tasks.
    """
    client.post('/tasks/', headers={'Authorization': user}, json={
        'title': 'New Task 1',
        'description': 'A new task 1',
    })

    client.post('/tasks/', headers={'Authorization': user}, json={
        'title': 'New Task 2',
        'description': 'A new task 2',
    })

    response = client.get('/tasks/', headers={'Authorization': user})
    json_data = response.get_json()

    assert response.status_code == 200
    assert len(json_data) == 2


def test_get_tasks_unauthenticated(client):
    """
    Test getting all tasks without authentication.
    """
    response = client.get('/tasks/')

    assert response.status_code == 401


def test_get_task_by_id(client, user):
    """
    Test getting a single task.
    """
    create_response = client.post('/tasks/', headers={'Authorization': user}, json={
        'title': 'New Task',
        'description': 'A new task',
    })

    task_id = create_response.get_json()['id']

    response = client.get(f'/tasks/{task_id}', headers={'Authorization': user})
    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data['title'] == 'New Task'
    assert json_data['description'] == 'A new task'


def test_get_task_by_id_unauthenticated(client, user):
    """
    Test getting a single task without authentication.
    """
    create_response = client.post('/tasks/', headers={'Authorization': user}, json={
        'title': 'New Task',
        'description': 'A new task',
    })

    task_id = create_response.get_json()['id']

    response = client.get(f'/tasks/{task_id}')

    assert response.status_code == 401


def test_get_task_by_id_not_exist(client, user):
    """
    Test getting a single task without an existing task.
    """
    fake_uuid = uuid.uuid4()

    response = client.get(f'/tasks/{fake_uuid}', headers={'Authorization': user})

    assert response.status_code == 404


def test_update_task(client, user):
    """
    Test updating a single task.
    """
    create_response = client.post('/tasks/', headers={'Authorization': user}, json={
        'title': 'New Task',
        'description': 'A new task',
    })

    task_id = create_response.get_json()['id']

    response = client.put(f'/tasks/{task_id}', headers={'Authorization': user}, json={
        'title': 'Updated Task',
        'description': 'A new task',
    })

    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data['title'] == 'Updated Task'
    assert json_data['description'] == 'A new task'


def test_update_task_unauthenticated(client, user):
    """
    Test updating a single task without authentication.
    """
    create_response = client.post('/tasks/', headers={'Authorization': user}, json={
        'title': 'New Task',
        'description': 'A new task',
    })

    task_id = create_response.get_json()['id']

    response = client.put(f'/tasks/{task_id}', json={
        'title': 'Updated Task',
        'description': 'A new task',
    })

    assert response.status_code == 401


def test_update_task_not_exist(client, user):
    """
    Test updating a single task without an existing task.
    """
    fake_uuid = uuid.uuid4()

    response = client.put(f'/tasks/{fake_uuid}', headers={'Authorization': user}, json={
        'title': 'Updated Task',
        'description': 'A new task',
    })

    assert response.status_code == 404


def test_delete_task(client, user):
    """
    Test deleting a single task.
    """
    create_response = client.post('/tasks/', headers={'Authorization': user}, json={
        'title': 'New Task',
        'description': 'A new task',
    })

    task_id = create_response.get_json()['id']

    response = client.delete(f'/tasks/{task_id}', headers={'Authorization': user})

    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data['message'] == 'Task deleted successfully'


def test_delete_task_unauthenticated(client, user):
    """
    Test deleting a single task without authentication.
    """
    create_response = client.post('/tasks/', headers={'Authorization': user}, json={
        'title': 'New Task',
        'description': 'A new task',
    })

    task_id = create_response.get_json()['id']

    response = client.delete(f'/tasks/{task_id}')

    assert response.status_code == 401


def test_delete_task_not_exist(client, user):
    """
    Test deleting a single task without an existing task.
    """
    fake_uuid = uuid.uuid4()

    response = client.delete(f'/tasks/{fake_uuid}', headers={'Authorization': user})

    assert response.status_code == 404
