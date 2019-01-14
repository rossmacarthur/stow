import datetime
import os

import stow


def get_environment_variable(var, default=None):
    try:
        return os.environ[var]
    except KeyError:
        if default is None:
            raise RuntimeError(f'{var} environment variable must be set')
        else:
            return default

def get_debug():
    role = get_environment_variable('STOW_ROLE', default='DEV')

    if role == 'PROD':
        return False
    elif role == 'DEV':
        return True

    raise RuntimeError(f'invalid role {role}')


class Config:
    DEBUG = get_debug()
    SECRET_KEY = get_environment_variable('SECRET_KEY')
    MAX_USERS = 1
    TOKEN_LIFETIME = 3600
    META = {
        'author': stow.__author__,
        'description': stow.__description__,
        'keywords': 'flask store retrieve key value secure',
        'year': datetime.datetime.now().year
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI =  'sqlite:///../../stow.db'
    TEMPLATES_AUTO_RELOAD = True
