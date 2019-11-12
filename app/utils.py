import random
import string
from time import time

import jwt

from app.config import BaseConfig


alphabet = string.ascii_lowercase + string.digits


def generate_simple_uuid(len):
    return ''.join(random.choices(alphabet, k=len))


def normalize_email(email):
    '''
    Reduces an email address to its canonical form:
        - strips white space
        - transforms to lowercase
        - removes the +tag part in the name
        - removes dots if a google domain
    '''
    email = email.strip().lower()
    name, domain = email.rsplit('@', 1)
    try:
        name, _ = name.rsplit('+', 1)
    except ValueError:
        pass

    if domain in ['googlemail.com', 'gmail.com', 'google.com']:
        name = name.replace('.', '')

    return name + '@' + domain


day_in_seconds = 86400
jwt_algorithm = 'HS256'


def encode_jwt_token(payload, expires_in=day_in_seconds):
    payload.update({'exp': time() + expires_in})
    return jwt.encode(
        payload, BaseConfig.SECRET_KEY,
        algorithm=jwt_algorithm).decode('utf-8')


def decode_jwt_token(token):
    return jwt.decode(
        token, BaseConfig.SECRET_KEY, algorithms=[jwt_algorithm])
