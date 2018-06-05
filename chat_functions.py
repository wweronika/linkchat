import sqlite3

def verify_token(user_id, user_token):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    ID = cursor.execute('SELECT User_ID FROM Tokens WHERE token=?', (user_token,))
    ID = ID.fetchone()
    if ID is None:
        return False  
        
    return True

def verify_group_membership(group_id, user_id):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    ID = cursor.execute('SELECT User_ID FROM group_user WHERE (userID=? AND groupID=?)', (user_id, group_id, ))
    ID = ID.fetchone()
    if ID is None:
        return False  

def verify_user_name(user_name):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    ID = cursor.execute('SELECT ID FROM Users WHERE name=?', (user_name, ))
    ID = ID.fetchone()
    if ID is None:
        return False 
    
    return True