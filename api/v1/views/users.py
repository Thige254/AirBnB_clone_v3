from flask import Blueprint, jsonify, request
from models import storage
from models.user import User

users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/users', methods=['GET'])
def get_all_users():
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


@users_blueprint.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(user.to_dict())


@users_blueprint.route('/users', methods=['POST'])
def create_user():
    request_data = request.get_json()
    if not request_data:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'email' not in request_data:
        return jsonify({'error': 'Missing email'}), 400
    if 'password' not in request_data:
        return jsonify({'error': 'Missing password'}), 400
    user = User(**request_data)
    storage.save(user)
    return jsonify(user.to_dict()), 201


@users_blueprint.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        return jsonify({'error': 'Not found'}), 404
    request_data = request.get_json()
    if not request_data:
        return jsonify({'error': 'Not a JSON'}), 400
    for key, value in request_data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save(user)
    return jsonify(user.to_dict())


@users_blueprint.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        return jsonify({'error': 'Not found'}), 404
    storage.delete(user)
    return jsonify({}), 200
