
from . import app, celery,mail
from flask import current_app, render_template
from flask_mail import Message


@celery.task
def send_async_email(sender,to, subject, template, **kwargs):
    message = Message(subject,
                  sender=sender, recipients=[to])
    message.body = render_template(template + '.txt', **kwargs)
    message.html = render_template(template + '.html', **kwargs)
    with app.app_context():
        mail.send(message)
