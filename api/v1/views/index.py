from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    """Returns the API status as a JSON object."""
    return jsonify({'status': 'OK'})
