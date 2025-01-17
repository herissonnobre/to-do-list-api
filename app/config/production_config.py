"""
Production configuration settings for the application.

Classes:
    - ProductionConfig: Production configuration.
"""
import os

from app.config import BaseConfig


class ProductionConfig(BaseConfig):
    """
    Production configuration class.

    Attributes:
        - SQLALCHEMY_DATABASE_URI (str): SQLAlchemy database URI.
    """
    SQLALCHEMY_DATABASE_URI: str = os.environ.get('PRODUCTION_DATABASE_URL') or 'sqlite:///production.db'
    DEBUG: bool = True
