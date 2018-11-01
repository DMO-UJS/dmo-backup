
from flask import Flask
from flask_cors import CORS

from app.models.OntologyLibray import db

def register_blueprints(app):
    from app.api.match import match
    from app.api.askfor import askfor
    app.register_blueprint(match)
    app.register_blueprint(askfor)

def create_app():
    app=Flask(__name__)
    CORS(app,resources=r'/*')
    app.config.from_object('app.config.setting')
    app.config.from_object('app.config.secure')

    register_blueprints(app)

    db.init_app(app)
    db.create_all(app=app)

    return app