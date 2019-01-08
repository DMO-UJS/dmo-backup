from datetime import timedelta

from flask import Flask
from flask_cors import CORS

from app.models.OntologyLibray import db
from app.user.client import client
from app.user.token import token
from app.user.user import user










def register_blueprints(app):
    from app.api.match import match
    from app.api.askfor import askfor
    from app.ontology.OntologyOperation import ontolog
    from app.ontology.OntologyClassOperation import ontologclass
    app.register_blueprint(match)
    app.register_blueprint(askfor)
    app.register_blueprint(ontolog)
    app.register_blueprint(ontologclass)
    app.register_blueprint(user)
    app.register_blueprint(client)
    app.register_blueprint(token)

def create_app():
    app=Flask(__name__)
    CORS(app,resources=r'/*')
    app.config.from_object('app.config.setting')
    app.config.from_object('app.config.secure')
    app.config['SEND_FILE_MAX_AGE_DEFAULT']=timedelta(seconds=1)
    from app.models.user import User
    register_blueprints(app)


    db.init_app(app)
    db.create_all(app=app)

    return app