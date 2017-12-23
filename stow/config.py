import datetime
import os


def get_environment_variable(var):
    value = os.environ.get(var)
    if value:
        return value
    raise RuntimeError('{} environment variable must be set'.format(var))


class Config:
    DEBUG = False
    SECRET_KEY = get_environment_variable('SECRET_KEY')
    MAX_USERS = 1
    TOKEN_LIFETIME = datetime.timedelta(days=30)
