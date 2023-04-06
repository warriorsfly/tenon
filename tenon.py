from flask_migrate import Migrate
from app import db,app,celery,socketio
from app.models import User, Role


migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)
