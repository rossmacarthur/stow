import dateutil
import traceback
from flask import g, jsonify, request
from flask_classful import FlaskView, route
from flask_httpauth import HTTPBasicAuth

from .config import Config
from .models import User, Stow


auth = HTTPBasicAuth()


class ServiceException(Exception):

    def __init__(self, message, status_code):
        super().__init__()
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        return {'message': self.message}


def accepted_content_type(f):
    """
    Check if the requested content type is application/json.
    """
    def decorator(*args, **kwargs):
        if request.content_type != 'application/json':
            raise ServiceException('Content type must be application/json', 400)
        return f(*args, **kwargs)
    return decorator


def error_handler(error):
    """
    Handle errors in views.
    """
    if not isinstance(error, ServiceException):
        payload = {'message': 'Unhandled server side exception'}
        if Config.DEBUG:
            payload['traceback'] = traceback.format_exc()
        return jsonify(payload), 500
    return jsonify(error.to_dict()), error.status_code


def check_fields_present(data, *fields):
    """
    Check if certain fields are present in a dictionary else raise 400.
    """
    missing = list()
    for field in fields:
        if field not in data:
            missing.append(field)
    if missing:
        fields = ', '.join("'{}'".format(field) for field in missing)
        raise ServiceException('The following fields are missing: {}'.format(fields), 400)


@auth.verify_password
def verify_password(name_or_token, password):
    user = User.verify_token(name_or_token)
    if not user:
        user = User.query.filter_by(name=name_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@auth.error_handler
def unauthorized_handler():
    return jsonify({'message': 'Unauthorized Access'})


class BaseView(FlaskView):
    decorators = [accepted_content_type]


class TokenView(BaseView):

    @auth.login_required
    def get(self):
        return jsonify({'token': g.user.generate_token(), 'duration': Config.TOKEN_LIFETIME})


class UserView(BaseView):

    @route('/', methods=['GET'])
    @auth.login_required
    def get(self):
        return jsonify({'id': g.user.id, 'name': g.user.name,
                        'created': g.user.created.isoformat()})

    def post(self):
        data = request.get_json()
        check_fields_present(data, 'name', 'password')
        if User.query.count() >= Config.MAX_USERS:
            raise ServiceException('No more users may be registered', 403)
        user = User.query.filter_by(name=data['name']).first()
        if user:
            raise ServiceException('User with name \'{}\' already exists'.format(user.name), 409)
        user = User(name=data['name'], password=data['password'])
        user.save()
        return jsonify({'message': 'User \'{}\' registered'.format(user.name)}), 201

    @route('/', methods=['DELETE'])
    @auth.login_required
    def delete(self):
        g.user.destroy()
        return jsonify({'message': 'User deleted'})


class StowView(BaseView):
    decorators = [accepted_content_type, auth.login_required]

    @staticmethod
    def _get_stow(key):
        stow = Stow.query.filter_by(user_id=g.user.id, key=key).first()
        if not stow:
            raise ServiceException('No entry was not found for key \'{}\''.format(key), 404)
        return stow

    def index(self):
        stows = {stow.key: {'value': stow.value, 'created': stow.created.isoformat(),
                            'modified': stow.modified.isoformat()}
                 for stow in Stow.query.filter_by(user_id=g.user.id).all()}
        return jsonify({'entries': stows})

    def get(self, key):
        stow = self._get_stow(key)
        return jsonify({'value': stow.value, 'created': stow.created.isoformat(),
                        'modified': stow.modified.isoformat()})

    def put(self, key):
        data = request.get_json()
        check_fields_present(data, 'value')
        stow = Stow.query.filter_by(user_id=g.user.id, key=key).first()
        if not stow:
            stow = Stow(user_id=g.user.id, key=key)
        elif 'modified' in data:
            modified = dateutil.parser.parse(data['modified'])
            if modified <= stow.modified:
                raise ServiceException('Conflicting timestamps', 409)
        stow.value = data['value']
        stow.save()
        return jsonify({'message': 'Entry stored successfully'})

    def delete(self, key):
        stow = self._get_stow(key)
        stow.destroy()
        return jsonify({'message': 'Entry deleted'})
