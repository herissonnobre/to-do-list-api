"""
teste
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

    :return:
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

    :return:
    """
    data = request.get_json()

    new_task = Task(title=data['title'], description=data['description'], user_id=request.user_id)

    db.session.add(new_task)
    db.session.commit()

    return jsonify(new_task.as_dict()), 201


@tasks_blueprint.route('/', methods=['GET'])
def get_tasks():
    """

    :return:
    """
    tasks = Task.query.filter_by(user_id=request.user_id).all()

    return jsonify([task.as_dict() for task in tasks]), 200


@tasks_blueprint.route('/<task_id>', methods=['GET'])
def get_task_by_id(task_id):
    """

    :param task_id:
    :return:
    """
    task = Task.query.filter_by(id=uuid.UUID(task_id), user_id=request.user_id).first()

    if task is None:
        return jsonify({"message": "Task not found"}), 404

    return jsonify(task.as_dict()), 200


@tasks_blueprint.route('/<task_id>', methods=['PUT'])
def update_task(task_id):
    """

    :param task_id:
    :return:
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

    :param task_id:
    :return:
    """
    task = Task.query.filter_by(id=uuid.UUID(task_id), user_id=request.user_id).first()

    if not task:
        return jsonify({"message": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "Task deleted successfully"}), 200
