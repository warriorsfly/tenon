from . import app, celery,socketio

@socketio.on('connection',namespace='/production')
def on_onconection():
    pass

@celery.task(name="task.message")
def send_message(event, namespace, room, message):
	pass
