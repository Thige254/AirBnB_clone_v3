from flask import Blueprint, jsonify, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User

places_blueprint = Blueprint('places', __name__)


@places_blueprint.route('/cities/<city_id>/places', methods=['GET'])
def get_places_by_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        return jsonify({'error': 'Not found'}), 404
    places = storage.all(Place).filter(city_id=city_id).values()
    return jsonify([place.to_dict() for place in places])


@places_blueprint.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(place.to_dict())


@places_blueprint.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    city = storage.get(City, city_id)
    if not city:
        return jsonify({'error': 'Not found'}), 404
    request_data = request.get_json()
    if not request_data:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'user_id' not in request_data:
        return jsonify({'error': 'Missing user_id'}), 400
    user = storage.get(User, request_data['user_id'])
    if not user:
        return jsonify({'error': 'Not found'}), 404
    if 'name' not in request_data:
        return jsonify({'error': 'Missing name'}), 400
    place = Place(city_id=city_id, user_id=request_data['user_id'], **request_data)
    storage.save(place)
    return jsonify(place.to_dict()), 201


@places_blueprint.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        return jsonify({'error': 'Not found'}), 404
    request_data = request.get_json()
    if not request_data:
        return jsonify({'error': 'Not a JSON'}), 400
    for key, value in request_data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save(place)
    return jsonify(place.to_dict())


@places_blueprint.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        return jsonify({'error': 'Not found'}), 404
    storage.delete(place)
    return jsonify({}), 200
