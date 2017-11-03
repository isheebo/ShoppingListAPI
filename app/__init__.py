from flask import Flask, jsonify
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
    from app.endpoints.items.views import items
    from app.docs.views import apiary

    app.register_blueprint(auth)
    app.register_blueprint(list_blueprint)
    app.register_blueprint(items)
    app.register_blueprint(apiary)

    @app.errorhandler(405)
    def method_not_allowed(_):
        return jsonify({
            "status": "failure",
            "message": "method not allowed on this endpoint"
        }), 405

    @app.errorhandler(404)
    def not_found(_):
        return jsonify({
            "status": "failure",
            "message": "resource not found on this URL"
        }), 404

    return app
