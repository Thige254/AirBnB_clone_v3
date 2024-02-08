from flask import Blueprint, jsonify, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User

places_reviews_blueprint = Blueprint('places_reviews', __name__)


@places_reviews_blueprint.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews_by_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        return jsonify({'error': 'Not found'}), 404
    reviews = storage.all(Review).filter(place_id=place_id).values()
    return jsonify([review.to_dict() for review in reviews])


@places_reviews_blueprint.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(review.to_dict())


@places_reviews_blueprint.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    place = storage.get(Place, place_id)
    if not place:
        return jsonify({'error': 'Not found'}), 404
    request_data = request.get_json()
    if not request_data:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'user_id' not in request_data:
        return jsonify({'error': 'Missing user_id'}), 400
    user = storage.get(User, request_data['user_id'])
    if not user:
        return jsonify({'error': 'Not found'}), 404
    if 'text' not in request_data:
        return jsonify({'error': 'Missing text'}), 400
    review = Review(place_id=place_id, user_id=request_data['user_id'], **request_data)
    storage.save(review)
    return jsonify(review.to_dict()), 201


@places_reviews_blueprint.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        return jsonify({'error': 'Not found'}), 404
    request_data = request.get_json()
    if not request_data:
        return jsonify({'error': 'Not a JSON'}), 400
    for key, value in request_data.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, key, value)
    storage.save(review)
    return jsonify(review.to_dict())


@places_reviews_blueprint.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        return jsonify({'error': 'Not found'}), 404
    storage.delete(review)
    return jsonify({}), 200
