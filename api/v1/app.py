from flask import Flask, Blueprint, request, jsonify, make_response
from os import environ
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Enable CORS for all origins.using asterisk
# FOR DEVELOPMENT ONLY...DURING PRODUCTION I WILL NEED TO UPDATE WITH SPECIFI ORIGINS
cors = CORS(app, origins=["*"])

app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    """Handles 404 errors and returns a JSON response."""
    response = jsonify({"error": "Not found"})
    response.status_code = 404
    return response


@app.teardown_appcontext
def teardown_db(error):
    storage.close()


if __name__ == "__main__":
    host = environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(environ.get('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
