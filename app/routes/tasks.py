"""
teste
"""
from flask import Blueprint, request, jsonify

from app.extensions import db
from app.models import Task
from app.utils.token import verify_token

tasks_blueprint = Blueprint('tasks', __name__)


@tasks_blueprint.before_request
def before_request():
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({"message": "Token is missing"}), 401
    print(token)
    user_id = verify_token(token)

    if not isinstance(user_id, int):
        return jsonify({"message": user_id}), 401

    request.user_id = user_id


@tasks_blueprint.route('', methods=['POST'])
def create_task():
    data = request.get_json()

    new_task = Task(title=data['title'], description=data['description'], user_id=request.user_id)

    db.session.add(new_task)
    db.session.commit()

    return jsonify(new_task.as_dict()), 201


@tasks_blueprint.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.filter_by(user_id=request.user_id).all()

    return jsonify([task.as_dict() for task in tasks]), 200


@tasks_blueprint.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    data = request.get_json()

    task = Task.query.filter_by(id=id, user_id=request.user_id).first()

    if not task:
        return jsonify({"message": "Task not found"}), 404

    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.completed = data.get('completed', task.completed)

    db.session.commit()

    return jsonify(task.as_dict()), 200


@tasks_blueprint.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.filter_by(id=id, user_id=request.user_id).first()

    if not task:
        return jsonify({"message": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "Task deleted successfully"}), 200
