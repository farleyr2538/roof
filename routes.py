from flask import Blueprint, request, jsonify, render_template
from sqlalchemy import or_
from models import db, Rating, User, ReviewRequest, BlogPost
from schemas import rating_schema, ratings_schema, user_schema, users_schema, blog_post_schema
import logging
from datetime import datetime, timezone
from flask_mail import Mail, Message
import os
from mail import mail

api = Blueprint('api', __name__)

# configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# create
@api.route('/submit', methods=['POST'])
def create():

    data = request.get_json()

    # check if user exists
    # if so, get user_id
    # if not, add user

    fn = data.get('first_name')
    ln = data.get('last_name')
    print(f"fn: {fn}")
    print(f"ln: {ln}")
    print(f"fn is of type {type(fn)}")
    print(f"ln is of type {type(ln)}")
    email = data.get('email')

    query = User.query.filter(User.email == email).first()

    if query:
        # user exists, so return user_id
        user_id = query.user_id
        print(f"User {fn} {ln} already exists")
    else:
        # user doesn't exist, so create user, and find its user_id
        user = User(
            fn=fn,
            ln=ln,
            email=email
        )
        db.session.add(user)
        db.session.commit()
        print(f"User added: {fn} + {ln}")
        user_id = User.query.filter(User.email == email).first().user_id

    print(f"User ID: {user_id}")
    
    for key, value in data.items():
        print(f"{key}: {value}")

    # get the rest of the data
    address = data.get('address')
    postcode = data.get('postcode')
    landlord_rating = int(data.get('landlordRating'))
    property_rating = int(data.get('propertyRating'))
    issues = data.get('issues')
    years = data.get('years')
    current_time = data.get('timestamp')

    # assign it all to a Rating instance
    r = Rating(
        user_id=user_id, 
        fn=fn, 
        ln=ln, 
        address=address, 
        postcode=postcode, 
        landlord_rating=landlord_rating, 
        property_rating=property_rating, 
        issues=issues, 
        years=years, 
        time=current_time
    )

    print("about to attempt adding rating to session")

    try:
        db.session.add(r)
        print("rating added to session")
        print("about to attempt commit")
        db.session.commit()
        print("commit successful")
        return {
            "fn" : fn,
            "ln" : ln,
            "user_id" : user_id,
            "address" : address,
            "postcode" : postcode,
            "landlord_rating" : landlord_rating,
            "property_rating" : property_rating,
            "issues" : issues,
            "years" : years,
            "current_time" : current_time
        }, 200
    except Exception as e:
        db.session.rollback()
        print(f"error: {e}")
        return jsonify({"error": "Failed to insert rating"}), 500


@api.route('/get_all', methods=['GET'])
def read():
    reviews = Rating.query.all()
    return jsonify([{
        'rating_id': review.rating_id,
        'address': review.address.replace("’", "").replace("'", "").title(),
        'postcode': review.postcode.upper(),
        'landlord_rating': review.landlord_rating,
        'years': review.years,
        'fn': review.fn,
        'ln': review.ln,
        'time': review.time
    } for review in reviews])
    
# if method is 'POST':
    # get the filter text field
    # search database for reviews in which the address/postcode is similar
    # return these reviews

@api.route('/search', methods=['POST'])
def search():
    json = request.get_json()
    filter = json['filter']
    if not filter:
        return jsonify({"error": "No JSON data received"}), 404
    else:
        query = Rating.query.filter(
            or_ (
                Rating.address.ilike(f"%{filter}%"),
                Rating.postcode.ilike(f"%{filter}%")
            )
        )
        result = query.all()
        return_value = ratings_schema.dump(result)
        print("Before: ", return_value)
        for value in return_value:
            value['address'] = value['address'].replace("'", "").title()
            value['postcode'] = value['postcode'].upper()
        print("After: ", return_value)
        return jsonify(return_value)
    

# given an id via post, return the data for that review
@api.route('/review/<uuid:rating_id>', methods=['GET', 'POST'])
def get(rating_id):
    review = Rating.query.filter(Rating.rating_id == rating_id).first()
    value = rating_schema.dump(review)
    if value:
        value['postcode'] = value['postcode'].upper()
        value['address'] = value['address'].replace("'", "").title()
        return jsonify(value)
    else:
        return jsonify({'error': 'no value found'}), 404
    

@api.route('/request-review', methods=['POST'])
def request_review():
    # Add these at the start of your route
    from flask import current_app
    print("Mail Settings:")
    print(f"MAIL_SERVER: {current_app.config['MAIL_SERVER']}")
    print(f"MAIL_PORT: {current_app.config['MAIL_PORT']}")
    print(f"MAIL_USERNAME: {current_app.config['MAIL_USERNAME']}")
    print(f"MAIL_USE_TLS: {current_app.config['MAIL_USE_TLS']}")
    print(f"MAIL_USE_SSL: {current_app.config['MAIL_USE_SSL']}")
    
    # get address1, address2, and postcode from json data posted.
    addressData = request.get_json()

    print(addressData)

    address1 = addressData.get('address1')
    address2 = addressData.get('address2')
    postcode = addressData.get('postcode')
    name = addressData.get('name')
    
    print(f"data received: {address1}, {address2}, {postcode}, {name}")
    
    if not address1 or not address2 or not postcode or not name:
        return jsonify({"error": "Address and postcode are required"}), 400
        
    # Combine address lines if address2 exists
    full_address = address1
    if address2:
        full_address = f"{address1}, {address2}"
        
    # Create new review request
    new_request = ReviewRequest(
        address=full_address,
        postcode=postcode,
        status='pending',
        request_date=datetime.now(timezone.utc),
        name=name
    )
    
    msg = Message(
        "New Review Request",
        sender=os.getenv('MAIL_USERNAME'),
        recipients=["farleyr2538@icloud.com"],
        body=f"address: {full_address}\npostcode: {postcode}\nname: {name}"
    )

    try:
        mail.send(msg)
        db.session.add(new_request)
        db.session.commit()
        return jsonify({"message": "Review request submitted successfully"}), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error: {str(e)}")
        return jsonify({"error": f"Failed to submit request: {str(e)}"}), 500
    

@api.route('/get_blog_posts')
def get_blog_posts():
    posts = BlogPost.query.all()
    return jsonify([{
        'post_id': post.post_id,
        'title': post.title,
        'html': post.html,
        'slug': post.slug,
        'created_at': post.created,
        'updated_at': post.updated
    } for post in posts])

@api.route('/view_post/<string:slug>', methods=['GET', 'POST'])
def view_post(slug):
    result = BlogPost.query.filter_by(slug=slug).first()
    result_data = blog_post_schema.dump(result)
    if result_data:
        return jsonify(result_data)
    else:
        return jsonify({'error':'post not found'}), 404