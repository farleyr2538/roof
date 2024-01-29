import os
import sqlite3
from flask import Flask, render_template, redirect, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

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

        db.execute('INSERT INTO ratings (fn, ln, address, postcode, rating, years, time) VALUES (?, ?, ?, ?, ?, ?, ?)', fn, ln, address, postcode, rating, years_string, time)
        db.execute('INSERT INTO users (fn, ln, email) VALUES (?, ?, ?)', fn, ln, email)
        database.commit()

        return render_template('submit.html')

@app.route("/rate", methods=["GET", "POST"])
def form():
    return render_template('form.html')

@app.route("/find-rating", methods=["GET", "POST"])
def find_rating():
    ratings = db.execute('SELECT * FROM ratings;')
    database.commit()
    return render_template('find_rating.html', ratings=ratings)

@app.route("/search", methods=["POST"])
def search():
    db = sqlite3.connect("sqlite:///project.db")
    term = request.form.get("search")
    search_term = ("%" + term + "%")
    ratings = db.execute("SELECT * FROM ratings WHERE address LIKE ? OR postcode LIKE ?;", search_term, search_term)
    database.commit()
    return render_template('find_rating.html', ratings=ratings)
