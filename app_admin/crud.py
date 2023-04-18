import os
from flask import Blueprint, request, render_template, redirect, flash, url_for, session
from werkzeug.security import check_password_hash
from flask import current_app as app
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, func
from app_user.models import User
from .models import Admin
from app_show_manager.models import Venue, Show, Tags, Bookings, Running, ShowSearch, SearchCity

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '../static/img/admin_src'))

from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from Main.db import db
from Main.config import admin_login_required

bp = Blueprint('admin_crud', __name__,url_prefix='/admin')


# basedir = os.path.abspath(os.path.dirname(__file__))

def allowed_file(filename):
    fext = filename.split(".")[1]
    if fext.lower() == 'jpg':
        return True 
    return False 

# ----------------------- Crud on Venue ---------------------------------------

## READ

@bp.route('/dashboard/', methods=["GET", "POST"])
@admin_login_required
def dashboard():
    venues = Venue.query.all()
    return render_template('admin/dashboard.html', venues=venues)

## CREATE
@bp.route('/create_venue', methods=["GET", "POST"])
@admin_login_required
def create_venue():
    if request.method == 'POST':
        name = request.form.get('name')
        place = request.form.get('place')
        capacity = request.form.get('capacity')
        message=None
        try:
            capacity = int(capacity)
        except:
            message='Capacity must be an integer !'
            flash(message)
            return redirect(url_for('admin_crud.create_venue'))
        if not message:
            try:
                new_venue = Venue(name=name, place=place, capacity=capacity)
                db.session.add(new_venue)
                db.session.commit()
                search_city = SearchCity(venue_id=new_venue.venue_id, name=name,place=place)
                db.session.add(search_city)
                db.session.commit()
            except IntegrityError:
                message = 'Venue already exist. Please add different Venue'
                flash(message)
                return redirect(url_for('admin_crud.create_venue'))
            except:
                message ='Oops something went wrong'
                flash(message, 'danger')
                return redirect(url_for('admin_crud.dashboard'))
            else:
                flash(f'Venue {name} created successfully!', "info")
                return redirect(url_for('admin_crud.dashboard'))
    return render_template('/admin/create_venue.html')


## UPDATE
@bp.route('/update_venue/<int:venue_id>', methods=["GET", "POST"])
@admin_login_required
def update_venue(venue_id):
    try:
        venue = Venue.query.filter(Venue.venue_id==venue_id).first_or_404()
        if request.method=='POST':
            message = None
            name = request.form.get('name')
            place = request.form.get('place')
            capacity = request.form.get('capacity')
            try:
                capacity = int(capacity)
            except:
                message='Capacity must be an integer !'
                flash(message)
                return redirect(url_for('admin_crud.update_venue'))
            if venue is not None:
                venue.name=name
                venue.place = place
                venue.capacity=capacity
                db.session.commit()
                search_city = SearchCity.query.filter(SearchCity.venue_id==venue_id).first()
                if search_city:
                    db.session.delete(search_city)
                db.session.commit()
                new_search_city = SearchCity(venue_id=venue_id, name=name, place=place)
                db.session.add(new_search_city)
                db.session.commit()
                message= 'Successfully updated the venue and shows for the venue!'
            if message:
                flash(message, 'success')
            return redirect(url_for('admin_crud.dashboard'))
    except:
        flash('Oops! something went wrong!')
        return redirect(url_for('admin_crud.dashboard'))
    return render_template('admin/update_venue.html', venue=venue)

## DELETE
@bp.route('/delete_venue/<int:venue_id>', methods=["GET","POST"])
@admin_login_required
def delete_venue(venue_id):
    try:
        venue = Venue.query.filter(Venue.venue_id==venue_id).first_or_404()
        bookings = Bookings.query.filter(Bookings.venue_id==venue_id).all()
        if request.method=='POST':
            message = None
            if len(bookings) !=0:
                for b in bookings:
                    db.session.delete(b)
                    db.session.commit()
            if venue is not None:
                search_city = SearchCity.query.filter(SearchCity.venue_id==venue_id).first()
                db.session.delete(venue)
                if search_city:
                    db.session.delete(search_city)
                db.session.commit()
                message= 'Successfully deleted the venue and shows for the venue!'
            if message:
                flash(message, 'success')
            return redirect(url_for('admin_crud.dashboard'))
    except ValueError:
        flash(f"No venue to delete.", 'danger')
        return redirect(url_for('admin_crud.dashboard'))
    
    return render_template('admin/confirm_delete_venue.html', venue=venue)
# -------------------------------------------------------------------------------------------
# ********************************************************************************************


# ----------------------- Crud on Show ---------------------------------------

global SIZE_3BY4
SIZE_3BY4 = (300, 400)
## READ
@bp.route('/<int:venue_id>/', methods=["GET", "POST"])
@admin_login_required
def shows_on_venue(venue_id):
    venues = Venue.query.filter(Venue.venue_id == venue_id).all()
    return render_template('admin/dashboard.html', venues=venues)

## CREATE
@bp.route('/<int:venue_id>/create_show', methods=["GET", "POST"])
@admin_login_required
def create_show(venue_id):
    if request.method == 'POST':
        msg= None
        title = request.form.get('title')
        desc = request.form.get('desc')
        ticket_price = float(request.form.get('price'))
        start_time = request.form.get('starttime')
        if start_time != "":
            start_time = start_time.replace("T", " ")
        end_time = request.form.get('endtime')
        if end_time != "":
            end_time = end_time.replace("T", " ")
        tags = request.form.get('tags').lower().split(',')
        if tags: 
            tags = set(tags)
        tn = request.files['thumbnail']
        
        if type(ticket_price) != float or ticket_price<0:
            msg = 'Ticket Price must be a Non-negative number'
            flash(msg, 'warning')
            return redirect(url_for('admin_crud.create_show'))
        if msg is None:
            try:
                new_show = Show(title=title, description=desc, ticket_price=ticket_price, venue_id=venue_id,
                                start_time=start_time, end_time=end_time)
                db.session.add(new_show)
                db.session.commit()
                
                search_show = ShowSearch(show_id=new_show.show_id, title=title)
                db.session.add(search_show)
                db.session.commit()
                if tn.filename != "" and tn.filename.endswith('.jpg'):
                    fn = f"{new_show.show_id}.jpg"
                    i = Image.open(tn)
                    i.thumbnail(SIZE_3BY4)
                    i.save(f"./static/img/show_thumbnails/{new_show.show_id}.jpg")
                if len(tags)>0:
                    for t in tags:
                        new_tag = Tags(show_id = new_show.show_id, tag= t.lower().strip())
                        db.session.add(new_tag)
                    db.session.commit()
            except IntegrityError:
                message = 'Show already exist. Please add different Show'
                flash(message, 'warning')
                return redirect(url_for('admin_crud.dashboard'))
            
            else:
                msg=f'Successfully created the show with title {title}'
                flash(msg, 'info')
                return redirect(url_for('admin_crud.dashboard'))
        
    return render_template('/admin/create_show.html')
   

## UPDATE
@bp.route('/update_show/<int:show_id>', methods=["GET", "POST"])
@admin_login_required
def update_show(show_id):
    try:
        show = Show.query.filter(Show.show_id==show_id).first_or_404()
        if request.method=='POST':
            show_search = ShowSearch.query.filter(ShowSearch.show_id==show_id)
            message = None
            title = request.form.get('title')
            desc = request.form.get('desc')
            ticket_price = request.form.get('price')
            start_time = request.form.get('starttime')
            
            if start_time != "":
                start_time = start_time.replace("T", " ")
            end_time = request.form.get('endtime')
            if end_time != "":
                end_time = end_time.replace("T", " ")
            try:
                ticket_price = float(ticket_price)
            except:
                message='Ticket price must be a Number !'
                flash(message)
                return redirect(url_for('admin_crud.update_show'))
            
            tags = request.form.get('tags').lower().split(',')
            tn = request.files['thumbnail']
            if tn.filename != "" and tn.filename.endswith('.jpg'):
                    i = Image.open(tn)
                    i.thumbnail(SIZE_3BY4)
                    i.save(f"./static/img/show_thumbnails/{show_id}.jpg")
            if tags:
                tags = set(tags)
            if show is not None:
                show.title=title
                show.description = desc
                show.ticket_price = ticket_price
                show.start_time = start_time
                show.end_time = end_time
                db.session.commit()
                show_search = ShowSearch.query.filter(ShowSearch.show_id==show_id).first()
                if show_search:
                    db.session.delete(show_search)
                    db.session.commit()
                show_search = ShowSearch(show_id=show_id, title = title)
                db.session.add(show_search)
                db.session.commit()
                message= 'Successfully updated the Show for the venue!'
                for t in show.tags:
                    db.session.delete(t)
                db.session.commit()
                if len(tags)>0:
                    for t in tags:
                        new_tag = Tags(show_id = show_id, tag=t)
                        db.session.add(new_tag)
                    db.session.commit()
            if message:
                flash(message, 'success')
            return redirect(url_for('admin_crud.dashboard'))
    except:
        flash('Oops! something went wrong!')
        return redirect(url_for('admin_crud.dashboard'))
    return render_template('admin/update_show.html', show=show)

## DELETE
@bp.route('/delete_show/<int:show_id>', methods=["GET", "POST"])
@admin_login_required
def delete_show(show_id):
    try:
        show = Show.query.filter(Show.show_id==show_id).first_or_404()
        if request.method=='POST':
            bookings = Bookings.query.filter(Bookings.show_id==show_id).all()
            show = Show.query.filter(Show.show_id==show_id).first_or_404()
            message = None
            if len(bookings) !=0:
                for b in bookings:
                    db.session.delete(b)
                    db.session.commit()
            if show is not None:
                show_search = ShowSearch.query.filter(ShowSearch.show_id==show_id).first()
                db.session.delete(show)
                if show_search:
                    db.session.delete(show_search)
                db.session.commit()
                message= f'Successfully deleted the show and shows!'
            if message:
                flash(message, 'success')
            return redirect(url_for('admin_crud.dashboard'))
    except:
        flash(f"No show to delete.", 'danger')
        return redirect(url_for('admin_crud.dashboard'))

    return render_template('admin/confirm_delete_show.html', show=show)



def shows_plot():
    shows_bookings = db.session.execute(select(Bookings.show_id, func.count(Bookings.bid).label('counts')).group_by(Bookings.show_id)).all()
    y = []
    for t in shows_bookings:
        y.append(t.counts)
    plt.ylabel('Show Ids')
    plt.xlabel('No of bookings')
    x = [str(t.show_id) for t in shows_bookings]
    y = np.array(y)
    plt.barh(x, y, height = 0.1)
    plt.savefig(os.path.join(ROOT_DIR, 'shows_hist.png'))

def venues_plot():
    venues_bookings = db.session.execute(select(Bookings.venue_id, func.count(Bookings.bid).label('counts')).group_by(Bookings.venue_id)).all()
    y = [t.counts for t in venues_bookings]
    x = [str(t.venue_id) for t in venues_bookings]
    plt.ylabel('Venue Ids')
    plt.xlabel('No of bookings')
    plt.barh(x, y, height = 0.2)
    plt.savefig(os.path.join(ROOT_DIR, 'venues_bar.png'))

def highest_rated():
    ratings = db.session.execute(select(Show.show_id, Show.rating)).all()
    x = [str(t.show_id) for t in ratings]
    y = [t.rating for t in ratings]
    plt.ylabel('Show Ids')
    plt.xlabel('ratings')
    plt.barh(x, y, height = 0.5)
    plt.savefig(os.path.join(ROOT_DIR, 'ratings.png'))

@bp.route('/summary', methods=["GET"])
@admin_login_required
def summary():
    
    shows_plot()
    venues_plot()
    highest_rated()
    return render_template('admin/summary.html')