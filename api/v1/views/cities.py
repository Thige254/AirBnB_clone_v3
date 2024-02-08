from flask import Blueprint, jsonify, request
from models import storage
from models.city import City
from models.state import State

cities_blueprint = Blueprint('cities', __name__)


@cities_blueprint.route('/states/<state_id>/cities', methods=['GET'])
def get_all_cities_by_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        return jsonify({'error': 'Not found'}), 404
    cities = storage.all(City).filter(City.state_id == state_id)
    return jsonify([city.to_dict() for city in cities])


@cities_blueprint.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(city.to_dict())


@cities_blueprint.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    request_data = request.get_json()
    if not request_data:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in request_data:
        return jsonify({'error': 'Missing name'}), 400
    state = storage.get(State, state_id)
    if not state:
        return jsonify({'error': 'Not found'}), 404
    city = City(**request_data)
    city.state_id = state_id
    storage.save(city)
    return jsonify(city.to_dict()), 201


@cities_blueprint.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        return jsonify({'error': 'Not found'}), 404
    request_data = request.get_json()
    if not request_data:
        return jsonify({'error': 'Not a JSON'}), 400
    for key, value in request_data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save(city)
    return jsonify(city.to_dict())


@cities_blueprint.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        return jsonify({'error': 'Not found'}), 404
    storage.delete(city)
    return jsonify({}), 200
