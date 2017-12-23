import datetime
import hashlib
import jwt
import os
from binascii import unhexlify, hexlify as hexlify_

from . import db
from .config import Config


def hexlify(bytes):
    return hexlify_(bytes).decode('utf-8')


def pbkdf2_hash(password, salt):
    return hexlify(hashlib.pbkdf2_hmac('sha256', password.encode(), unhexlify(salt), 100000, dklen=20))


class BaseModel:

    def save(self):
        if hasattr(self, 'modified'):
            self.modified = datetime.datetime.now()
        if self.id is None:
            db.session.add(self)
        return db.session.commit()

    def destroy(self):
        db.session.delete(self)
        return db.session.commit()


class User(db.Model, BaseModel):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(96), nullable=False)
    modified = db.Column(db.DateTime, nullable=False)

    def __init__(self, name, password):
        self.name = name
        self.update_password(password)
        self.modified = datetime.datetime.now()

    def update_password(self, password):
        salt = hexlify(os.urandom(16))
        hashed = pbkdf2_hash(password, salt)
        self.password_hash = salt + hashed

    def verify_password(self, password):
        salt = self.password_hash[:32]
        hashed = pbkdf2_hash(password, salt)
        return self.password_hash == salt + hashed

    def generate_token(self):
        payload = {
            'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow() + Config.TOKEN_LIFETIME,
            'sub': self.id
        }
        return jwt.encode(payload, Config.SECRET_KEY, algorithm='HS512').decode()

    @staticmethod
    def decode_token(token):
        payload = jwt.decode(token, Config.SECRET_KEY)
        return User.query.filter_by(id=payload['sub']).first()


class Stow(db.Model, BaseModel):
    __tablename__ = 'stow'
    __table_args__ = (db.UniqueConstraint('user_id', 'key'),)
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    key = db.Column(db.String(100))
    value = db.Column(db.UnicodeText)
    modified = db.Column(db.DateTime, nullable=False)
