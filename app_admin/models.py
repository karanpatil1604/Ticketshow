from Main.db import db

class Admin(db.Model):
    admin_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    admin_name = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    mobile = db.Column(db.String)
