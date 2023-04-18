from flask_restful import Api
from flask import current_app as app
from .api import ShowAPI, VenueAPI

from flask_cors import CORS
cors = CORS(app)
api = Api(app)
app.app_context().push()


api.add_resource(VenueAPI, '/api/v1/venue', '/api/v1/venue/<int:venue_id>')
api.add_resource(ShowAPI, '/api/v1/show', '/api/v1/show/<int:show_id>' )
