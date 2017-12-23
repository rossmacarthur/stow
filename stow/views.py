import datetime
import jwt
import traceback
from flask import jsonify, request
from flask.views import MethodView

from .config import Config
from .models import User, Stow


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


def error_handler_view(error):
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
    for field in fields:
        if field not in data:
            raise ServiceException('\'{}\' field is missing from the request.'.format(field), 400)


def get_user():
    """
    Gets the user from the Authorization header otherwise raises 401.
    """
    token = request.headers.get('Authorization')
    if token:
        try:
            user = User.decode_token(token)
            if user:
                return user
            else:
                raise ServiceException('User not found', 404)
        except jwt.InvalidTokenError:
            pass
    raise ServiceException('No valid token provided', 401)


class BaseView(MethodView):
    decorators = [accepted_content_type]


class UserView(BaseView):

    def post(self):
        data = request.get_json()
        check_fields_present(data, 'name', 'password')

        if User.query.count() >= Config.MAX_USERS:
            raise ServiceException('No more users may be registered', 403)

        user = User.query.filter_by(name=data.get('name')).first()
        if user:
            raise ServiceException('User with name \'{}\' already exists'.format(user.name), 202)

        user = User(
            name=data.get('name'),
            password=data.get('password')
        )
        user.save()

        return jsonify({'message': 'User \'{}\' registered'.format(user.name), 'token': user.generate_token()}), 201

    def delete(self):
        user = get_user()
        user.destroy()
        return jsonify({'message': 'User deleted'}), 200


class TokenView(BaseView):

    def post(self):
        data = request.get_json()
        check_fields_present(data, 'name', 'password')

        user = User.query.filter_by(name=data.get('name')).first()
        if not user or not user.verify_password(data.get('password')):
            raise ServiceException('Token generation failed', 401)

        return jsonify({'message': 'Token generation succeeded', 'token': user.generate_token()}), 200


class StowView(BaseView):

    def get(self):
        user = get_user()
        data = request.args
        check_fields_present(data, 'key')
        stow = Stow.query.filter_by(user_id=user.id, key=data.get('key')).first()
        if not stow:
            raise ServiceException('No entry was not found for key {}'.format(data.get('key')), 404)
        return jsonify({'key': stow.key, 'value': stow.value, 'modified': stow.modified})

    def delete(self):
        user = get_user()
        data = request.args
        check_fields_present(data, 'key')
        stow = Stow.query.filter_by(user_id=user.id, key=data.get('key')).first()
        if not stow:
            raise ServiceException('No entry was not found for key {}'.format(data.get('key')), 404)
        stow.destroy()
        return jsonify({'message': 'Entry deleted'}), 200

    def put(self):
        user = get_user()
        data = request.get_json()
        check_fields_present(data, 'key', 'value')

        stow = Stow.query.filter_by(user_id=user.id, key=data.get('key')).first()
        if not stow:
            stow = Stow()
            stow.user_id = user.id
            stow.key = data.get('key')
        elif 'modified' in data:
            modified = datetime.datetime.fromtimestamp(data.get('modified'))
            if modified <= stow.modified:
                return jsonify({
                    'message': 'Conflicting timestamps',
                    'modified': stow.modified
                }), 409

        stow.value = data.get('value')
        stow.save()

        return jsonify({'message': 'Entry stored successfully'}), 200
