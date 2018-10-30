
from flask import Flask
from flask_cors import CORS

from app.models.OntologyLibray import db


def create_app():
    app=Flask(__name__)
    CORS(app,resources=r'/*')
    app.config.from_object('app.config.setting')
    app.config.from_object('app.config.secure')


    db.init_app(app)
    db.create_all(app=app)

    return app