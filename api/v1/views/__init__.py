from flask import Blueprint
from .index import status
from .cities import cities_blueprint
from .amenities import amenities_blueprint
from .users import users_blueprint

app.register_blueprint(cities_blueprint)
app.register_blueprint(amenities_blueprint)
app.register_blueprint(users_blueprint)

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
