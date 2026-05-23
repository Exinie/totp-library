import bcrypt
from functools import wraps
from flask import session, redirect, url_for

from models.user_model import get_user_by_username, create_user


def hash_password(plain_text):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain_text.encode("utf-8"), salt).decode("utf-8")


def verify_password(plain_text, hashed):
    return bcrypt.checkpw(plain_text.encode("utf-8"), hashed.encode("utf-8"))


def register_user(username, password):
    if get_user_by_username(username):
        return False, "Username already exists"

    password_hash = hash_password(password)
    create_user(username, password_hash)
    return True, None


def authenticate_user(username, password):
    user = get_user_by_username(username)
    if not user:
        return None

    if not verify_password(password, user["password"]):
        return None

    return user


def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return view_func(*args, **kwargs)

    return wrapper
