from flask import Blueprint, jsonify, request
from models import storage
from models.place import Place
from models.city import City
from models.amenity import Amenity

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


# Additional route for searching places
@places_blueprint.route('/places_search', methods=['POST'])
def search_places():
    request_data = request.get_json()
    if not request_data:
        return jsonify({'error': 'Not a JSON'}), 400

    states = request_data.get('states', [])
    cities = request_data.get('cities', [])
    amenities = request_data.get('amenities', [])

    places = storage.all(Place)

    # Filter by states
    if states:
        state_ids = [state_id for state_id in states if storage.get(State, state_id)]
        cities_in_states = storage.all(City).filter(state_id__in=state_ids).values_list('id', flat=True)
        places = places.filter(city_id__in=cities_in_states)

    # Filter by cities
    if cities:
        city_ids = [city_id for city_id in cities if storage.get(City, city_id)]
        places = places.filter(city_id__in=city_ids)

    # Filter by amenities (exclusive)
    if amenities:
        amenity_ids = [amenity_id for amenity_id in amenities if storage.get(Amenity, amenity_id)]
        place_ids = storage.all(Place.amenities).filter(amenity_id__in=amenity_ids).values_list('place_id', flat=True)
        places = places.filter(id__in=place_ids)

    return jsonify([place.to_dict() for place in places])
