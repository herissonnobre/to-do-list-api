"""
Configuration settings for the application.

Classes:
    - Config: Application configuration.
"""

import os


class Config:
    """
    Application configuration class.

    Attributes:
        - SECRET_KEY (str): Secret key for the application.
        - SQLALCHEMY_DATABASE_URI (str): SQLAlchemy database URI.
        - SQLALCHEMY_TRACK_MODIFICATIONS (bool): If True, SQLAlchemy tracks modifications.
        - SQLALCHEMY_ECHO (bool): If True, SQLAlchemy echoes messages.
    """
    SECRET_KEY: str = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    SQLALCHEMY_DATABASE_URI: str = os.environ.get('DATABASE_URL') or 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_ECHO: bool = True
