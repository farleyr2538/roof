from flask import Flask
from models import db
from schemas import ma
from routes import api
from views import views

def create_app():

    app = Flask(__name__)

    old_url = "postgres://mwwlxvlluvoquu:1b2b550fde58c40f13f4b5e21e645d665a028038fc5f49f2420d0c426c49fc78@ec2-52-22-202-133.compute-1.amazonaws.com:5432/datr46pdevhh42"
    addition = "ql"
    index = 8
    url = old_url[:index] + addition + old_url[index:]
    app.config['SQLALCHEMY_DATABASE_URI'] = url

    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(views)

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)