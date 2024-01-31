import os
from flask import Flask, render_template, redirect, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from sqlalchemy.dialects.postgresql import psycopg2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app, session_options={"autoflush": False})

class ratings(db.Model):
    fn = db.Column(db.String, nullable=False)
    ln = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    postcode = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    years = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)

class users(db.Model):
    fn = db.Column(db.String, nullable=False)
    ln = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()

    @app.route("/")
    def index():
        return render_template('index.html')

    @app.route("/submit", methods=["GET", "POST"])
    def submit():
        if request.method == "POST":
            # assign data to variables
            fn = request.form.get("first_name")
            ln = request.form.get("last_name")
            address = request.form.get("address")
            postcode = request.form.get("postcode")
            email = request.form.get("email")
            rating = request.form.get("rating")
            years = request.form.getlist("years[]")
            years_string = ", ".join(years)
            time = datetime.now()

            rating = ratings(fn = fn, ln = ln, address=address, postcode=postcode, email=email, rating=rating, years=years_string, time=time)
            user = users(fn=fn, ln=ln, email=email)
            db.session.add(rating)
            db.session.add(user)
            db.session.commit()

            return render_template('submit.html')

    @app.route("/rate", methods=["GET", "POST"])
    def form():
        return render_template('form.html')

    @app.route("/find-rating", methods=["GET", "POST"])
    def find_rating():
        all_ratings = ratings.query.all()
        return render_template('find_rating.html', ratings=all_ratings)

    @app.route("/search", methods=["POST"])
    def search():
        term = request.form.get("search")
        search_term = ("%" + term + "%")
        rv = ratings.query.filter(
            or_ (
                ratings.address.like(f"%{term}"),
                ratings.postcode.like(f"%{term}")
            )
        )
        return render_template('find_rating.html', ratings=rv)
