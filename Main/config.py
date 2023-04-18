import os
from functools import wraps
from flask import session, redirect, url_for, request,flash
from flask import current_app as app

from werkzeug.security import generate_password_hash


basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    DEBUG = False
    SECRET_KEY='dev'
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False

class LocalDevelopmentConfig(Config):
    SQLITE_DB_DIR = os.path.join(basedir, "../db_directory")
    # SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "database.db")
    TESTING = False
    SQLALCHEMY_DATABASE_URI= "sqlite:///ticket_project.db"
    DEBUG = True





def admin_login_required(original):
    @wraps(original)
    def wrapper_function(*args, **kwargs):
        if session.get('admin_id'):
            return original(*args, **kwargs)
        else:
            flash('You are required to Log in as an admin', 'warning')
            return redirect(url_for('admin.login', next=request.url))
    return wrapper_function

def login_required(original):
    @wraps(original)
    def wrapper_function(*args, **kwargs):
        if session.get('user_id'):
            return original(*args, **kwargs)
        flash('You are required to log in or register first', 'warning')
        return redirect(url_for('auth.login', next=request.url))
    return wrapper_function
