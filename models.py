from flask_sqlalchemy import SQLAlchemy
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey, ARRAY, String, Column, Integer

db = SQLAlchemy()

class Rating(db.Model):
    __tablename__ = 'ratings'
    rating_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False) 
    user_id = db.Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    fn = db.Column(db.String, nullable=True)
    ln = db.Column(db.String, nullable=True)
    address = db.Column(db.String, nullable=False)
    landlord_rating = db.Column(db.Integer, nullable=True)
    property_rating = db.Column(db.Integer, nullable=True)
    postcode = db.Column(db.String, nullable=False)
    issues = db.Column(db.JSON, default=list, nullable=True)
    years = db.Column(db.String, nullable=True)
    time = db.Column(db.String, nullable=True)

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    fn = db.Column(db.String, nullable=False)
    ln = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)

class ReviewRequest(db.Model):
    __tablename__ = 'review_requests'
    request_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    address = db.Column(db.String, nullable=False)
    postcode = db.Column(db.String, nullable=False) 
    status = db.Column(db.String, nullable=False)
    request_date = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.String, nullable=False)

class BlogPost(db.Model):
    __tablename__ = 'blog_posts'
    post_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    title = db.Column(db.String, nullable=False)
    html = db.Column(db.String, nullable=True)
    created = db.Column(db.String, nullable=True)
    updated = db.Column(db.String, nullable=True)
    slug = db.Column(db.String, nullable=True)