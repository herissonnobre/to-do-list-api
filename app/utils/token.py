"""
This module allows functions to generate and verify JWT tokens

Functions:
    - generate_token(user_id): Generates a JWT token for a given user_id
    - verify_token(token): Verifies a JWT token

Exceptions:
    - jwt.ExpiredTokenError: Raised when JWT expired
    - jwt.InvalidTokenError: Raised when JWT invalid
    - Generic Exception: Raised when generic error occurs
"""
import os
from datetime import datetime, timedelta

import jwt
from dotenv import load_dotenv

# Load env variables from .env file
load_dotenv()

# Gets secret key from env variables
SECRET_KEY = os.getenv('SECRET_KEY')


def generate_token(user_id: str):
    """
    Generates a JWT token for a specific user

    Parameters:
    user_id (int): the id of the user

    Returns:
    str: the JWT token

    Raises:
    Exception: if an error occurs while generating the token

    :param user_id:str: the id of the user
    :return: str: the JWT token
    """
    try:
        payload = {
            'exp': datetime.now() + timedelta(days=1),
            'iat': datetime.now(),
            'sub': user_id,
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return token
    except Exception as e:
        raise Exception(f"An error occurred while generating the token: {e}")


def verify_token(token):
    """
    Verifies if a JWT token is valid and returns the user id

    Parameters:
    token (str): the JWT token

    Returns:
    str: the id of the user if valid

    Raises:
    jwt.ExpiredSignatureError: if the token is expired
    jwt.InvalidTokenError: if the token is invalid
    Exception: if an error occurs while verifying the token

    :param token:str: the JWT token
    :return: user_id (str): the id of the user
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError("Token expired. Please log in again.")
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError("Invalid token. Please log in again.")
    except Exception as e:
        raise Exception(f"An error occurred while verifying the token: {e}")
