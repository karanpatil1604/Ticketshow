from flask_restful import Resource, Api
from flask_restful import marshal_with, Resource, fields, reqparse
from Main.db import db
from flask import current_app as app

# ============================= CUSTOM VALIDATIONS ===========================================
from werkzeug.exceptions import HTTPException
from flask import make_response
import json


class NotFoundError(HTTPException):
    def __init__(self, status_code):
        self.response = make_response("", status_code)

class BusinessValidationError(HTTPException):
    def __init__(self, status_code, error_code, error_message):
        res = {"error_code": error_code, "error_message":error_message}
        self.response = make_response(json.dumps(res), status_code)
# -------------------------------------------------------------------------------------------------


from app_show_manager.models import Venue, Show, ShowSearch, SearchCity



output_fields = {
            "venue_id": fields.Integer,
            "name": fields.String,
            "place": fields.String,
            "capacity": fields.Integer

}
create_venue_parser = reqparse.RequestParser()
create_venue_parser.add_argument('venue_id')
create_venue_parser.add_argument('name')
create_venue_parser.add_argument('place')
create_venue_parser.add_argument('capacity')

class VenueAPI(Resource):
    @marshal_with(output_fields)
    def get(self, venue_id):
        venue = Venue.query.filter(Venue.venue_id == venue_id).first()
        if venue is not None:
            return venue
        else:
            raise NotFoundError(status_code=404)

    @marshal_with(output_fields)
    def put(self, venue_id):
        venue = Venue.query.filter(Venue.venue_id == venue_id).first()
        if venue is None:
            raise NotFoundError(status_code=404)
        args = create_venue_parser.parse_args()
        vname = args.get('name', None)
        city = args.get('place', None)
        capacity = args.get('capacity')

        
        if vname is None:
            raise BusinessValidationError(status_code=400, error_code='NAME', error_message='Venue Name is required')
        if city is None:
            raise BusinessValidationError(status_code=400, error_code='PLACE', error_message='City Name is required')
        if capacity is None:
            raise BusinessValidationError(status_code=400, error_code='CAPACITY', error_message='Capacity is required')
            

        try:
            if venue is not None:
                venue.name = vname
                venue.place = city
                venue.capacity = capacity
                db.session.commit()
            search_city = SearchCity.query.filter(SearchCity.venue_id==venue_id).first()
            if search_city:
                db.session.delete(search_city)
                db.session.commit()
            new_search_city = SearchCity(venue_id=venue_id, name=vname, place=city)
            db.session.add(new_search_city)
            db.session.commit()
        except:
            return NotFoundError(status_code=500)
        else:
            return venue, 200

    def delete(self, venue_id):
        venue = Venue.query.filter(Venue.venue_id == venue_id).first()
        shows = venue.shows
        if venue is None:
            raise NotFoundError(status_code=404)
        try:
            db.session.delete(venue)
            db.session.commit()
            # for s in shows:
            #     db.session.delete(s)
            #     db.session.commit()
            search_city = SearchCity.query.filter(SearchCity.venue_id==venue_id).first()
            if search_city:
                db.session.delete(search_city)
                db.session.commit()
        except:
            raise NotFoundError(status_code=500)
        else:
            return "", 200

    @marshal_with(output_fields)
    def post(self):
        args = create_venue_parser.parse_args()
        vname = args.get('name', None)
        place = args.get('place', None)
        capacity = args.get('capacity', None)
        if vname is None:
            raise BusinessValidationError(status_code=400, error_code="NAME", error_message="Venue Name required")
        if place is None:
            raise BusinessValidationError(status_code=400, error_code="PLACE", error_message="Place is required")
        if capacity is None:
            raise BusinessValidationError(status_code=400, error_code='CAPACITY', error_message='Capacity is required')
            
        try:
            new_venue = Venue(name=vname, place=place, capacity=capacity)
            db.session.add(new_venue)
            db.session.commit()
            new_search_city = SearchCity(venue_id=new_venue.venue_id, name=vname, place=place)
            db.session.add(new_search_city)
            db.session.commit()
            
        except:
            raise NotFoundError(status_code=409)
        else:
            return new_venue, 201

# <-------------------------------------- VenueAPI ends here ---------------------------------->
# ------------------------------------------------------------------------------------------------------

# <-------------------------------------- ShowAPI starts here ---------------------------------->
show_output_fields = {
    "show_id": fields.Integer,
            "title": fields.String,
            "description": fields.String,
            "start_time": fields.String,
            "end_time": fields.String,
            "ticket_price": fields.Integer,
            "venue_id": fields.Integer

}
create_show_parser = reqparse.RequestParser()
create_show_parser.add_argument('title')
create_show_parser.add_argument('description')
create_show_parser.add_argument('start_time')
create_show_parser.add_argument('end_time')
create_show_parser.add_argument('ticket_price')
create_show_parser.add_argument('venue_id')



class ShowAPI(Resource):
    @marshal_with(show_output_fields)
    def get(self, show_id):
        show = Show.query.filter(Show.show_id == show_id).first()
        if show is not None:
            return show
        else:
            raise NotFoundError(status_code=404)

    @marshal_with(show_output_fields)
    def put(self, show_id):
        show = Show.query.filter(Show.show_id == show_id).first()
        if show is None:
            return NotFoundError(status_code=404)
        args = create_show_parser.parse_args()
        stitle = args.get('title', None)
        desc = args.get('description', None)
        start_t = args.get('start_time', None)
        end_t = args.get('end_time', None)
        ticket_price = args.get('ticket_price', None)
        venue_id = args.get('venue_id', None)

        if stitle is None:
            raise BusinessValidationError(status_code=400, error_code='SHOQ001', error_message='Show title is required')
        if start_t is None:
            raise BusinessValidationError(status_code=400, error_code='SHOW002', error_message='Show start Time is required')
        if end_t is None:
            raise BusinessValidationError(status_code=400, error_code='SHOW003', error_message='Show end Time is required')
        if ticket_price is None:
            raise BusinessValidationError(status_code=400, error_code='SHOW004', error_message='Ticket Price is required')
        if ticket_price is None:
            
            raise BusinessValidationError(status_code=400, error_code='SHOW005', error_message='Venue ID for show is required')

        try:
            show.title = stitle
            show.description = desc
            show.start_time = start_t
            show.end_time = end_t
            show.ticket_price = ticket_price
            show.venue_id = venue_id
            db.session.commit()
            show_search = ShowSearch.query.filter(ShowSearch.show_id==show_id).first()
            if show_search:
                db.session.delete(show_search)
                db.session.commit()
            new_show_search = ShowSearch(show_id=show_id, title=stitle)
            db.session.add(new_show_search)
            db.session.commit()
        except:
            return NotFoundError(status_code=500)
        else:
            return show, 200

    def delete(self, show_id):
        show = Show.query.filter(Show.show_id == show_id).first()
        if show is None:
            raise NotFoundError(status_code=404)
        try:
            db.session.delete(show)
            db.session.commit()
            show_search = ShowSearch.query.filter(ShowSearch.show_id==show_id).first()
            if show_search:
                db.session.delete(show_search)
                db.session.commit()
        except:
            raise NotFoundError(status_code=500)
        else:
            return "", 200

    @marshal_with(show_output_fields)
    def post(self):
        args = create_show_parser.parse_args()
        stitle = args.get('title', None)
        desc = args.get('description', None)
        start_t = args.get('start_time', None)
        end_t = args.get('end_time', None)
        ticket_price = args.get('ticket_price', None)
        venue_id = args.get('venue_id', None)
        if stitle is None:
            raise BusinessValidationError(status_code=400, error_code='show001', error_message='Show Title is required')

        if start_t is None:
            raise BusinessValidationError(status_code=400, error_code='SHOW002', error_message='Show start Time is required')
        if end_t is None:
            raise BusinessValidationError(status_code=400, error_code='SHOW003', error_message='Show end Time is required')
        if ticket_price is None:
            raise BusinessValidationError(status_code=400, error_code='SHOW004', error_message='Ticket Price is required')
        if ticket_price is None:
            raise BusinessValidationError(status_code=400, error_code="SHOW005", error_message="Venue Id for show is required")


        try:
            new_show = Show(title=stitle, description=desc, ticket_price=ticket_price, venue_id=venue_id,
                                start_time=start_t, end_time=end_t)
            db.session.add(new_show)
            db.session.commit()
            new_show_search = ShowSearch(show_id=new_show.show_id, title=stitle)
            db.session.add(new_show_search)
            db.session.commit()
        except:
            raise NotFoundError(status_code=409)
        else:
            return new_show, 201



