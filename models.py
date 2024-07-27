from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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