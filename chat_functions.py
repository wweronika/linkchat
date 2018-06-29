
def verify_token(user_id, user_token, cursor):
    cursor.execute('SELECT User_ID FROM Tokens WHERE token=%s', (user_token,))
    ID = cursor.fetchone()
    if ID is None:
        return False  
        
    return True

def verify_group_membership(group_id, user_id, cursor,):
    cursor.execute('SELECT User_ID FROM group_user WHERE (userID=%s AND groupID=%s)', (user_id, group_id, ))
    ID = cursor.fetchone()
    if ID is None:
        return False  

def verify_user_name(user_name, cursor):
    cursor.execute('SELECT ID FROM Users WHERE name=%s', (user_name, ))
    ID = cursor.fetchone()
    if ID is None:
        return False 
    
    return True

def get_recent_messages(user_ID):
    return []