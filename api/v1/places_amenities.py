from flask import Blueprint, jsonify, request
from models import storage
from models.place import Place
from models.amenity import Amenity

places_amenities_blueprint = Blueprint('places_amenities', __name__)


@places_amenities_blueprint.route('/places/<place_id>/amenities', methods=['GET'])
def get_amenities_by_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        return jsonify({'error': 'Not found'}), 404
    if models.storage_t == 'db':
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = [storage.get(Amenity, amenity_id).to_dict()
                     for amenity_id in place.amenity_ids]
    return jsonify(amenities)


@places_amenities_blueprint.route('/places/<place_id>/amenities/<amenity_id>',
                                  methods=['DELETE'])
def delete_amenity_from_place(place_id, amenity_id):
    place = storage.get(Place, place_id)
    if not place:
        return jsonify({'error': 'Not found'}), 404
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        return jsonify({'error': 'Not found'}), 404
    if models.storage_t == 'db':
        if amenity not in place.amenities:
            return jsonify({'error': 'Not found'}), 404
        place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            return jsonify({'error': 'Not found'}), 404
        place.amenity_ids.remove(amenity_id)
    storage.save()
    return jsonify({}), 200


@places_amenities_blueprint.route('/places/<place_id>/amenities/<amenity_id>',
                                  methods=['POST'])
def link_amenity_to_place(place_id, amenity_id):
    place = storage.get(Place, place_id)
    if not place:
        return jsonify({'error': 'Not found'}), 404
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        return jsonify({'error': 'Not found'}), 404
    if models.storage_t == 'db':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity_id)
    storage.save()
    return jsonify(amenity.to_dict()), 201
