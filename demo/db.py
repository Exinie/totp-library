import sqlite3
from flask import current_app, g


def get_db():
    if "conn" not in g:
        db_path = current_app.config["DB_PATH"]
        g.conn = sqlite3.connect(db_path)
        g.conn.row_factory = sqlite3.Row
    return g.conn


def close_db(error=None):
    conn = g.pop("conn", None)
    if conn is not None:
        conn.close()


def query_one(query, params=()):
    conn = get_db()
    cur = conn.execute(query, params)
    row = cur.fetchone()
    cur.close()
    return row


def query_all(query, params=()):
    conn = get_db()
    cur = conn.execute(query, params)
    rows = cur.fetchall()
    cur.close()
    return rows


def execute(query, params=()):
    conn = get_db()
    conn.execute(query, params)
    conn.commit()
