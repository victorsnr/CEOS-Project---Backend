from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from routes.web import web
from routes.api import api
from extensions import db

def create_app():

    app = Flask(__name__)

    app.config.from_object("config.Config")

    db.init_app(app)
    
    with app.app_context():
        db.create_all()

    app.register_blueprint(api, url_prefix = '/api')
    app.register_blueprint(web)

    return app