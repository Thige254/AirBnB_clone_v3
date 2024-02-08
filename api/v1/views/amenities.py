from flask import Blueprint, jsonify, request
from models import storage
from models.amenity import Amenity

amenities_blueprint = Blueprint('amenities', __name__)


@amenities_blueprint.route('/amenities', methods=['GET'])
def get_all_amenities():
    amenities = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in amenities])


@amenities_blueprint.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(amenity.to_dict())


@amenities_blueprint.route('/amenities', methods=['POST'])
def create_amenity():
    request_data = request.get_json()
    if not request_data:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in request_data:
        return jsonify({'error': 'Missing name'}), 400
    amenity = Amenity(**request_data)
    storage.save(amenity)
    return jsonify(amenity.to_dict()), 201


@amenities_blueprint.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        return jsonify({'error': 'Not found'}), 404
    request_data = request.get_json()
    if not request_data:
        return jsonify({'error': 'Not a JSON'}), 400
    for key, value in request_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    storage.save(amenity)
    return jsonify(amenity.to_dict())


@amenities_blueprint.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        return jsonify({'error': 'Not found'}), 404
    storage.delete(amenity)
    return jsonify({}), 200
