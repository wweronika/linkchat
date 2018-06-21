from flask import Flask, render_template, session, request, redirect, url_for
from flask_socketio import SocketIO, Namespace, emit, join_room, leave_room, \
    close_room, rooms, disconnect
import sqlite3
import json
import random
import string
import chat_functions
import secret

"""


"""

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = secret.user
app.config['MYSQL_DATABASE_PASSWORD'] = secret.password
app.config['MYSQL_DATABASE_DB'] = secret.db
app.config['MYSQL_DATABASE_HOST'] = secret.host
mysql.init_app(app)

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@app.route('/register')
def register():
    return render_template('register.html', async_mode=socketio.async_mode)


@app.route('/register-verify', methods=["post", "get"])
def register_verify():
    print('data received in register')
    print(request.form)
    print(request.form['login'])

    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    t = (request.form['login'], '123', '123', request.form['email'])
    cursor.execute('insert into Users (login, password, salt, email) values(?,?,?,?)', t)
    connection.commit()
    connection.close()
    return redirect(url_for('index'))

@app.route('/login', methods=['post', 'get'])
def login():
    return render_template('login.html', async_mode=socketio.async_mode)


@app.route('/login-verify', methods=['post'])
def login_verify():
    data = request.data
    login = json.loads(data)['login']
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    check_login = cursor.execute('select ID from Users where login=?', (login, ))
    ID = check_login.fetchone()

    if ID is None:
        message = {}
        message['status'] = 'error'
        message['message'] = 'wrong login, bro'
        connection.commit()
        connection.close()
        return json.dumps(message)
    
    else:
        token = ''.join(
            random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in
            range(20))
        
        new_token = (ID[0], token, "user_info_some_day", )
        cursor.execute('insert into Tokens values (?, ?, ?)', new_token)
        message = {}
        message['status'] = 'success'
        message['token'] = token
        message['ID'] = ID[0]
        message['login'] = login
        connection.commit()
        connection.close()
        return json.dumps(message)
        
@app.route('/create-group')
def create_group():
    data = json.loads(request.data)
    group_name = data['group_name']
    userID = data['userID']
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    new_group = (group_name, )
    cursor.execute('INSERT INTO Groups (name) VALUES (?)', new_group)
    groupID = cursor.execute('SELECT ID FROM Groups WHERE name=?', (group_name, ))
    cursor.execute('INSERT INTO group_user (groupID, userID) VALUES (?, ?)', (groupID, userID, ))
    connection.commit()
    connection.close()
    
@app.route('/add-members')
def add_members():
    data = json.loads(request.data)
    member_list = data['member_list']
    groupID = data['groupID']
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    for member_name in member_list:
        memberID = cursor.execute('SELECT ID FROM Users WHERE name=?', (member_name, ))
        if memberID is not None:
            cursor.execute('INSERT INTO group_user (groupID, userID) VALUES (?, ?)', (groupID, memberID))
    connection.commit()
    connection.close()
"""

    /debug - a site that calls /debug-data to receive the latest data
    from the DB

"""
@app.route('/debug')
def debug_site():
    return render_template('debug.html')

@app.route('/app')
def chat_app():
    return render_template('app.html')

@app.route('/debug-data')
def debug_data():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    users = cursor.execute("SELECT * FROM Users")
    users = users.fetchall()
    connection.close()
    return json.dumps(users)

@app.route('/token-data')
def token_data():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    tokens = cursor.execute("SELECT * FROM Tokens")
    tokens = tokens.fetchall()
    connection.close()
    return json.dumps(tokens)

'''

    SocketIO down there

'''

@socketio.on('auth', namespace='/chat')
def auth(message):
    print(message)
    token = message['token']
    ID = message['ID']
    if chat_functions.verify_token(ID, token):
        last_messages = chat_functions.get_recent_messages(ID) # TODO: create get_recent_messages
        emit('auth_success', {'status': 'success', 'last_messages': last_messages})
        join_room(ID)
        session['ID'] = ID # Client's ID is mapped with his socket
    
    else:
        emit('auth_success', {'status': 'fail'})

@socketio.on('message', namespace='/chat')
def receive_message(message):
    user_ID = session['ID']
    group_ID = session['groupID']

@socketio.on('disconnect_request', namespace='/chat')
def disconnect_request():
    emit('my_response',
         {'data': 'Disconnected!'})
    disconnect()


@socketio.on('connect', namespace='/chat')
def test_connect():
    emit('my_response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/chat')
def test_disconnect():
    print('Client disconnected', request.sid)


@socketio.on('join', namespace='/chat')
def join(message):
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms())})


@socketio.on('leave', namespace='/chat')
def leave(message):
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms())})


@socketio.on('close_room', namespace='/chat')
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
