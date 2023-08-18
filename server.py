import socketio
import eventlet
import time
import threading

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

def send_data():
    global sio
    print("sent event")
    sio.emit('kellyDer', {'data': [1,2,3,4,5,76,8,45,4,9]})
    time.sleep(1)

logger = threading.Thread(target=send_data, args=())
logger.start()

eventlet.wsgi.server(eventlet.listen(('localhost', 3000)), app)

