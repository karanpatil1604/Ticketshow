from flask import Blueprint, request, render_template, redirect, flash, url_for, session, g
from werkzeug.security import check_password_hash, generate_password_hash
from app_user.models import User

from sqlalchemy.exc import IntegrityError
from functools import wraps
from flask import session, redirect, url_for,g
from Main.db import db

bp = Blueprint('auth', __name__,url_prefix='/auth')

# def login_required(original):
#     @wraps(original)
#     def wrapper_function(*args, **kwargs):
#         print(session['username'])
#         if g.user is None:
#             return redirect(url_for('auth.login'))
#         else:
#             return original(*args, **kwargs)
#     return wrapper_function




@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        mobile = request.form['mob']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not email:
            error = "email is required"


        if error is None:
            try:
                new_user = User(username=username, password=generate_password_hash(password), email=email, mobile=mobile)
                db.session.add(new_user)
                db.session.commit()
            except AttributeError:
                error = f"User {username} is already registered."
                return redirect(url_for("auth.register"))

            else:
                flash(f'Created account for {username}!', 'success')
                return redirect(url_for("auth.login"))

        flash(error)

        # debugging
        print(error)
        
    return render_template('user/user_register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = User.query.filter(User.username == username).first()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['username'] = user.username
            session['user_id'] = user.user_id
            session.modified = True
            return redirect(url_for('show_manager.home'))

        flash(error)
        
        # debugging 
        print(error)

    return render_template('user/user_login.html')

@bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    session.modified= True
    return redirect(url_for('show_manager.home'))