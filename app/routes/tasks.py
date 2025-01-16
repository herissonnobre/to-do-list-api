"""
Task management routes using Flask and SQLAlchemy.

Functions:
    - create_task(): Creates a new task.
    - get_tasks(): Returns all tasks for the authenticated user.
    - get_task_by_id(task_id): Returns the task with the given ID.
    - update_task(): Updates the task with the given ID.
    - delete_task(): Deletes the task with the given ID.

Decorators:
    - before_request(): Verifies the JWT token before each request.
"""
import uuid

from flask import Blueprint, request, jsonify

from app.extensions import db
from app.models import Task
from app.utils.token import verify_token

tasks_blueprint = Blueprint('tasks', __name__)


@tasks_blueprint.before_request
def before_request():
    """
    Verify the JWT token before each request.

    Returns:
        - JSON: Error message if token is missing or invalid.
        - HTTP Status Code: 401 (Unauthorized).
    """
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({"message": "Token is missing"}), 401

    user_id = verify_token(token)

    user_id_uuid = uuid.UUID(user_id)

    if not (user_id or str(user_id_uuid) == user_id):
        return jsonify({"message": "An error occurred while authenticating the user token"}), 401

    request.user_id = user_id_uuid


@tasks_blueprint.route('/', methods=['POST'])
def create_task():
    """
    Create a new task for the authenticated user.

    Request bodu (JSON):
        - title (str): The title of the task.
        - description (str): The description of the task.

    Returns:
        - JSON: The created task details.
        - HTTP Status Code: 201 (Created).
    """
    data = request.get_json()

    new_task = Task(title=data['title'], description=data['description'], user_id=request.user_id)

    db.session.add(new_task)
    db.session.commit()

    return jsonify(new_task.as_dict()), 201


@tasks_blueprint.route('/', methods=['GET'])
def get_tasks():
    """
    Retrieve all tasks for the authenticated user.

    Returns:
        - JSON: The retrieved tasks.
        - HTTP Status Code: 200 (OK).
    """
    tasks = Task.query.filter_by(user_id=request.user_id).all()

    return jsonify([task.as_dict() for task in tasks]), 200


@tasks_blueprint.route('/<task_id>', methods=['GET'])
def get_task_by_id(task_id):
    """
    Retrieve a specific task by ID for the authenticated user.

    Parameters:
        - task_id (str): The ID of the task to retrieve.

    Returns:
        - JSON: The task details or an error message.
        - HTTP Status Code: 200 (OK), 404 (Not Found).
    """
    task = Task.query.filter_by(id=uuid.UUID(task_id), user_id=request.user_id).first()

    if task is None:
        return jsonify({"message": "Task not found"}), 404

    return jsonify(task.as_dict()), 200


@tasks_blueprint.route('/<task_id>', methods=['PUT'])
def update_task(task_id):
    """
    Update a specific task by ID for the authenticated user.

    Parameters:
        - task_id (str): The ID of the task to update.

    Request bodu (JSON):
        - title (str, optional): The title of the task.
        - description (str, optional): The description of the task.
        - completed (bool, optional): Whether the task is completed.

    Returns:
        - JSON: The updated task details or an error message.
        - HTTP Status Code: 200 (OK), 404 (Not Found).
    """
    data = request.get_json()

    task = Task.query.filter_by(id=uuid.UUID(task_id), user_id=request.user_id).first()

    if not task:
        return jsonify({"message": "Task not found"}), 404

    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.completed = data.get('completed', task.completed)

    db.session.commit()

    return jsonify(task.as_dict()), 200


@tasks_blueprint.route('/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    Delete a specific task by ID for the authenticated user.

    Parameters:
        - task_id (str): The ID of the task to delete.

    Returns:
        - JSON: The deleted task details or an error message.
        - HTTP Status Code: 200 (OK), 404 (Not Found).
    """
    task = Task.query.filter_by(id=uuid.UUID(task_id), user_id=request.user_id).first()

    if not task:
        return jsonify({"message": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "Task deleted successfully"}), 200
