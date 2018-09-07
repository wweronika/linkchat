
def verify_token(user_id, user_token, cursor):
    cursor.execute('SELECT user_id FROM tokens WHERE token=%s', (user_token,))
    ID = cursor.fetchone()
    if ID is None:
        return False  
        
    return True

def verify_group_membership(group_id, user_id, cursor):
    cursor.execute('SELECT user_id FROM user_group WHERE (user_id=%s AND group_id=%s)', (user_id, group_id, ))
    ID = cursor.fetchone()
    if ID is None:
        return False  

def verify_user_name(user_name, cursor):
    cursor.execute('SELECT user_id FROM users WHERE login=%s', (user_name, ))
    ID = cursor.fetchone()
    if ID is None:
        return False 
    
    return True

def get_recent_messages(user_ID):
    return []