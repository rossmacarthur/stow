import datetime
import os

import stow


def get_environment_variable(var, default=None):
    try:
        return os.environ[var]
    except KeyError:
        if default is None:
            raise RuntimeError(f'{var!r} environment variable must be set')
        else:
            return default


def dirnames(path, up=1):
    if up == 0:
        return path
    else:
        return os.path.dirname(dirnames(path, up=up-1))


class BaseConfig:
    MAX_USERS = 1
    TOKEN_LIFETIME = 3600
    META = {
        'author': stow.__author__,
        'description': stow.__description__,
        'keywords': 'flask store retrieve key value secure',
        'year': datetime.datetime.now().year
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = (
        'sqlite:///' + os.path.join(dirnames(os.path.abspath(__file__), up=3), 'stow.db')
    )
    TEMPLATES_AUTO_RELOAD = True


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SECRET_KEY = get_environment_variable(
        'FLASK_SECRET_KEY',
        default='secret'
    )


class ProductionConfig(BaseConfig):
    DEBUG = False
    SECRET_KEY = get_environment_variable('FLASK_SECRET_KEY')


role = get_environment_variable('FLASK_ENV', default='production')

if role == 'development':
    Config = DevelopmentConfig
elif role == 'production':
    Config = ProductionConfig
else:
    raise RuntimeError(f'invalid role {role!r}')
