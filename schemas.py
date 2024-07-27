from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import Rating, User

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