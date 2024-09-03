from flask import Blueprint, request, jsonify
from sqlalchemy import or_
from models import db, Rating, User
from schemas import rating_schema, ratings_schema, user_schema, users_schema
import logging

api = Blueprint('api', __name__)

# configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# create
@api.route('/submit', methods=['POST'])
def create():
    if request.is_json:
        # theoretically, requests from Swift
        # handle as JSON
        data = request.get_json()
        logging.debug("Handled as JSON")
        from_app = True
    else:
        # theoretically, requests from web
        # handle as form data
        data = request.form.to_dict()
        logging.debug("Handled as dictionary")
        from_app = False
    
    for key, value in data.items():
        logging.debug(f"{key}: {value}")

    fn = data.get('first_name')
    ln = data.get('last_name')
    address = data.get('address')
    postcode = data.get('postcode')
    if not from_app:
        rating = int(data.get('rating')[0])
    else:
        rating = int(data.get('rating'))
    years = data.get('years')
    current_time = data.get('time')

    # assign it all to a Rating instance
    r = Rating(fn=fn, ln=ln, address=address, postcode=postcode, rating=rating, years=years, time=current_time)

    try:
        db.session.add(r)
        db.session.commit()
        return jsonify({
            "fn":fn,
            "ln":ln,
            "address":address,
            "postcode":postcode,
            "rating":rating,
            "years":years,
            "time":current_time
            }), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        logging.debug(f"Error: {e}")
        return jsonify({"error": "Failed to insert rating"}), 500


# if method is 'GET', return all reviews

@api.route('/get_all', methods=['GET'])
def read():
    reviews = Rating.query.all()
    return jsonify([{
        'rating_id': review.rating_id,
        'address': review.address.replace("'", "").title(),
        'postcode': review.postcode.upper(),
        'rating': str(review.rating),
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
        return jsonify(value)
    else:
        return jsonify({'error': 'no value found'}), 404