from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import app_config

db = SQLAlchemy()


def create_app(configuration="development"):
    app = Flask(__name__)
    app.config.from_object(app_config[configuration])
    db.init_app(app)

    # register blueprints
    from app.endpoints.authentication.views import auth
    from app.endpoints.shoppinglist.views import list_blueprint

    app.register_blueprint(auth)
    app.register_blueprint(list_blueprint)
    return app
