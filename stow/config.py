import os


def get_environment_variable(var):
    try:
        return os.environ[var]
    except KeyError:
        raise RuntimeError('{} environment variable must be set'.format(var))


class Config:
    DEBUG = True if get_environment_variable('ROLE') == 'DEV' else False
    SECRET_KEY = get_environment_variable('SECRET_KEY')
    MAX_USERS = 1
    TOKEN_LIFETIME = 3600
    META = {
        'author': 'Ross MacArthur',
        'description': 'A Flask app to securely store and retrieve data.',
        'keywords': 'flask store retrieve key value secure'
    }
