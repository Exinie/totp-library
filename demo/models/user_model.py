from db import query_one, execute


def get_user_by_username(username):
    return query_one(
        "SELECT id, username, password, totp_secret, totp_enabled FROM users WHERE username = ?",
        (username,),
    )


def get_user_by_id(user_id):
    return query_one(
        "SELECT id, username, password, totp_secret, totp_enabled FROM users WHERE id = ?",
        (user_id,),
    )


def create_user(username, password_hash):
    execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, password_hash),
    )


def set_totp_secret(user_id, secret):
    execute(
        "UPDATE users SET totp_secret = ?, totp_enabled = 0 WHERE id = ?",
        (secret, user_id),
    )


def enable_totp(user_id):
    execute(
        "UPDATE users SET totp_enabled = 1 WHERE id = ?",
        (user_id,),
    )
