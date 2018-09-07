INSERT INTO users (
        user_id,
        login,
        salted_password,
        salt,
        email,
        is_active
    ) VALUES (
        1,
        'baczek',
        '',
        '',
        'mateusz.baczek1998@gmail.com',
        1
    );

INSERT INTO users (
        user_id,
        login,
        salted_password,
        salt,
        email,
        is_active
    ) VALUES (
        2,
        'wiesiolek',
        '',
        '',
        'wiesiolek@wiesiolek.com',
        1
    );




INSERT INTO groups (group_id, title, last_message) VALUES (1, 'abc', NOW());

INSERT INTO user_group (user_id, group_id) VALUES (1, 1);
INSERT INTO user_group (user_id, group_id) VALUES (2, 1);