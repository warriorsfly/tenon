
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


class UserGroup(db.Model):
    """用户组:factory-厂别；department:部门;section-课；team-小组"""
    __tablename__ = 'user_groups'

    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer)
    code = db.Column(db.String(10))
    name = db.Column(db.String(64))
    short_name = db.Column(db.String(10))
    
    users = db.relationship('User', secondary='group_user_link')
    roles = db.relationship('Role', secondary='group_user_link')


class GroupUserLink(db.Model):
    __tablename__ = 'group_user_link'
    group_id = db.Column(db.Integer, db.ForeignKey(
        'user_groups.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), primary_key=True)


class Role(db.Model):
    """厂长，处长、副处长、部经理、副经理、课级主管、副理，PE，EE"""
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    short_name = db.Column(db.String(10))
    power = db.Column(db.Integer)
    # permissions = db.Column(db.Integer)
    user_groups = db.relationship('UserGroup', secondary='user_group_role_link')
    apis = db.relationship('ApiStore', secondary='role_api_permissions_link')
    menus = db.relationship('MenuStore', secondary='role_menu_permissions_link')


class GroupRoleLink(db.Model):
    __tablename__ = 'user_group_role_link'
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), primary_key=True)
    user_group_id = db.Column(db.Integer, db.ForeignKey(
        'user_groups.id'), primary_key=True)

class ApiStore(db.Model):
    __tablename__ = "api_store"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(255), comment='api url')
    group = db.Column(db.String(512), comment='api group')
    brief = db.Column(db.Text, comment='comment')
    request_method = db.Column(db.String(200), comment='method')
    is_delete = db.Column(db.Boolean, default=0)
    
class RoleApiPermission(db.Model):
    __tablename__ = "role_api_permissions_link"
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), primary_key=True)
    api_id = db.Column(db.Integer, db.ForeignKey('api_store.id'), primary_key=True)

class MenuStore(db.Model):
    __tablename__ = "menu_store"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pid = db.Column(db.Integer, comment='parent menu id')
    name = db.Column(db.String(200))
    en_name = db.Column(db.String(200))
    icon = db.Column(db.String(200))
    url = db.Column(db.String(200))
    sort = db.Column(db.Integer)
    is_delete = db.Column(db.Boolean, default=0)

class RoleMenuPermission(db.Model):
    __tablename__ = "role_menu_permissions_link"
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu_store.id'), primary_key=True) 

class CasbinRule(db.Model):
    __tablename__ = "casbin_rule"

    id = db.Column(db.Integer, primary_key=True)
    ptype = db.Column(db.String(255))
    v0 = db.Column(db.String(255))
    v1 = db.Column(db.String(255))
    v2 = db.Column(db.String(255))
    v3 = db.Column(db.String(255))
    v4 = db.Column(db.String(255))
    v5 = db.Column(db.String(255))

    def __str__(self):
        arr = [self.ptype]
        for v in (self.v0, self.v1, self.v2, self.v3, self.v4, self.v5):
            if v is None:
                break
            arr.append(v)
        return ", ".join(arr)

    def __repr__(self):
        return '<CasbinRule {}: "{}">'.format(self.id, str(self))