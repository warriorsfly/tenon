
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from authlib.jose import jwt, JoseError
from flask import current_app, request, url_for
from flask_login import UserMixin, AnonymousUserMixin
from .. import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    # employee_no
    username = db.Column(db.String(64), unique=True, index=True)

    name = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    avatar_hash = db.Column(db.String(32))
    password_hash = db.Column(db.String(128))
    roles = db.relationship('Role', secondary='role_user_link')
    groups = db.relationship('UserGroup', secondary='group_user_link')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # def generate_auth_token(self, expiration):
    #     s = Serializer(current_app.config['SECRET_KEY'],
    #                 expires_in=expiration)
    #     return s.dumps({'id': self.id})

    # @staticmethod
    # def verify_auth_token(token):
    #     s = Serializer(current_app.config['SECRET_KEY'])
    #     try:
    #         data = s.loads(token)
    #     except:
    #         return None
    #     return User.query.get(data['id'])

    # def verify_password(self, password):
    #     return check_password_hash(self.password_hash, password)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    # permissions = db.Column(db.Integer)
    users = db.relationship('User', secondary='role_user_link')


class RoleUserLink(db.Model):
    __tablename__ = 'role_user_link'
    role_id = db.Column(db.Integer, db.ForeignKey(
        'roles.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), primary_key=True)


class UserGroup(db.Model):
    __tablename__ = 'user_groups'

    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer)
    code = db.Column(db.String(10))
    name = db.Column(db.String(64))
    short_name = db.Column(db.String(10))
    module_id = db.Column(db.String(10), unique=True)
    users = db.relationship('User', secondary='group_user_link')


class GroupUserLink(db.Model):
    __tablename__ = 'group_user_link'
    group_id = db.Column(db.Integer, db.ForeignKey(
        'user_groups.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), primary_key=True)
