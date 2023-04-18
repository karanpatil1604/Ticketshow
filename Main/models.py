# from .db import db

# class User(db.Model):
#     __tablename__ = 'user'
#     user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     username= db.Column(db.String, unique=True, nullable=False)
#     password = db.Column(db.String, nullable=False)
#     email = db.Column(db.String, unique=True, nullable=False)
#     mobile = db.Column(db.String)

#     bookings = db.relationship('Bookings', backref='user', lazy=True)
    
# class Venue(db.Model):
#     __tablename__ = 'venue'
#     venue_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     name = db.Column(db.String, nullable=False)
#     place = db.Column(db.String, nullable=False)
#     capacity = db.Column(db.Integer, nullable=False)
#     shows = db.relationship('Show', backref='venue', lazy=True)
    
#     # just for testing/debugging purpose; string format of User object
#     def __str__(self) -> str:
#         return f"name: {self.name}, capacity: {self.capacity}, place: {self.place}"
    
# class Show(db.Model):
#     __tablename__ = 'show'
#     show_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     title = db.Column(db.String, nullable=False)
#     description = db.Column(db.String)
#     rating = db.Column(db.Float)
#     ticket_price = db.Column(db.Float, nullable=False)
#     venue_id = db.Column(db.Integer, db.ForeignKey('venue.venue_id'),
#         nullable=False )
#     # date_created needs to be added
#     # -------------
#     # tags are needed to add
#     # --------------
    
#     # just for testing/debugging purpose; string format of Show object
#     def __str__(self) -> str:
#         return f"title: {self.title}, description: {self.description}, ticket_price: {self.ticket_price}"

# class Admin(db.Model):
#     admin_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     user_id = db.Column(db.Integer, nullable=False)

# class Bookings(db.Model):
#     user_id = db.Column(db.Integer,   db.ForeignKey("user.user_id"), primary_key=True, nullable=False)
#     venue_id = db.Column(db.Integer,   db.ForeignKey("venue.venue_id"), primary_key=True, nullable=False)
#     show_id = db.Column(db.Integer,  db.ForeignKey("show.show_id"), primary_key=True, nullable=False) 
#     user_id = db.Column(db.Integer,  db.ForeignKey("user.user_id"), primary_key=True, nullable=False)
