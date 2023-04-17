import casbin_sqlalchemy_adapter
import casbin
from flask_authz import CasbinEnforcer

from app.models.user import CasbinRule

from . import app,db


__adapter__ = casbin_sqlalchemy_adapter.Adapter(engine=db.engine,db_class=CasbinRule)

csbef = CasbinEnforcer(app, __adapter__)
