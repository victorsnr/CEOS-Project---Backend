from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from routes.web import web

db = SQLAlchemy()


def create_app():

    app = Flask(__name__)

    app.config.from_object("config.Config")

    db.init_app(app)


    app.register_blueprint(web)

    return app