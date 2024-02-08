from flask import jsonify
from models import storage


@app_views.route('/stats', methods=['GET'])
def stats():
    """Returns the number of objects of each type as a JSON object."""
    stats = {
        'amenities': storage.count(Amenity),
        'cities': storage.count(City),
        'places': storage.count(Place),
        'reviews': storage.count(Review),
        'states': storage.count(State),
        'users': storage.count(User),
    }
    return jsonify(stats)
