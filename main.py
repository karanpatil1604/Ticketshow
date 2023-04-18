import os
from flask import Flask
from Main.config import LocalDevelopmentConfig
from Main.db import db
from flask_migrate import Migrate
from flask_restful import Resource, Api
from app_admin.api import ShowAPI, VenueAPI


basedir = os.path.abspath(os.path.dirname(__file__))
def create_app():
    
    app = Flask(__name__, template_folder='templates')
    
    if os.getenv('ENV', "development") == "production":
      raise Exception("Currently no production config is setup.")
    else:
      print("Starting Local Development")
      app.config.from_object(LocalDevelopmentConfig)
      UPLOAD_FOLDER = os.path.join(basedir, "static/img/show_thumbnails" )
      app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    db.init_app(app)
    app.app_context().push()
    # with app.app_context():
      # db.create_all()
    migrate = Migrate(app, db)
    


    from Main import controllers
    
    return app

app = create_app()



# @app.before_first_request
# def before_first_request():
#     from flask import session
#     session.clear()
#     session.modified=True

# from Main.controllers import *

if __name__ == '__main__':
  # Run the Flask app
  with app.app_context():
        db.create_all()
  app.run(host='0.0.0.0',port=8080, debug=True)