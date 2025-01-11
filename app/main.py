"""
Application factory and initialization.

Functions:
    - create_app(): Creates and configures the Flask application.
"""
from dotenv import load_dotenv
from flask import Flask
from app.config import Config
from app.extensions import db, migrate
from app.routes import register_blueprints

load_dotenv()


def create_app() -> Flask:
    """
    Create and configure the Flask application.

    :return:Flask: The configured Flask app instance.
    """
    flask_app = Flask(__name__)
    flask_app.config.from_object(Config)

    db.init_app(flask_app)
    migrate.init_app(flask_app, db)

    register_blueprints(flask_app)

    return flask_app


if __name__ == "app.main":
    app = create_app()
    with app.app_context():
        db.create_all()
