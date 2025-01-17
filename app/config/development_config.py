"""
Development configuration settings for the application.

Classes:
    - DevelopmentConfig: Development configuration.
"""
import os

from app.config import BaseConfig


class DevelopmentConfig(BaseConfig):
    """
    Development configuration class.

    Attributes:
        - SQLALCHEMY_DATABASE_URI (str): SQLAlchemy database URI.
    """
    SQLALCHEMY_DATABASE_URI: str = os.environ.get('DEVELOPMENT_DATABASE_URL') or 'sqlite:///development.db'
    DEBUG: bool = True
