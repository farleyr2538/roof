import os
from flask import Flask, render_template, request
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, create_engine, MetaData, or_
from sqlalchemy.orm import DeclarativeBase

app = Flask(__name__)

addition = "ql"
old_url = os.environ.get('DATABASE_URL')
index = 8
url = old_url[:index] + addition + old_url[index:]
app.config['SQLALCHEMY_DATABASE_URI'] = url
link = app.config['SQLALCHEMY_DATABASE_URI']

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(app)

metadata_obj = MetaData()
engine = create_engine(link)
print("test")

class Rating(db.Model):
    __tablename__ = 'ratings'
    rating_id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    fn = db.Column(db.String, nullable=False)
    ln = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    postcode = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    years = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fn = db.Column(db.String, nullable=False)
    ln = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)

with app.app_context():
        db.create_all()

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

        rating = Rating(fn = fn, ln = ln, address=address, postcode=postcode, rating=rating, years=years_string, time=time)
        user = User(fn=fn, ln=ln, email=email)
        db.session.add(rating)
        db.session.add(user)
        db.session.commit()

        return render_template('submit.html')

@app.route("/rate", methods=["GET", "POST"])
def form():
    return render_template('form.html')

@app.route("/find-rating", methods=["GET", "POST"])
def find_rating():
    all_ratings = Rating.query.all()
    return render_template('find_rating.html', ratings=all_ratings)

@app.route("/search", methods=["POST"])
def search():
    term = request.form.get("search")
    rv = Rating.query.filter(
        or_ (
            Rating.address.ilike(f"%{term}%"),
            Rating.postcode.ilike(f"%{term}%")
        )
    )
    return render_template('find_rating.html', ratings=rv)
