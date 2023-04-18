from Main.db import db


class Venue(db.Model):
    __tablename__ = 'venue'
    venue_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    place = db.Column(db.String, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    shows = db.relationship('Show', cascade='delete', backref='venue', lazy=True)
    
    # just for testing/debugging purpose; string format of Venue object
    def __str__(self) -> str:
        return f"name: {self.name}, capacity: {self.capacity}, place: {self.place}"

    def __repr__(self) -> str:
        return f"name: {self.name}, capacity: {self.capacity}, place: {self.place}"



class Show(db.Model):
    __tablename__ = 'show'
    show_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    rating = db.Column(db.Float, default=0)
    ticket_price = db.Column(db.Float, nullable=False)
    start_time = db.Column(db.String, nullable=False)
    end_time = db.Column(db.String, nullable=False)
    fill_count = db.Column(db.Integer, default=0)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.venue_id'),
        nullable=False )
    tags = db.relationship('Tags', cascade='delete', backref='show', lazy=True)
    runnings = db.relationship('Running', cascade='delete', backref='show', lazy=True)
    
    # just for testing/debugging purpose; string format of Show object
    def __str__(self) -> str:
        return f"title: {self.title}, description: {self.description}, ticket_price: {self.ticket_price}"

    def __repr__(self) -> str:
        return f"name: {self.title}, capacity: {self.ticket_price}, place: {self.start_time}"

class Tags(db.Model):
    show_id = db.Column(db.Integer, db.ForeignKey("show.show_id"), primary_key=True, nullable=False, unique=False)
    tag = db.Column(db.String,primary_key=True, nullable=False)
    

class Running(db.Model):
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.venue_id'), primary_key=True)
    show_id = db.Column(db.Integer, db.ForeignKey("show.show_id"), primary_key=True, unique=False)
    start_time = db.Column(db.String, nullable=False)
    end_time = db.Column(db.String, nullable=False)


class Bookings(db.Model):
    __tablename__ = 'bookings'
    bid = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer,   db.ForeignKey("user.user_id"), nullable=False, unique=False)
    venue_id = db.Column(db.Integer,   db.ForeignKey("venue.venue_id"), nullable=False, unique=False)
    venue_name= db.Column(db.Integer,   db.ForeignKey("venue.name"), nullable=False, unique=False)
    show_id = db.Column(db.Integer,  db.ForeignKey("show.show_id"), nullable=False, unique=False)
    show_title = db.Column(db.Integer,  db.ForeignKey("show.title"), nullable=False, unique=False)
    num_seats = db.Column(db.Integer, default=1, nullable=False)
    user_rating = db.Column(db.Integer, default=0, nullable=False)


class ShowSearch(db.Model):
    __tablename__ = 'search_show'
    show_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

    def __repr__(self) -> str:
        return f"{self.show_id} and {self.title}"

class SearchCity(db.Model):
    __tablename__ = 'search_city'
    venue_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    place = db.Column(db.String)

    def __repr__(self) -> str:
        return f"{self.venue_id} and {self.name} city: {self.place}"