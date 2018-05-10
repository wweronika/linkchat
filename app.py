from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, Namespace, emit, join_room, leave_room, \
    close_room, rooms, disconnect
import sqlite3


# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@app.route('/login')
def login():
    return render_template('login.html', async_mode=socketio.async_mode)

@app.route('/login-verify', methods=["post", "get"])
def login_verify():
    print('data received in login')
    print(request.form)
    print(request.form['login'])

    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    t = (0, request.form['login'], '', '', request.form['email']) #all IDs set to 0 since a classic global variable is insufficient
    cursor.execute('insert into Users values (?, ?, ?, ?, ?)', t)
    connection.commit()
    connection.close()
    return ""

@socketio.on('my_event', namespace='/test')
def test_message(message):
    emit('my_response',
         {'data': message['data']})


@socketio.on('my_broadcast_event', namespace='/test')
def test_broadcast_message(message):
    emit('my_response',
         {'data': message['data']},
         broadcast=True)



@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    emit('my_response',
         {'data': 'Disconnected!'})
    disconnect()


@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my_response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)

@socketio.on('join', namespace='/test')
def join(message):
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms())})


@socketio.on('leave', namespace='/test')
def leave(message):
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms())})


@socketio.on('close_room', namespace='/test')
def close(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response', {'data': 'Room ' + message['room'] + ' is closing.'},
         room=message['room'])
    close_room(message['room'])


def save_msg_to_db(message):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    t = (None, 23, 0, 1, message)
    cursor.execute('insert into Messages values (?, ?, ?, ?, ?)', t)
    connection.commit()
    connection.close()


@socketio.on('my_room_event', namespace='/test')
def send_room_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data']},
         room=message['room'])
    save_msg_to_db(message['data'])


if __name__ == '__main__':
    socketio.run(app, debug=True)
    disconnect()


@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my_response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    socketio.run(app, debug=True)
