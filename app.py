import os
import psycopg2
from flask import Flask, render_template, redirect, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, String, MetaData, Integer, Computed, Text, create_engine, event, MetaData, or_
from sqlalchemy.orm import DeclarativeBase


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://cbxuyldqyifqcu:95de1fa4afcafdf7df6bfcd075109614bafd6dc7e2244bb754aeb7ce042e2540@ec2-44-215-40-87.compute-1.amazonaws.com:5432/dfk6dqpg7rk537'
link = app.config['SQLALCHEMY_DATABASE_URI']

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(app)

metadata_obj = MetaData()
engine = create_engine(link)

print("Database URL:", app.config['SQLALCHEMY_DATABASE_URI'])

ratings = Table(
    "ratings",
    metadata_obj,
    Column("rating_id", Integer, primary_key=True),
    Column("fn", String),
    Column("ln", String),
    Column("address", String),
    Column("postcode", String),
    Column("rating", Integer),
    Column("years", String),
    Column("time", String)
)

users = Table(
    "users",
    metadata_obj,
    Column("user_id", Integer, primary_key=True),
    Column("fn", String),
    Column("ln", String),
    Column("email", String)
)

class ratings_model(db.Model):
    rating_id = db.Column(db.Integer, primary_key=True) 
    fn = db.Column(db.String, nullable=False)
    ln = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    postcode = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    years = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)

class users_model(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    fn = db.Column(db.String, nullable=False)
    ln = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)

if __name__ == '__main__':
    with app.app_context():
        metadata_obj.create_all()
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
