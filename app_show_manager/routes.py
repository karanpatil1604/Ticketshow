from flask import Blueprint, request, render_template, redirect, flash, url_for, session
from .models import Venue, Show,Bookings, ShowSearch, SearchCity, Tags
from app_user.models import User 
from Main.config import login_required
from flask import current_app as app
from Main.db import db

from datetime import datetime

bp = Blueprint('show_manager', __name__, url_prefix='')


@bp.route("/", methods=["GET", "POST"])
def home():
    try:
        venues = Venue.query.all()
        # tuple of (start_time, end_time, show_id, show.title, show.ticket_price, s.fill_count, venue_id, v.name, v.place,v.capacity, show.rating)
        # _________(___0______,____1____,____2____,____3_____,_______4________,_______5________,____6___,____7____,___8____,___9____,____10_____)
        shows = []
        qtags = Tags.query.all()
        tags=set()
        for t in qtags:
            print(t.tag)
            tags.add(t.tag.lower().strip())
        for v in venues:
            for s in v.shows:
                if str(datetime.now()) <= s.start_time:
                    shows.append((s.start_time,s.end_time, s.show_id, s.title, s.ticket_price, s.fill_count , v.venue_id, v.name, v.place, v.capacity, s.rating))
        shows.sort(reverse=True)
    except:
        flash("Oops! something went wrong!", 'error')
        return redirect(url_for('show_manager.home'))
    return render_template('index.html', venues=venues, shows=shows, tags=tags)



@bp.route("/genere_wise", methods=["GET", "POST"])
def genre_wise():
    if request.method == "POST":
        try:
            sel_tags = request.form.getlist('tag')
            sel_tags = [t.strip().lower() for t in sel_tags]
            venues = Venue.query.all()
            shows = []
            ids = []
            for t in sel_tags:
                tag = Tags.query.filter(Tags.tag.like(t.strip())).all()
                for e in tag:
                    ids.append(e.show_id)
                print('got t')
            ids = set(ids)
            for id in ids:
                shows.append(Show.query.filter(Show.show_id==id).first())
                
        except:
            flash("No shows with given genre", 'info')
            # return redirect(url_for("show_manager.home"))
        return render_template('user/genre_wise.html', sel_tags=sel_tags, shows= shows, venues=venues)


@bp.route("/bookings/<int:user_id>/", methods=["GET", "POST"])
@login_required
def user_bookings(user_id):
    bookings = Bookings.query.filter(Bookings.user_id==user_id).order_by(Bookings.num_seats).all()
    return render_template('user/bookings.html', bookings=bookings)






@bp.route("booking/<int:venue_id>/<int:show_id>/", methods=["GET", "POST"])
@login_required
def create_booking(venue_id, show_id):
    venue = Venue.query.filter( Venue.venue_id == venue_id).first()
    show = Show.query.filter(Show.show_id==show_id).first()
    if request.method=='POST':
        show = Show.query.filter(Show.show_id==show_id).first()
        num_seats = int(request.form.get('number'))
        user_id = session.get('user_id')
        bookings = Bookings.query.filter(Bookings.venue_id==venue_id, Bookings.show_id==show_id, Bookings.user_id==user_id).all()
        error = ''
        try:
            if (show.fill_count + num_seats) <= venue.capacity:
                if len(list(bookings)) != 0:
                    print(bookings[0].venue_name)
                    bookings[0].num_seats += num_seats
                    db.session.commit()
                else:
                    new_booking = Bookings(user_id=user_id, venue_id=venue_id,
                                           venue_name=venue.name, show_id=show_id,
                                           show_title=show.title, num_seats=num_seats)
                    db.session.add(new_booking)
                    db.session.commit()
                show.fill_count += int(num_seats)
                db.session.commit()
                flash(f'successfully booked {num_seats} tickets for show {show.title}', 'success')
                return redirect(url_for('show_manager.home'))
            else:
                flash('Number of seats can\'t be more than available seats!', 'danger')
                return redirect(url_for('request.url'))
        except :
            error = "Seats already occupied"
    return render_template('user/book_ticket.html', show=show, venue=venue)

@bp.route('/venue/<int:venue_id>', methods=["GET", "POST"])
def venue_wise(venue_id):
    try:
        venue = Venue.query.filter(Venue.venue_id==venue_id).first()
        shows = venue.shows
    except:
        flash("Oops! something went wrong!", "warning")
        return redirect(url_for('show_manager.home'))
    return render_template('user/venue_wise.html', venue=venue, shows=shows)

@bp.route('/rate/<int:user_id>/<int:show_id>', methods=["GET", "POST"])
@login_required
def rate(user_id, show_id):
    
    try:
        user_book= Bookings.query.filter(Bookings.user_id==user_id, Bookings.show_id==show_id).first()
        if not user_book:
            flash("No bookings for the user to rate!", 'warning')
            return redirect(url_for('show_manager.home'))
        if request.method=="POST":
            rating = request.form['rating']
            show = Show.query.filter(Show.show_id==show_id).first()
            user_book= Bookings.query.filter(Bookings.user_id==user_id, Bookings.show_id==show_id).first()
            print(user_book.venue_name, user_book.show_title)
            user_book.user_rating = float(rating)
            db.session.commit()
            rating = Bookings.query.filter(Bookings.show_id==show_id).all()
            if rating:
                n = len(rating)
                total = 0
                for r in rating:
                    total += r.user_rating
                avg = total/n
                show.rating = avg
                db.session.commit()
            flash("Rated the show successfully!", "info")
            return redirect(url_for('show_manager.user_bookings', user_id=user_id))
    except:
        print("rated Failed ------------")
        flash("Oops! something went wrong!", "warning")
        return redirect(url_for('show_manager.rate', user_id=user_book.user_id, show_id=user_book.show_id))
    return render_template('user/rate.html', user_book=user_book)


@bp.route('/show_details/<int:show_id>', methods=["GET"])
def show_details(show_id):
    try:
        show = Show.query.filter(Show.show_id == show_id).first()
        venue = None
        if show is not None:
            venue = Venue.query.filter(Venue.venue_id == show.venue_id).first()
    except:
        flash("Oops! something went wrong")
        return redirect(url_for("show_manager.home"))
    return render_template('show_details.html', show=show, venue=venue)



@bp.route('/search', methods=["GET"])
def search():
    q = request.args.get('q')
    results = []
    city_result = []
    cities = []

    try:
        if q:
            sh_query = db.session.query(ShowSearch).filter(
                ShowSearch.title.op("MATCH")(q)).all()
        v_query = db.session.query(SearchCity).filter(
            SearchCity.name.op("MATCH")(q)).all()

        c_query = db.session.query(SearchCity).filter(
            SearchCity.place.op("MATCH")(q)).all()

        if v_query is not None:
            for v in v_query:
                city_result.extend(Venue.query.filter(
                    Venue.venue_id == v.venue_id).all())

        if c_query is not None:
            for c in c_query:
                city_result.extend(Venue.query.filter(
                    Venue.venue_id == c.venue_id))

        if sh_query is not None:
            for s in sh_query:
                results.extend(Show.query.filter(Show.show_id == s.show_id))
    except:
        flash("oops, something went wrong!", 'danger')
        return redirect(url_for('show_manager.home'))
    return render_template('results.html', results=results, city_wise=city_result, q=q)
