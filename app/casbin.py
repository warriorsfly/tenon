import casbin_sqlalchemy_adapter
import casbin
from flask_authz import CasbinEnforcer

from . import db


__adapter__ = casbin_sqlalchemy_adapter.Adapter(engine=db.engine)

enforcer = casbin.Enforcer('./model.conf', __adapter__)
