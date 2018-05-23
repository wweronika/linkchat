def verify_token(user_id, group_id, user_token):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    ID = cursor.execute('SELECT User_ID FROM Tokens WHERE token=?', (user_token,))
    ID = ID.fetchone()
    if ID is None:
        return False

    group = cursor.execute('SELECT * FROM group_user WHERE (groupID=? AND userID=?)', (group_id, user_id, ))
    group = group.fetchone()
    if group is None:
        return False   
    
    return True
