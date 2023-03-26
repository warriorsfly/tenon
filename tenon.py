from app import db,app,celery,migrate,socketio
from app.models import User, Role
from flask_migrate import Migrate




@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)
