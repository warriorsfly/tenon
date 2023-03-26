
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedSerializer as Serializer
from flask import current_app, request, url_for
from flask_login import UserMixin, AnonymousUserMixin
from .. import db

class User(UserMixin, db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    # employee_no
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    avatar_hash = db.Column(db.String(32))


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    # permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')
    
class Module(db.Model):
    __tablename__ = "modules"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    users = db.relationship('User', backref='role', lazy='dynamic')
    
