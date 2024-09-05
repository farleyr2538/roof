from flask import Flask
from models import db
from schemas import ma
from routes import api
from views import views
import os

app = Flask(__name__)

old_url = os.environ.get('DATABASE_URL')
if old_url:
    if old_url.startswith("postgres://"):
        new_url = old_url.replace("postgres://", "postgresql://", 1)
    else:
        new_url = old_url
else:
    print("environment url is None")
    new_url = None

app.config['SQLALCHEMY_DATABASE_URI'] = new_url

db.init_app(app)
ma.init_app(app)

app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(views)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)