from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, Namespace, emit, join_room, leave_room, \
    close_room, rooms, disconnect

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

    def on_join(self, message):
        join_room(message['room'])
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response',
            {'data': 'In rooms: ' + ', '.join(rooms())})

    def on_leave(self, message):
        leave_room(message['room'])
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response',
            {'data': 'In rooms: ' + ', '.join(rooms())})

    def on_close_room(self, message):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response', {'data': 'Room ' + message['room'] + ' is closing.'},
                 room=message['room'])
            close_room(message['room'])

    def on_my_room_event(self, message):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response',
            {'data': message['data'], 'count': session['receive_count']},
            room=message['room'])


socketio.on_namespace(MyNamespace('/test'))


if __name__ == '__main__':
    socketio.run(app, debug=True)
