from flask import Flask, render_template, request
from flask_socketio import SocketIO, Namespace, emit, disconnect

async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


class MyNamespace(Namespace):
    def on_my_event(self, message):
        emit('my_response',
             {'data': message['data']})

    def on_my_broadcast_event(self, message):
        emit('my_response',
             {'data': message['data']},
             broadcast=True)

    def on_disconnect_request(self):
        emit('my_response',
             {'data': 'Disconnected!'})
        disconnect()


    def on_connect(self):
        emit('my_response', {'data': 'Connected', 'count': 0})

    def on_disconnect(self):
        print('Client disconnected', request.sid)


socketio.on_namespace(MyNamespace('/test'))


if __name__ == '__main__':
    socketio.run(app, debug=True)
