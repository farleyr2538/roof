from flask import Blueprint, request, jsonify, render_template
from sqlalchemy import or_
import time
from models import db, Rating, User
from schemas import rating_schema, ratings_schema, user_schema, users_schema

views = Blueprint('views', __name__)

# homepage
@views.route("/")
def index():
    return render_template('index.html', time=time)


# view reviews
@views.route("/find_rating", methods=["GET", "POST"])
def find_rating():
    return render_template('find_rating.html')


@views.route("/search", methods=["POST"])
def search():
    return render_template('find_rating.html')


# review submittion form
@views.route("/rate", methods=['GET'])
def form():
    return render_template('form.html', time=time)


# view an individual review
@views.route("/view_review/<uuid:rating_id>", methods=['GET', 'POST'])
def review(rating_id):
    return render_template('review.html', rating_id=rating_id)


# show a thank-you screen
@views.route('/submit', methods=['GET', 'POST'])
def submit():
    return render_template('submit.html')

# about page
@views.route("/about", methods=['GET'])
def about():
    return render_template('about.html')


@views.route("/blog")
def blog():
    return render_template('blog_home.html')


@views.route("/read_blog/<string:slug>", methods=['GET', 'POST'])
def view_blog_post(slug):
    return render_template('blog_post.html', slug=slug)