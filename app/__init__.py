from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_moment import Moment
from celery import Celery, Task
from opentelemetry.instrumentation.flask import FlaskInstrumentor
# from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

# from opentelemetry import trace
# from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
# from opentelemetry.sdk.resources import SERVICE_NAME,Resource
# from opentelemetry.sdk.trace import TracerProvider
# from opentelemetry.sdk.trace.export import BatchSpanProcessor
# from opentelemetry.sdk.trace.export import ConsoleSpanExporter
# from opentelemetry.sdk.trace.export import SimpleSpanProcessor

import toml


def create_app() -> Flask:
    
    # trace.set_tracer_provider(TracerProvider(
    #     resource=Resource.create({SERVICE_NAME: __name__})
    # ))
    app = Flask(__name__)
    app.config.from_file('../config.toml', load=toml.load)
    FlaskInstrumentor.instrument_app(app)
    
    # otlp_exporter = OTLPSpanExporter()
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    # SQLAlchemyInstrumentor().instrument(engine=db.engine)
    # create_celery(app)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')
    return app


def create_celery(flsk: Flask) -> Celery:
    class TenonTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with flsk.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(flsk.name, task_cls=TenonTask)
    celery_app.config_from_object(flsk.config["CELERY"])
    celery_app.set_default()
    flsk.extensions["celery"] = celery_app
    return celery_app


mail = Mail()
moment = Moment()
db = SQLAlchemy()

app = create_app()
celery = create_celery(app)
migrate = Migrate(app, db)
