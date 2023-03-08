from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_moment import Moment
from celery import Celery, Task

mail = Mail()
moment = Moment()
db = SQLAlchemy()

def create_app(config_name)->Flask:
    app = Flask(__name__)
    app.config.from_object(config_name)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    create_celery(app)
    
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint,url_prefix = '/api/v1')
    
    return app
 
def create_celery(flsk:Flask)->Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with flsk.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(flsk.name, task_cls=FlaskTask)
    celery_app.config_from_object(flsk.config["CELERY"])
    celery_app.set_default()
    flsk.extensions["celery"] = celery_app
    return celery_app