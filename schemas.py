from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import Rating, User, ReviewRequest, BlogPost

ma = Marshmallow()

class RatingSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Rating
        load_instance = True

rating_schema = RatingSchema()
ratings_schema = RatingSchema(many=True)

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class ReviewRequestSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ReviewRequest
        load_instance = True

review_request_schema = ReviewRequestSchema()
review_requests_schema = ReviewRequestSchema(many=True)

class BlogPostSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = BlogPost
        load_instance = True

blog_post_schema = BlogPostSchema()
blog_posts_schema = BlogPostSchema(many=True)