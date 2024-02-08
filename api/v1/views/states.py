from flask import Blueprint, jsonify, request
from models import storage
from models.state import State

states_blueprint = Blueprint('states', __name__)


@states_blueprint.route('/states', methods=['GET'])
def get_all_states():
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@states_blueprint.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(state.to_dict())


@states_blueprint.route('/states', methods=['POST'])
def create_state():
    request_data = request.get_json()
    if not request_data:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in request_data:
        return jsonify({'error': 'Missing name'}), 400
    state = State(**request_data)
    storage.save(state)
    return jsonify(state.to_dict()), 201


@states_blueprint.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        return jsonify({'error': 'Not found'}), 404
    request_data = request.get_json()
    if not request_data:
        return jsonify({'error': 'Not a JSON'}), 400
    for key, value in request_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save(state)
    return jsonify(state.to_dict())


@states_blueprint.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        return jsonify({'error': 'Not found'}), 404
    storage.delete(state)
    return jsonify({}), 200
