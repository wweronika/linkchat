from flask import Flask, render_template, session, request, redirect, url_for
from flask_socketio import SocketIO, Namespace, emit, join_room, leave_room, \
    close_room, rooms, disconnect
import sqlite3
import json
import random
import string
import chat_functions
import secret
from flaskext.mysql import MySQL
import emailaccess
import secrets

"""


"""

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
app.config['MYSQL_DATABASE_USER'] = secret.user
app.config['MYSQL_DATABASE_PASSWORD'] = secret.password
app.config['MYSQL_DATABASE_DB'] = secret.db
app.config['MYSQL_DATABASE_HOST'] = secret.host

mysql = MySQL(app)


# a global Database connection object
DatabaseConnection = mysql.connect()
DatabaseCursor = DatabaseConnection.cursor()

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@app.route('/register')
def register():
    return render_template('register.html', async_mode=socketio.async_mode)


@app.route('/register-verify', methods=["post", "get"])
def register_verify():
    global DatabaseCursor
    print('data received in register')
    print(request.form)
    print(request.form['login'])
    t = (request.form['login'], '123', '123', request.form['email'])
    DatabaseCursor.execute('INSERT INTO users (login, salted_password, salt, email) VALUES(%s,%s,%s,%s)', t)
    
    account_activation_token = secrets.token_urlsafe()
    try:
        emailaccess.send_activation_message(request.form['email'], account_activation_token)

        DatabaseCursor.execute('INSERT INTO activation_links VALUES (%s, NOW(), %s)', (account_activation_token, request.form['login']))
        DatabaseConnection.commit()
    except e:
        return "stuff went wrong, try again"

    return redirect(url_for('index'))

@app.route('/login', methods=['post', 'get'])
def login():
    return render_template('login.html', async_mode=socketio.async_mode)


@app.route('/login-verify', methods=['post'])
def login_verify():
    global DatabaseCursor
    data = request.data
    login = json.loads(data)['login']
    check_login = DatabaseCursor.execute('select user_id from users where login=%s', (login, ))
    ID = DatabaseCursor.fetchone()

    if ID is None:
        message = {}
        message['status'] = 'error'
        message['message'] = 'wrong login, bro'
        return json.dumps(message)
    
    else:
        token = ''.join(
            random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in
            range(20))
        
        new_token = (ID[0], token )
        DatabaseCursor.execute('insert into tokens values (%s, %s)', new_token)
        DatabaseConnection.commit()
        message = {}
        message['status'] = 'success'
        message['token'] = token
        message['ID'] = ID[0]
        message['login'] = login
        return json.dumps(message)
        
@app.route('/create-group')
def create_group():
    global DatabaseCursor
    data = json.loads(request.data)
    group_name = data['group_name']
    userID = data['userID']
    new_group = (group_name, )
    DatabaseCursor.execute('INSERT INTO groups (name) VALUES (%s)', new_group)
    groupID = DatabaseCursor.execute('SELECT ID FROM groups WHERE name=%s', (group_name, ))
    DatabaseCursor.execute('INSERT INTO user_group (group_id, user_id) VALUES (%s, %s)', (groupID, userID, ))
    DatabaseConnection.commit()
    
@app.route('/add-members')
def add_members():
    global DatabaseCursor
    data = json.loads(request.data)
    member_list = data['member_list']
    groupID = data['group_id']
    for member_name in member_list:
        memberID = DatabaseCursor.execute('SELECT user_id FROM users WHERE name=%s', (member_name, ))
        if memberID is not None:
            DatabaseCursor.execute('INSERT INTO user_group (groupID, userID) VALUES (%s, %s)', (groupID, memberID))
            DatabaseConnection.commit()


@app.route('/activate-account/<token>')
def account_activation (token):
    DatabaseCursor.execute('SELECT user_login from activation_links WHERE token=%s', (token, ))
    
    response = DatabaseCursor.fetchone()

    if response is None:
        return "Wrong activation code, can u even copy paste?"

    login = response[0]

    DatabaseCursor.execute('UPDATE users SET is_active=1 WHERE login=%s', (login, ))
    DatabaseConnection.commit()

    return "Account active, log in now"

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
    DatabaseCursor.execute("SELECT * FROM users")
    users = DatabaseCursor.fetchall()
    return json.dumps(users)

@app.route('/token-data')
def token_data():
    DatabaseCursor.execute("SELECT * FROM tokens")
    tokens = DatabaseCursor.fetchall()
    return json.dumps(tokens)

'''

    SocketIO down there

'''

@socketio.on('auth', namespace='/chat')
def auth(message):
    global DatabaseCursor
    print(message)
    token = message['token']
    ID = message['ID']
    if chat_functions.verify_token(ID, token, DatabaseCursor):
        last_messages = chat_functions.get_recent_messages(ID) # TODO: create get_recent_messages
        emit('auth_success', {'status': 'success', 'last_messages': last_messages})
        join_room(ID)
        session['ID'] = str(ID) # Client's ID is mapped with his socket, so the server remembers the user 
    
    else:
        emit('auth_success', {'status': 'fail'})



@socketio.on('get_message_history', namespace='/chat')
def get_message_history(message):
    if session['ID'] is None:
        emit('fail', {'status': 'socket not authorised'})
        return
    
    ## TODO: SKOŃCZYLIŚMY TUTAJ
    


@socketio.on('message', namespace='/chat')
def receive_message(message):
    
    # Retrieve the message info
    user_ID = session['ID']
    group_ID = message['groupID']
    text = message['text']

    # Insert the message into the DB
    data = (user_ID, group_ID, text,)
    sql = 'INSERT INTO messages (sender_id, is_link, group_id, text) VALUES(%s, false, %s, %s)'
    DatabaseCursor.execute(sql, data)
    DatabaseConnection.commit()

    # Emit the message to users in the group
    ## 1. Get users in the message's group


    data = (group_ID,)
    sql = 'SELECT user_id from user_group where group_idX=%s'
    DatabaseCursor.execute(sql,data)
    reciptients = DatabaseCursor.fetchall()
    #print('===============')
    #print(reciptients)
    #print('===============')
    ## 2. Send the event to each user

    for reciptient in reciptients:
        reciptient = str(reciptient[0])
        print(reciptient)
        emit('message', {'text': text, 'userID': user_ID},
            room=reciptient)
    
    DatabaseCursor.execute('UPDATE groups SET last_message=NOW() WHERE group_id=%s',(group_ID, ))
    

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
    global DatabaseCursor
    t = (None, 23, 0, 1, message)
    DatabaseCursor.execute('insert into Messages values (%s, %s, %s, %s, %s)', t)
    DatabaseConnection.commit()


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
