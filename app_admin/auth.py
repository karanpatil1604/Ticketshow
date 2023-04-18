from flask import Blueprint, request, render_template, redirect, flash, url_for, session
from werkzeug.security import check_password_hash
from app_user.models import User
from .models import Admin
from flask import current_app as app
from Main.db import db
import click
from werkzeug.security import generate_password_hash

bp = Blueprint('admin', __name__,url_prefix='/admin')


@app.cli.command('create-admin')
def create_admin():
    name = input("Admin Name: ")
    pas = input("Password: ")
    conf_pas = input("Confirm password: ")
    pswd = generate_password_hash(pas)
    while True:
        if conf_pas.strip() == pas.strip():
            break
        print("password did not match")
    email = input("email: ")
    mobile=input("Phone: ")
    
    if not name or not pas or not email:
        print('All parameters are required except phone.')
        return 

    print(f'Creating Admin for username: {name}')
    try:
        new_admin = Admin(admin_name=name, password=pswd, email=email, mobile=mobile)
        db.session.add(new_admin)
        db.session.commit()
    except:
        print("Something went wrong on the server side.")
    else:
        print(f'Successfully created admin with username: {name} and email: {email}')
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        admin_name = request.form['username']
        password = request.form['password']
        error = None
        admin = Admin.query.filter(Admin.admin_name == admin_name).first()
        if admin:
            user = User.query.filter(User.username==admin.admin_name).first()
        if admin is None:
            error = 'Incorrect Username.'
        elif not check_password_hash(admin.password, password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['admin_name'] = admin.admin_name
            if user is not None:
                session['user_id'] = user.user_id
            session['admin_id'] = admin.admin_id
            session.modified = True
            flash(f"Successfully logged in for Admin: {admin.admin_name}", 'info')
            return redirect(url_for('admin_crud.dashboard'))

        flash(error, 'error')
        
        # debugging 
        print(error)

    return render_template('admin/admin_login.html')

@bp.route('/logout')
def logout():
    session.pop('admin_id', None)
    session.pop('admin_name', None)
    session.modified= True
    flash('You were logged out!', 'info')
    return redirect(url_for('admin.login'))
