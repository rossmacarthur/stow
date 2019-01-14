import datetime

from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import BadSignature, SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from stow.config import Config


bcrypt = Bcrypt()
db = SQLAlchemy()


class BaseModel:

    def save(self):
        now = datetime.datetime.now()
        if hasattr(self, 'created') and not self.created:
            self.created = now
        if hasattr(self, 'modified'):
            self.modified = now
        if self.id is None:
            db.session.add(self)
        return db.session.commit()

    def destroy(self):
        db.session.delete(self)
        return db.session.commit()


class User(db.Model, BaseModel, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    modified = db.Column(db.DateTime, nullable=False)

    def __init__(self, *args, **kwargs):
        password = kwargs.pop('password', None)
        super().__init__(*args, **kwargs)
        if password:
            self.hash_password(password)

    def hash_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def generate_token(self):
        serializer = Serializer(Config.SECRET_KEY, expires_in=Config.TOKEN_LIFETIME)
        return serializer.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_token(token):
        try:
            serializer = Serializer(Config.SECRET_KEY)
            data = serializer.loads(token)
            return User.query.get(data['id'])
        except (SignatureExpired, BadSignature):
            return None


class Stow(db.Model, BaseModel):
    __tablename__ = 'stow'
    __table_args__ = (db.UniqueConstraint('user_id', 'key'),)
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    key = db.Column(db.String(100))
    value = db.Column(db.UnicodeText)
    created = db.Column(db.DateTime, nullable=False)
    modified = db.Column(db.DateTime, nullable=False)
