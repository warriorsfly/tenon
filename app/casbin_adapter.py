import casbin_sqlalchemy_adapter
import casbin
from flask_authz import CasbinEnforcer

from . import db


adapter = casbin_sqlalchemy_adapter.Adapter(engine=db.engine)

casbin_enforcer = casbin.Enforcer('path/to/model.conf', adapter)
