import casbin_sqlalchemy_adapter
import casbin
from flask_authz import CasbinEnforcer

from . import app,db


__adapter__ = casbin_sqlalchemy_adapter.Adapter(engine=db.engine)

csbn_efcr = CasbinEnforcer(app, __adapter__)
