import os
from flask import Flask
from models import db
from schemas import ma
from routes import api
from views import views
from mail import mail

app = Flask(__name__)

# set db url
# print(os.environ.get('DATABASE_URL'))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

# set mail settings
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PW')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_DEBUG'] = True

mail.init_app(app)
db.init_app(app)
ma.init_app(app)

app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(views)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)